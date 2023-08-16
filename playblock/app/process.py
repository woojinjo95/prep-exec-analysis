import logging
import asyncio
import traceback
from sub.message import check_skip_message
from sub.redis import get_redis_pool, CHANNEL_NAME 

logger = logging.getLogger(__name__)




async def consumer_handler(conn: any, CHANNEL_NAME: str):
    print(f"subscribe {CHANNEL_NAME}")
    pubsub = conn.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    while True:
        try:  # 루프 깨지지 않도록 예외처리
            raw = await pubsub.get_message(ignore_subscribe_messages=True)
            asyncio.sleep(0.001)

            check_skip, message = check_skip_message(raw)
            if not check_skip:
                continue
            command = message['data']['command']
            if command == "start":
                print("start")
            if command == "stop":
                print("stop")
            
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            print("consumer_handler end")


async def main():
    conn = await get_redis_pool()

    # 수행해야 하는 블럭 정보는 몽고DB를 통해 받아야 함
    # 수행해야 하는 시나리오 정보는 redis의 키를 통해 몽고DB에서 조회해야 함

    try:
        consumer_task = asyncio.create_task(consumer_handler(conn=conn, CHANNEL_NAME=CHANNEL_NAME))

        print("Start task")
        done, pending = await asyncio.wait(
            [consumer_task], return_when=asyncio.FIRST_COMPLETED,
        )

        print(f"Done task: {done}")

        for task in pending:
            print(f"Canceling task: {task}")
            task.cancel()
    except Exception as e:
        print(e)
        print(traceback.format_exc())


# asyncio.run(main())
