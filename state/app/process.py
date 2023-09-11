import asyncio
import json
import logging
import time
import traceback
from datetime import datetime
from enum import Enum

from db import CHANNEL_NAME, get_collection, get_redis_pool

logger = logging.getLogger(__name__)


class ServiceStateEnum(Enum):
    idle = "idle"
    streaming = "streaming"
    playblock = "playblock"
    analysis = "analysis"
    recording = "recording"


async def update_log_level_finder_to_scenario(scenario_id: str, testrun_id: str, measure_target_dict: dict):
    try:
        mongo_client = get_collection('scenario')
        doc = mongo_client.find_one({'id': scenario_id})
        testruns = doc.get('testruns', [])
        index = next((i for i, item in enumerate(testruns) if item.get('id') == testrun_id), None)

        # Fetch the existing 'measure_targets' list from MongoDB
        testrun = testruns[index]
        existing_measure_targets = testrun.get('measure_targets', [])
        # Check if an item with the same type exists
        for i, target in enumerate(existing_measure_targets):
            if target.get('type') == measure_target_dict['type']:
                # Update the item if it exists
                update_query = {f'testruns.{index}.measure_targets.{i}': measure_target_dict}
                mongo_client.update_one({'id': scenario_id}, {'$set': update_query})
                break
        # If not found, append the new element
        else:
            update_query = {f'testruns.{index}.measure_targets': measure_target_dict}
            mongo_client.update_one({'id': scenario_id}, {'$push': update_query})

        update_query = {
            f'testruns.{index}.last_updated_timestamp': measure_target_dict['timestamp']
        }
        res = mongo_client.update_one({'id': scenario_id}, {'$set': update_query})

        acknowledged = res.acknowledged
        upserted_id = res.upserted_id  # This will be None if no document was inserted

        return acknowledged, upserted_id

    except Exception as e:
        return False, str(e)


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
                await asyncio.sleep(0.01)
                command_data = raw.get('data', None) if raw else None
                data = json.loads(command_data) if isinstance(command_data, str) else {}
                msg = data.get('msg', None)

                # 레코딩을 시작했을 때
                if msg == 'recording_response':
                    print(f'----> {msg}')
                    # 스트리밍 중단 메세지 전송
                    await pub_msg(conn, msg="streaming", data={"action": "stop"})

                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.recording)

                    # 레코딩이 끝났을 때
                    if data.get('data', {}).get('video_info', {}).get('error', None) is None:
                        # 상태 변경 및 메세지 전송
                        await set_service_state_and_pub(conn, ServiceStateEnum.idle)

                        # 컬러레퍼런스 분석 메세지 전송
                        await pub_msg(conn, msg="analysis", data={"measurement": ["color_reference"]})

                # 분석이 종료되었을 때
                if msg == 'end_analysis':
                    print(f'----> {msg}')
                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.idle)

                # 분석이 시작되었을 때
                if msg == 'start_analysis_response':
                    print(f'----> {msg}')
                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.analysis)

                # 플레이블럭이 시작했을 때
                if msg == 'start_playblock_response':
                    print(f'----> {msg}')
                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.playblock)

                # 액션 페이지에서 분석 페이지에 진입했을때(수동, 자동)
                if msg == 'analysis_mode_init' or msg == 'end_playblock':
                    print(f'----> {msg}')
                    # 로그수집 중단 메세지 전송
                    await pub_msg(conn, msg="stb_log", data={"control": "stop"})

                    # 패킷 캡쳐 중단 메세지 전송
                    await pub_msg(conn, msg="packet_capture", data={"action": "stop"})

                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.idle)

                    # 레코딩 시작 메세지 전송
                    msg_data = data.get('data', {})
                    await pub_msg(conn, msg="recording", data={"start_time": msg_data.get('start_time', 0),
                                                               "end_time":  msg_data.get('end_time', 0)})

                # 메인 페이지에서 분석 페이지에 진입했을때(수동)
                if msg == 'analysis_mode':
                    print(f'----> {msg}')
                    # 로그수집 중단 메세지 전송
                    await pub_msg(conn, msg="stb_log", data={"control": "stop"})

                    # 패킷 캡쳐 중단 메세지 전송
                    await pub_msg(conn, msg="packet_capture", data={"action": "stop"})

                    # 스트리밍 중단 메세지 전송
                    await pub_msg(conn, msg="streaming", data={"action": "stop"})

                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.idle)

                # 액션 페이지에 진입했을때(수동)
                if msg == 'action_mode':
                    print(f'----> {msg}')
                    # 분석 중단 메세지 전송
                    await pub_msg(conn, msg="analysis_terminate", data={})

                    # 로그수집 시작 메세지 전송
                    await pub_msg(conn, msg="stb_log", data={"control": "start"})

                    # 패킷 캡쳐 시작 메세지 전송
                    await pub_msg(conn, msg="packet_capture", data={"action": "start"})

                    # 스트리밍 시작 메세지 전송
                    await pub_msg(conn, msg="streaming", data={"action": "start"})

                    # 상태 변경 및 메세지 전송
                    await set_service_state_and_pub(conn, ServiceStateEnum.streaming)

                # 분석 시작
                if msg == 'analysis':
                    print(f'----> {msg}')
                    msg_data = data.get('data', {})
                    measurement = msg_data.get('measurement', [])

                    # 마지막 측정결과 갱신
                    if ('loudness' in measurement
                            or 'monkey_test' in measurement
                            or 'log_level_finder' in measurement
                            or 'intelligent_monkey_test' in measurement):  # TODO 모듈에서 하지 않는 걸로
                        testrun_id = await conn.hget("testrun", "id")
                        scenario_id = await conn.hget("testrun", "scenario_id")
                        await update_log_level_finder_to_scenario(scenario_id, testrun_id,
                                                                  {'type': measurement[0],
                                                                   'timestamp': datetime.utcfromtimestamp(time.time())})

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
