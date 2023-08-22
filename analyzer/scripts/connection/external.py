from typing import Dict
import time
import json

from scripts.connection.redis_conn import get_value
from scripts.util._timezone import get_utc_datetime
from scripts.config.constant import RedisDB, RedisChannel
from scripts.connection.redis_conn import get_strict_redis_connection
from scripts.connection.redis_pubsub import publish


def get_scenario_info() -> Dict:
    return {
        'scenario_id': get_value('testrun', 'scenario_id', '', db=RedisDB.hardware),
        'testrun_id': get_value('testrun', 'id', '', db=RedisDB.hardware),
    }


def construct_report_data() -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time()),
    }


def load_input() -> Dict:
    # load data format to db
    data = {
        "path": "/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-18T163309F381036+0900_1800.mp4",
        "stat_path": "/app/workspace/testruns/2023-08-14T054428F718593/raw/videos/video_2023-08-18T163309F381036+0900_1800.mp4_stat",
    }
    with open(data['stat_path'], 'r') as f:
        json_data = json.load(f)
    return {
        'video_path': data['path'],
        'json_data': json_data
    }


def publish_msg(data: Dict, msg: str, level: str = 'info'):
    with get_strict_redis_connection(RedisDB.hardware) as src:
        publish(src, RedisChannel.command, {
            'data': data,
            'msg': msg,
            'level': level,
        })