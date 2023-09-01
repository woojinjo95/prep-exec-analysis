import logging
import asyncio
import traceback
import copy
import json
from datetime import datetime
from sub.message import check_skip_message
from sub.db import get_db, get_redis_pool, CHANNEL_NAME

logger = logging.getLogger(__name__)


async def set_run_state(redis_connection):
    print("run_scenario")
    await redis_connection.hset("testrun", "state", "run")
    await redis_connection.publish(CHANNEL_NAME, publish_message("start_playblock_response"))


async def is_run_state(redis_connection):
    state = await redis_connection.hget("testrun", "state") == "run"
    print(f"scenario = {state}")
    return state


async def set_stop_state(redis_connection):
    print("stop_scenario")
    await redis_connection.hset("testrun", "state", "stop")
    await redis_connection.publish(CHANNEL_NAME, publish_message("stop_playblock_response"))


def calc_scenario_to_run_blocks(total_loop: int, scenario: dict):
    idx = 0
    blocks = []
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
    return blocks


def calc_analysis_to_run_blocks(analysis_configs: list):
    idx = 0
    blocks = []
    for analysis_config in analysis_configs:
        _analysis_config = {
            "type": "analysis",
            "args": [
                {
                    "key": "measurement",
                    "value": analysis_config
                }
            ]
        }
        _analysis_config['run'] = False
        _analysis_config['idx'] = idx
        idx = idx + 1
        blocks.append(copy.deepcopy(_analysis_config))


async def consumer_handler(conn: any, db_scenario: any, db_blocks: any, CHANNEL_NAME: str, event: asyncio.Event):
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
                if command == "start_playblock":
                    testrun_state = await conn.hgetall("testrun")
                    print(f"state: {testrun_state}")
                    if await is_run_state(conn):
                        # 이미 동작 수행중으로 보이면 추가 실행 명령은 건너뜀
                        print("already running block")
                        continue

                    testrun_id = testrun_state.get('id')
                    scenario_id = testrun_state.get('scenario_id')
                    scenario = db_scenario.find_one({'id': scenario_id})

                    total_loop = scenario.get('repeat_cnt') if hasattr(scenario, 'repeat_cnt') else 1
                    blocks = calc_scenario_to_run_blocks(total_loop, scenario)

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
                    await set_run_state(conn)

                if command == "start_analysis":
                    analysis_configs = await conn.keys("analysis_config:*")
                    print(f"state: {analysis_configs}")
                    if await is_run_state(conn):
                        # 이미 동작 수행중으로 보이면 추가 실행 명령은 건너뜀
                        print("already running block")
                        continue

                    blocks = calc_analysis_to_run_blocks(analysis_configs)

                    # 수행할 때마다 테스트런이 증가해야 하지만 현재 증가하지 않으므로 임시로 upsert 사용
                    db_blocks.update_one({
                        "testrun": "analysis",
                        "scenario": "analysis",
                        "blocks": blocks
                    }, {'$set': {
                        "testrun": "analysis",
                        "scenario": "analysis",
                    }}, upsert=True)

                    # 동작 상태를 run으로 설정함
                    await set_run_state(conn)
                if command == "start_analysis_response" or command == "remocon_response":
                    # 일단 순차적으로 수행할 것이므로 내용물 체크 안함
                    event.set()

                if command == "stop_playblock" or command == "stop_analysis":
                    await set_stop_state(conn)
                    # 또는 여기서 중지하고 동작아이템 정리 해야 함

            except Exception as e:
                print(e)
                print(traceback.format_exc())
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print("consumer_handler end")


def publish_message(message: str, data: dict = dict()):
    return json.dumps({
        "msg": message,
        "level": "info",
        "data": data,
        "service": "playblock",
        "time": datetime.utcnow().timestamp()
    })


def cvt_block_to_message(block: dict):
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
    # message['msg'] = "debug_remocon_transmit",
    for arg in block['args']:
        message['data'][arg['key']] = arg['value']

    return json.dumps(message)


async def run_blocks(conn, db_blocks, scenario_id, blocks: list, event: asyncio.Event):
    try:
        for block in blocks:
            # 블럭 수행 도중에 취소되는 경우
            if await is_run_state(conn) is False:
                print("stop running block")
                return
            # 다음 수행될 블럭 정보 송신
            await conn.publish(CHANNEL_NAME, publish_message(message="next_playblock", data={"block_id": block['id']}))

            # 수행 메시지 송신
            await conn.publish(CHANNEL_NAME, cvt_block_to_message(block))

            print("wait... message response")
            # 블럭 타입이 분석이면 이벤트 대기

            await event.wait()
            # # 다른 파트는 시간대기
            # delay_time = block['delay_time']
            # await asyncio.sleep(delay_time / 1000)

            # 완료 처리
            db_blocks.update_one(
                {"scenario": scenario_id, "blocks.idx": block['idx']},
                {"$set": {"blocks.$.run": True}}
            )
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        await set_stop_state(conn)
        await conn.publish(CHANNEL_NAME, publish_message("end_playblock"))
        print("run_blocks end")


async def process_handler(conn: any, db_blocks: any, CHANNEL_NAME: str, event: asyncio.Event):
    print("process_handler")
    try:
        while True:
            try:  # 루프 깨지지 않도록 예외처리
                await asyncio.sleep(1)  # 수행 루프는 1초 단위로
                if await is_run_state(conn):
                    # 상태가 run일때만.
                    testrun_id = await conn.hget("testrun", "id")
                    scenario_id = await conn.hget("testrun", "scenario_id")
                    testrun = db_blocks.find_one({
                        'scenario': scenario_id,
                        'testrun': testrun_id
                    })
                    await run_blocks(conn, db_blocks, scenario_id, testrun['blocks'], event)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
            # finally:
            #     await set_stop_state(conn)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print("process_handler end")


async def main():
    event = asyncio.Event()
    conn = await get_redis_pool()
    _mongodb = get_db()
    db_scenario = _mongodb['scenario']
    db_blocks = _mongodb['blockrun']
    # 수행해야 하는 블럭 정보는 몽고DB를 통해 받아야 함
    # 수행해야 하는 시나리오 정보는 redis의 키를 통해 몽고DB에서 조회해야 함

    try:
        consumer_task = asyncio.create_task(consumer_handler(
            conn=conn, db_scenario=db_scenario, db_blocks=db_blocks, CHANNEL_NAME=CHANNEL_NAME, event=event))
        process_task = asyncio.create_task(process_handler(
            conn=conn, db_blocks=db_blocks, CHANNEL_NAME=CHANNEL_NAME, event=event))

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
