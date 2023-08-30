import asyncio
import json
import logging
import logging.config
import traceback
from threading import Thread

import sentry_sdk
from app import schemas
from app.api.api_v1.api import api_router
from app.api.utility import set_redis_pub_msg
from app.core.config import settings
from app.db.redis_session import RedisClient
from app.schemas.enum import ServiceStateEnum
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

logging.config.fileConfig('./app/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
sentry_sdk.init(dsn=settings.SENTRY_DSN)
sentry_sdk.set_tag("service", f"{settings.SERVICE_NAME}-backend")


def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    return app


app = get_application()


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def set_service_state_and_pub(state):
    state = state.value
    # 상태 변경
    RedisClient.hset('common', 'service_state', state)

    # 상태 변경 메세지 전송
    RedisClient.publish('command',
                        set_redis_pub_msg(msg="service_state", data={"state": state}))


def command_parser(command):
    command_data = command.get('data', None)
    data = json.loads(command_data) if isinstance(command_data, str) else {}
    msg = data.get('msg', None)

    # 액션블럭이 종료되면 리플레이가 전송한 메세지 수신 -> 대기
    if msg == 'end_playblock':
        # 로그수집 중단 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="stb_log", data={"control": "stop"}))

        # 스트리밍 중단 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="streaming", data={"action": "stop"}))

        # 상태 변경 및 메세지 전송
        set_service_state_and_pub(ServiceStateEnum.idle)

    # 액션 페이지에서 액션블럭 재생시 -> 재생
    elif msg == 'start_playblock_response':
        # 상태 변경 및 메세지 전송
        set_service_state_and_pub(ServiceStateEnum.playblock)

    # 분석 페이지에 진입했을때 -> 분석
    elif msg == 'analysis_mode':
        # 로그수집 중단 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="stb_log", data={"control": "stop"}))

        # 스트리밍 중단 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="streaming", data={"action": "stop"}))

        # 컬러레퍼런스 분석 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="analysis", data={"measurement": ["color_reference"]}))

        # 상태 변경 및 메세지 전송
        set_service_state_and_pub(ServiceStateEnum.idle)

    # 액션 페이지에 진입했을때 -> 녹화
    elif msg == 'action_mode':
        # 분석 중단 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="analysis_terminate", data={}))

        # 로그수집 시작 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="stb_log", data={"control": "start"}))

        # 스트리밍 시작 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="streaming", data={"action": "start"}))

        # 상태 변경 및 메세지 전송
        set_service_state_and_pub(ServiceStateEnum.streaming)

    # 분석이 시작되었을 때
    if msg == 'analysis_started':
        # 상태 변경 및 메세지 전송
        set_service_state_and_pub(ServiceStateEnum.analysis)

    # 분석이 종료되었을 때
    if msg == 'analysis_response':
        # 상태 변경 및 메세지 전송
        set_service_state_and_pub(ServiceStateEnum.idle)

    # 분석 시작
    if msg == 'analysis':
        msg_data = data.get('data', {})
        measurement = msg_data.get('measurement', [])
        if 'loudness' in measurement or 'log_level_finder' in measurement:
            RedisClient.publish('command',
                                set_redis_pub_msg(msg="analysis_response", data=msg_data))


def subscribe_to_redis():
    pubsub = RedisClient.pubsub()
    pubsub.subscribe('command')
    for command in pubsub.listen():
        command_parser(command)


def start_redis_subscription():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(subscribe_to_redis())


@app.on_event("startup")
async def startup_event():
    redis_thread = Thread(target=start_redis_subscription)
    redis_thread.daemon = True
    redis_thread.start()


@api_router.get("/healthcheck", response_model=schemas.Msg)
def healthcheck() -> schemas.Msg:
    try:
        from app.db.session import db_session
        RedisClient.hget(name='item', key='id')
        db_session
    except Exception as er:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"msg": "OK"}


app.include_router(api_router, prefix=settings.API_V1_STR)
