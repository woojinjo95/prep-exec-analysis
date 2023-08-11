import logging
import asyncio
import traceback
import os
import json
import redis.asyncio as redis

logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", '')
CHANNEL_NAME = os.getenv("CHANNEL_NAME", 'shell')


async def get_redis_pool():
    return await redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)


def check_skip_message(raw: any):
    try:
        if raw is None:
            return False, None
        if not isinstance(raw, dict):
            return False, None

        message = json.loads(raw['data'])

        # 에코 메시지 체크
        service = message['service']
        if service == 'shell':
            print(f"check_skip_message service == {service}")
            return False

        level = message['level']
        # info가 아닌 모든 메시지 스킵
        if level != 'info':
            print(f"check_skip_message level: {level}")
            print(f"trace: {message}")
            return False

        # msg가 start or stop이 아닌 모든 메시지 스킵
        msg = message['msg']
        if msg != 'start' and msg != 'stop':
            print(f"check_skip_message shell: {msg}")
            return False

        # data = message['data']
        # if data is None:
        #     print(f"check_skip_message data: {data}")
        #     return False

        return True
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False

async def consumer_adb_handler(conn: any, CHANNEL_NAME: str):
    print(f"subscribe {CHANNEL_NAME}")
    pubsub = conn.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    while True:
        try:  # 루프 깨지지 않도록 예외처리
            raw = await pubsub.get_message(ignore_subscribe_messages=True)

            if not check_skip_message(raw):
                continue

        except Exception as e:
            print(exc)
            print(traceback.format_exc()
    print("consumer_handler end")
async def main():
    conn = await get_redis_pool()

    # 레디스로 시작, 중단 메시지를 받아야 함
    # 수행해야 하는 블럭 정보는 몽고DB를 통해 받아야 함
    # 수행해야 하는 시나리오 정보는 redis의 키를 통해 몽고DB에서 조회해야 함


    try:
        # 시작 또는 중단 메시지를 받는 레디스 핸들러
        print("Start task")
        done, pending = await asyncio.wait(
            [redis_message_task], return_when=asyncio.FIRST_COMPLETED,
        )

        print(f"Done task: {done}")

        for task in pending:
            print(f"Canceling task: {task}")
            task.cancel()
    except Exception as e:
        print(e)
        print(traceback.format_exc())


asyncio.run(main())
