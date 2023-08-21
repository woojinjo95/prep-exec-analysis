import logging
import asyncio
import traceback
import copy
import json
import datetime
from sub.message import check_skip_message
from playblock.app.sub.db import get_redis_pool, CHANNEL_NAME
from sub.db import get_collection

logger = logging.getLogger(__name__)


async def consumer_handler(conn: any, db_scenario: any, db_blocks: any, CHANNEL_NAME: str):
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
            if command == "run_scenario":
                state = await conn.hget("testrun", "state")
                if state == "run" or state is None:
                    # 이미 동작 수행중으로 보이면 무시함
                    print("already running block")
                    continue

                scenario_id = message['data']['scenario_id']
                scenario_id = '5e731960-616a-436e-9cad-84fdbb39bbf4'  # test code

                testrun_id = message['data']['testrun_id']
                testrun_id = '2023-08-14T054428F718593'  # test code
                res = await db_scenario.find_one({'id': scenario_id})

                blocks = []
                idx = 0
                total_loop = res['repeat_cnt'] if hasattr(res, 'repeat_cnt') else 3
                # 또는...
                # total_loop = message['data']['total_loop'] 메시지 파라미터로 처리
                for loop_cnt in range(total_loop):  # 시나리오 전체 루프
                    print(f"name: {res['name']} loop_cnt: {loop_cnt}")
                    for block_group in res['block_group']:  # 개별 블록그룹 루프
                        for block_loop_cnt in range(block_group['repeat_cnt']):
                            for block_item in block_group['block']:  # 그룹내 아이템 루프
                                _block_item = copy.deepcopy(block_item)
                                print(f"block: {idx} / {_block_item['name']} block_loop_cnt: {block_loop_cnt}")
                                _block_item['run'] = False
                                _block_item['idx'] = idx
                                idx = idx + 1
                                blocks.append(copy.deepcopy(_block_item))

                await db_blocks.insert_one({
                    "testrun": testrun_id,
                    "scenario": scenario_id,
                    "blocks": blocks
                })

                # 동작 상태를 run으로 설정함
                await conn.hset("testrun", "state", "run")

            if command == "stop":
                await conn.hset("testrun", "state", "stop")
                # 또는 여기서 중지하고 동작아이템 정리 해야 함
                print("stop")

        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            print("consumer_handler end")


async def process_handler(conn: any, db_blocks: any, CHANNEL_NAME: str):
    while True:
        try:  # 루프 깨지지 않도록 예외처리
            print("process_handler")
            state = await conn.hget("testrun", "state")
            if state == "run":
                # 상태가 run일때만.
                testrun_id = await conn.hget("testrun", "id")
                scenario_id = await conn.hget("testrun", "scenario_id")
                testrun = db_blocks.find_one({
                    'scenario': scenario_id,
                    'testrun': testrun_id
                })
                for block in testrun:
                    print(block)
                    # 여기서 블럭 메시지 수행하면 됨.
                    # 메시지 송신 -> 일단은 리모콘 메시지 1종만
                    message = json.dumps({
                        "msg": "remocon_transmit",
                        "level": "info",
                        "data": {},
                        "service": "playblock",
                        "time": datetime.now()
                    })
                    for arg in block['args']:
                        message['data'][arg['key']] = arg['value']
                    await conn.publish(CHANNEL_NAME, message)
                    # 여기서 대기 (원래는 여기서 작업완료 (보낸 명령에 대한)대기)
                    delay_time = block['deplay_time']
                    await asyncio.sleep(delay_time / 1000)
                    print("wait... message response")
                    # 완료 처리
                    db_blocks.update_one(
                        {"scenario": scenario_id, "blocks.idx": block['idx']},
                        {"$set": {"blocks.$.run": True}}
                    )
            await asyncio.sleep(1)  # 수행 루프는 1초 단위로
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
