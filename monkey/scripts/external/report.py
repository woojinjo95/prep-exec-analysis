from typing import Dict
import time
import logging

from scripts.util._timezone import get_utc_datetime
from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.external.scenario import get_scenario_info
from scripts.format import SmartSenseData

logger = logging.getLogger('main')


def construct_report_data() -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time()),
    }


def report_smart_sense(data: SmartSenseData):
    report = {**construct_report_data(), **data.__dict__}
    logger.info(f'insert smart_sense {report} to db')
    insert_to_mongodb('monkey_smart_sense', report)

