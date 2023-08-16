import logging
import asyncio
import traceback
from bson.objectid import ObjectId
from sub.message import check_skip_message
from sub.redis import get_redis_pool, CHANNEL_NAME 
from sub.mongodb import get_collection

logger = logging.getLogger(__name__)




async def consumer_handler(conn: any, db: any, queue: any, CHANNEL_NAME: str):
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
            command = message['msg']
            if command == "start":
                scenario_id = message['data']['scenario_id']
                scenario_id = '64d9bf3caeb91b6a6ef87810' # test code
                scenario = await db.find_one({'_id': ObjectId(scenario_id)})
                # 여기서 시나리오가 이미 동작중일때 예외처리 해야함
                # 시나리오가 동작중이지 않을 때는 반복 조건에 의해서 블럭 아이템을 추가해야 함. 
                # 껐다가 켜도 시나리오가 복구되게 하고 싶은데 당장은 고려하지 않음
                # 고려해야 한다면 어떻게 하면 될까? 
                # 반복 횟수가 명시된 전체 시나리오를 해석해서 반복루트를 작성
                # 근데 껐다 켜면 의미없는거 아닌가..? 작업 복구가 안될거 같은데. 
                # 일단 반복 횟수에 의해서 전체 블럭을 배열로 만들자. 
                # 블럭 조립

            if command == "stop":
                print("stop")
            
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            print("consumer_handler end")


async def process_handler(conn: any, CHANNEL_NAME: str):
    while True:
        try:  # 루프 깨지지 않도록 예외처리
            print("process_handler")
            await asyncio.sleep(0.001)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            print("process_handler end")

async def main():
    conn = await get_redis_pool()
    db = await get_collection('scenario')
    # 수행해야 하는 블럭 정보는 몽고DB를 통해 받아야 함
    # 수행해야 하는 시나리오 정보는 redis의 키를 통해 몽고DB에서 조회해야 함

    try:
        consumer_task = asyncio.create_task(consumer_handler(conn=conn, CHANNEL_NAME=CHANNEL_NAME))
        process_task = asyncio.create_task(process_handler(conn=conn, CHANNEL_NAME=CHANNEL_NAME))

        print("Start task")
        done, pending = await asyncio.wait(
            [process_task, consumer_task], return_when=asyncio.FIRST_COMPLETED,
        )

        print(f"Done task: {done}")

        for task in pending:
            print(f"Canceling task: {task}")
            task.cancel()
    except Exception as e:
        print(e)
        print(traceback.format_exc())


# asyncio.run(main())
