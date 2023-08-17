from typing import Dict
import time

from scripts.connection.redis_conn import get_value
from scripts.util._timezone import get_utc_datetime
from scripts.config.constant import RedisDB
from scripts.format import ReportData


def get_scenario_id() -> str:
    scenario_id = get_value('testrun', 'scenario_id', '', db=RedisDB.hardware)
    return scenario_id


def construct_report_data() -> ReportData:
    return ReportData(
        scenario_id=get_scenario_id(),
        timestamp=get_utc_datetime(time.time()),
    )
