import logging
import asyncio
import traceback
from sub.message import check_skip_message
from sub.db import get_db, get_redis_pool, CHANNEL_NAME
from sub.state import is_run_state, set_stop_state, is_analysis_state
from sub.block import run_blocks, run_analysis
from sub.setup import setup_playblock, setup_analysis

logger = logging.getLogger(__name__)


async def consumer_handler(conn: any, db_scenario: any, db_blocks: any, CHANNEL_NAME: str, event: asyncio.Event):
    try:
        pubsub = conn.pubsub()
        await pubsub.subscribe(CHANNEL_NAME)
        while True:
            try:  # 루프 깨지지 않도록 예외처리
                raw = await pubsub.get_message(ignore_subscribe_messages=True)
                await asyncio.sleep(0.01)

                check_skip, message = check_skip_message(raw)
                if not check_skip:
                    continue

                command = message['msg']
                if command == "start_playblock":
                    state = await conn.hgetall("testrun")
                    print(f"state: {state}")
                    if await is_run_state(conn) or await is_analysis_state(conn):
                        # 이미 동작 수행중으로 보이면 추가 실행 명령은 건너뜀
                        print("already running block")
                        continue

                    await setup_playblock(state, db_scenario, db_blocks, conn)

                if command == "start_analysis":
                    if await is_run_state(conn) or await is_analysis_state(conn):
                        # 이미 동작 수행중으로 보이면 추가 실행 명령은 건너뜀
                        print("already running block")
                        continue
                    state = await conn.hgetall("testrun")
                    print(f"state: {state}")
                    await setup_analysis(state, db_scenario, db_blocks, conn)

                if command == "monkey_response" or command == "analysis_response":
                    # 일단 순차적으로 수행할 것이므로 내용물 체크 안함
                    # 여기가 애매하고 문제가 되는 부분.
                    print("response set event ==> {analysis_response}")
                    event.set()

                if command == "stop_playblock" or command == "stop_analysis":
                    await set_stop_state(conn, event)
                    # 또는 여기서 중지하고 동작아이템 정리 해야 함

            except Exception as e:
                print(e)
                print(traceback.format_exc())
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        print("consumer_handler end")


async def process_handler(conn: any, db_blocks: any, CHANNEL_NAME: str, event: asyncio.Event):
    print("process_handler")
    try:
        while True:
            try:  # 루프 깨지지 않도록 예외처리
                await asyncio.sleep(0.01)  # 수행 루프는 1초 단위로
                if await is_run_state(conn):
                    # 상태가 run일때만.
                    testrun_id = await conn.hget("testrun", "id")
                    scenario_id = await conn.hget("testrun", "scenario_id")
                    testrun = db_blocks.find_one({
                        'scenario': scenario_id,
                        'testrun': testrun_id
                    })
                    await run_blocks(conn, db_blocks, scenario_id, testrun_id, testrun['blocks'], event)
                if await is_analysis_state(conn):
                    # 상태가 run일때만.
                    testrun = db_blocks.find_one({
                        'scenario': "analysis",
                        'testrun': "analysis"
                    })
                    print(f"testrun: {testrun}")
                    await run_analysis(conn, db_blocks, "analysis", "analysis", testrun['blocks'], event)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                await set_stop_state(conn, event)
                # 예외발생시 강제 중단 처리
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
