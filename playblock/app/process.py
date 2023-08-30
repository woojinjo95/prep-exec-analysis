import logging
import asyncio
import traceback
import copy
import json
from datetime import datetime
from sub.message import check_skip_message
from sub.db import get_db, get_redis_pool, CHANNEL_NAME

logger = logging.getLogger(__name__)




async def consumer_handler(conn: any, db_scenario: any, db_blocks: any, CHANNEL_NAME: str):
    try:
        pubsub = conn.pubsub()
        await pubsub.subscribe(CHANNEL_NAME)
        while True:
            try:  # 루프 깨지지 않도록 예외처리
                raw = await pubsub.get_message(ignore_subscribe_messages=True)
                await asyncio.sleep(1)

                check_skip, message = check_skip_message(raw)
                if not check_skip:
                    continue

                command = message['msg']
                if command == "run_scenario":
                    testrun_state = await conn.hgetall("testrun")
                    print(f"state: {testrun_state}")
                    if testrun_state.get('state') == "run":
                        # 이미 동작 수행중으로 보이면 무시함
                        print("already running block")
                        continue

                    testrun_id = testrun_state.get('id')
                    scenario_id = testrun_state.get('scenario_id')
                    scenario = db_scenario.find_one({'id': scenario_id})

                    blocks = []
                    idx = 0
                    total_loop = scenario.get('repeat_cnt') if hasattr(scenario, 'repeat_cnt') else 1
                    # 또는...
                    # total_loop = message['data']['total_loop'] 메시지 파라미터로 처리
                    # 수행해야 하는 블럭을 반복조건에 맞춰서 배열로 만드는 단계
                    for loop_cnt in range(total_loop):  # 시나리오 전체 루프
                        print(f"name: {scenario['name']} loop_cnt: {loop_cnt}")
                        for block_group in scenario['block_group']:  # 개별 블록그룹 루프
                            for block_loop_cnt in range(block_group['repeat_cnt']):
                                for block_item in block_group['block']:  # 그룹내 아이템 루프
                                    _block_item = copy.deepcopy(block_item)
                                    print(f"block: {idx} / {_block_item['name']} block_loop_cnt: {block_loop_cnt}")
                                    _block_item['run'] = False
                                    _block_item['idx'] = idx
                                    idx = idx + 1
                                    blocks.append(copy.deepcopy(_block_item))

                    # 수행할 때마다 테스트런이 증가해야 하지만 현재 증가하지 않으므로 임시로 upsert 사용
                    db_blocks.update_one({
                        "testrun": testrun_id,
                        "scenario": scenario_id,
                        "blocks": blocks
                    }, {'$set': {
                        "testrun": testrun_id,
                        "scenario": scenario_id
                    }}, upsert=True)

                    # 동작 상태를 run으로 설정함
                    await conn.hset("testrun", "state", "run")

                if command == "stop_scenario":
                    await conn.hset("testrun", "state", "stop")
                    # 또는 여기서 중지하고 동작아이템 정리 해야 함
                    print("stop")

            except Exception as e:
                print(e)
                print(traceback.format_exc())
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print("consumer_handler end")


async def process_handler(conn: any, db_blocks: any, CHANNEL_NAME: str):
    print("process_handler")
    try:
        while True:
            try:  # 루프 깨지지 않도록 예외처리
                await asyncio.sleep(1)  # 수행 루프는 1초 단위로
                state = await conn.hget("testrun", "state")
                if state == "run":
                    # 상태가 run일때만.
                    testrun_id = await conn.hget("testrun", "id")
                    scenario_id = await conn.hget("testrun", "scenario_id")
                    testrun = db_blocks.find_one({
                        'scenario': scenario_id,
                        'testrun': testrun_id
                    })
                    for block in testrun['blocks']:
                        state = await conn.hget("testrun", "state")
                        print(f"state: {state}")
                        if state == "stop":
                            # 이미 동작 수행중으로 보이면 무시함
                            print("stop running block")
                            break
                        print(f"block ==> {block}")
                        # 여기서 블럭 메시지 수행하면 됨.
                        # 메시지 송신 -> 일단은 리모콘 메시지 1종만 추후 메시지 추가
                        message = {
                            "msg": "debug_remocon_transmit",
                            "level": "info",
                            "data": {},
                            "service": "playblock",
                            "time": datetime.utcnow().timestamp()
                        }
                        message['msg'] = block['type']
                        message['msg'] = "debug_remocon_transmit",
                        for arg in block['args']:
                            message['data'][arg['key']] = arg['value']
                        
                        dumps_message = json.dumps(message)
                        await conn.publish(CHANNEL_NAME, dumps_message)
                        # 여기서 대기 (원래는 여기서 작업완료 (보낸 명령에 대한)대기)
                        delay_time = block['delay_time']
                        await asyncio.sleep(delay_time / 1000)
                        print("wait... message response")
                        # 완료 처리
                        db_blocks.update_one(
                            {"scenario": scenario_id, "blocks.idx": block['idx']},
                            {"$set": {"blocks.$.run": True}}
                        )
                    await conn.hset("testrun", "state", "stop")
            except Exception as e:
                print(e)
                print(traceback.format_exc())
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print("process_handler end")


async def main():
    conn = await get_redis_pool()
    _mongodb = get_db()
    db_scenario = _mongodb['scenario']
    db_blocks = _mongodb['blockrun']
    # 수행해야 하는 블럭 정보는 몽고DB를 통해 받아야 함
    # 수행해야 하는 시나리오 정보는 redis의 키를 통해 몽고DB에서 조회해야 함

    try:
        consumer_task = asyncio.create_task(consumer_handler(conn=conn, db_scenario=db_scenario, db_blocks=db_blocks, CHANNEL_NAME=CHANNEL_NAME))
        process_task = asyncio.create_task(process_handler(conn=conn, db_blocks=db_blocks, CHANNEL_NAME=CHANNEL_NAME))

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


asyncio.run(main())
