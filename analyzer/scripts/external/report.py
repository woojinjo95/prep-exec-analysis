from typing import Dict
import time
import logging

from scripts.util._timezone import get_utc_datetime
from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.external.scenario import get_scenario_info

logger = logging.getLogger('connection')


def construct_report_data() -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time()),
    }


def report_output(col_name: str, additional_data: Dict):
    report = {**construct_report_data(), **additional_data}
    logger.info(f'insert {report} to db')
    insert_to_mongodb(col_name, report)
