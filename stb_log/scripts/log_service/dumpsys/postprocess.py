import logging
import time
from typing import Dict

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.util._timezone import get_utc_datetime
from scripts.connection.external import get_scenario_info
from .format import CPUInfo, MemoryInfo
from .cpu_info import parse_cpu_info
from .memory_info import parse_memory_info


logger = logging.getLogger('dumpsys')


def postprocess():
    logger.info(f"start dumpsys postprocess")
    while True:
        time.sleep(1)
        try:
            extract_data()
        except Exception as err:
            logger.warning(f'error in extract_data. Cause => {err}')


def extract_data():
    cpu_info = parse_cpu_info()
    memory_info = parse_memory_info()
    json_data = construct_json_data(cpu_info, memory_info)

    logger.info(f'insert {json_data} to db')
    insert_to_mongodb('stb_info', json_data)


def construct_json_data(cpu_info: CPUInfo, memory_info: MemoryInfo) -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time(), remove_float_point=True),
        **cpu_info.__dict__,
        **memory_info.__dict__
    }
 