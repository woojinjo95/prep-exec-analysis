import asyncio
import copy
import traceback
from sub.message import cvt_block_to_message, publish_message
from sub.db import CHANNEL_NAME
from sub.state import is_run_state, set_stop_state, set_run_item, is_analysis_state


def calc_scenario_to_run_blocks(total_loop: int, scenario: dict):
    print(f"calc_scenario_to_run_blocks:")
    idx = 0
    blocks = []
    # 수행해야 하는 블럭을 반복조건에 맞춰서 배열로 만드는 단계
    for loop_cnt in range(total_loop):  # 시나리오 전체 루프
        print(f"name: {scenario['name']} loop_cnt: {loop_cnt}, block_group: {scenario['block_group']}")
        for block_group in scenario['block_group']:  # 개별 블록그룹 루프
            print(f"block_group-id: {block_group['id']}, block_group-repeat_cnt: {block_group['repeat_cnt']}")
            # print(f"block_group-repeat_cnt: {block_group['block']}")
            block_group_cnt = block_group['repeat_cnt'] if block_group['repeat_cnt'] > 0 else 1

            for block_loop_idx in range(block_group_cnt):
                for block_item in block_group['block']:  # 그룹내 아이템 루프
                    print(f"block: {idx} / {block_item['name']} block_loop_cnt: {block_loop_idx}")
                    _block_item = copy.deepcopy(block_item)
                    _block_item['run'] = False
                    _block_item['idx'] = idx
                    idx = idx + 1
                    blocks.append(copy.deepcopy(_block_item))
    return blocks


def calc_analysis_to_run_blocks(configs: list):
    idx = 0
    blocks = []
    for config_key in configs.keys():
        config = configs[config_key]
        if config is None:
            continue
        _analysis_config = {
            "type": "analysis",
            "name": config_key,
            "args": [
                {
                    "key": "measurement",
                    "value": config_key
                }
            ]
        }
        _analysis_config['run'] = False
        _analysis_config['idx'] = idx
        idx = idx + 1
        blocks.append(copy.deepcopy(_analysis_config))
    return blocks


async def run_blocks(conn, db_blocks, scenario_id, testrun_id, blocks: list, event: asyncio.Event):
    try:
        for block in blocks:
            # 블럭 수행 도중에 취소되는 경우
            if await is_run_state(conn) is False:
                print("stop running block")
                return
            
            # 다음 수행될 블럭 정보 송신
            await conn.publish(CHANNEL_NAME, publish_message(message="next_playblock", data={"block_id": block['id']}))
            await set_run_item(conn, block_id=block['id'])
            message = cvt_block_to_message(block)
            print(f"run block: {message}")
            # 수행 메시지 송신
            await conn.publish(CHANNEL_NAME, message)

            print("wait... message response")
            try:
                # 몽키테스트는 완료 대기
                print(f"monkey test wait...{block['type']}")
                if block['type'] == 'monkey_test':
                    event.clear()
                    await asyncio.wait_for(event.wait(), 3200)
                    print("monkey test end...")
            except Exception as e:
                print(e)

            # # 다른 파트는 시간대기
            delay_time = block['delay_time']
            await asyncio.sleep(delay_time / 1000)



            # 완료 처리
            db_blocks.update_one(
                {"scenario": scenario_id, "testrun_id": testrun_id, "blocks.idx": block['idx']},
                {"$set": {"blocks.$.run": True}}
            )
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        await set_stop_state(conn, event)
        await conn.publish(CHANNEL_NAME, publish_message("end_playblock"))
        print("run_blocks end")


async def run_analysis(conn, db_blocks, scenario_id, testrun_id, blocks: list, event: asyncio.Event):
    try:
        print("run_analysis")
        for block in blocks:
            # 블럭 수행 도중에 취소되는 경우
            if await is_analysis_state(conn) is False:
                print("stop analysis")
                return
            
            # 다음 수행될 블럭 정보 송신
            await conn.publish(CHANNEL_NAME, publish_message(message="next_analysis", data={"analysis": block['name']}))
            await set_run_item(conn, block_id=block['name'])

            # 수행 메시지 송신
            await conn.publish(CHANNEL_NAME, cvt_block_to_message(block))

            print("wait... message response")
            # 블럭 타입이 분석이면 이벤트 대기
            try:
                await asyncio.wait_for(event.wait(), 60)
            except Exception as e:
                print(e)
            # finally:
                # event.clear()
            # # 다른 파트는 시간대기
            # delay_time = block['delay_time']
            # await asyncio.sleep(delay_time / 1000)

            # 완료 처리
            db_blocks.update_one(
                {"scenario": scenario_id, "testrun_id": testrun_id, "blocks.idx": block['idx']},
                {"$set": {"blocks.$.run": True}}
            )
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        await set_stop_state(conn, event)
        await conn.publish(CHANNEL_NAME, publish_message("end_analysis"))
        print("run_analysis end")
