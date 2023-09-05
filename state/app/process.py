import asyncio
import json
import logging
import time
import traceback
from enum import Enum

from db import CHANNEL_NAME, get_redis_pool

logger = logging.getLogger(__name__)


class ServiceStateEnum(Enum):
    idle = "idle"
    streaming = "streaming"
    playblock = "playblock"
    analysis = "analysis"


def set_message(msg: str, data: dict = {}, level: str = 'info'):
    return json.dumps({
        "service": 'state',
        "level": level,
        "time": time.time(),
        "msg": msg,
        "data": data
    })


async def set_service_state_and_pub(redis_connection, state):
    state = state.value
    # 상태 변경
    await redis_connection.hset('common', 'service_state', state)

    # 상태 변경 메세지 전송
    await redis_connection.publish(CHANNEL_NAME, set_message(msg="service_state", data={"state": state}))


async def pub_msg(redis_connection, msg, data):
    await redis_connection.publish(CHANNEL_NAME, set_message(msg=msg, data=data))


async def consumer_handler(conn: any, CHANNEL_NAME: str):
    try:
        pubsub = conn.pubsub()
        await pubsub.subscribe(CHANNEL_NAME)
        while True:
            try:  # 루프 깨지지 않도록 예외처리
                raw = await pubsub.get_message(ignore_subscribe_messages=True)
                await asyncio.sleep(0.001)
                command_data = raw.get('data', None) if raw else None
                data = json.loads(command_data) if isinstance(command_data, str) else {}
                msg = data.get('msg', None)

                if msg == 'start_playblock_response':
                    print('----> start_playblock_response')
                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.playblock)

                # 분석 페이지에 진입했을때 -> 분석
                if msg == 'analysis_mode':
                    print('----> analysis_mode')
                    # 로그수집 중단 메세지 전송
                    await pub_msg(conn, msg="stb_log", data={"control": "stop"})

                    # 스트리밍 중단 메세지 전송
                    await pub_msg(conn, msg="streaming", data={"action": "stop"})

                    # 컬러레퍼런스 분석 메세지 전송
                    await pub_msg(conn, msg="analysis", data={"measurement": ["color_reference"]})

                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.idle)

                # 액션 페이지에 진입했을때 -> 녹화
                if msg == 'action_mode':
                    print('----> action_mode')
                    # 분석 중단 메세지 전송
                    await pub_msg(conn, msg="analysis_terminate", data={})

                    # 로그수집 시작 메세지 전송
                    await pub_msg(conn, msg="stb_log", data={"control": "start"})

                    # 스트리밍 시작 메세지 전송
                    await pub_msg(conn, msg="streaming", data={"action": "start"})

                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.streaming)

                # 분석이 시작되었을 때
                if msg == 'analysis_started':
                    print('----> analysis_started')
                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.analysis)

                # 분석이 종료되었을 때
                if msg == 'analysis_response':
                    print('----> analysis_response')
                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.idle)

                # 분석 시작
                if msg == 'analysis':
                    print('----> analysis')
                    msg_data = data.get('data', {})
                    measurement = msg_data.get('measurement', [])
                    if 'log_level_finder' in measurement:
                        await pub_msg(conn, msg="analysis_response", data=msg_data)

                        # 상태 변경 및 메세지 전송
                        await set_service_state_and_pub(conn, ServiceStateEnum.idle)

            except Exception as e:
                print(e, traceback.format_exc())
    except Exception as e:
        print(e, traceback.format_exc())
    finally:
        print("consumer_handler end")


async def main():
    conn = await get_redis_pool()
    try:
        consumer_task = asyncio.create_task(consumer_handler(conn=conn, CHANNEL_NAME=CHANNEL_NAME))
        print("Start task")
        done, pending = await asyncio.wait([consumer_task], return_when=asyncio.FIRST_COMPLETED)

        print(f"Done task: {done}")
        for task in pending:
            print(f"Canceling task: {task}")
            task.cancel()
    except Exception as e:
        print(e, traceback.format_exc())


asyncio.run(main())
