from typing import Dict
import time

from scripts.connection.redis_conn import get_value
from scripts.util._timezone import get_utc_datetime
from scripts.config.constant import RedisDB
from scripts.format import ReportData


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
