import logging
import time
from typing import Dict

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.util._timezone import get_utc_datetime
from scripts.connection.external import get_scenario_info
from .cpu_info import parse_cpu_info
from .memory_info import parse_memory_info


logger = logging.getLogger('dumpsys')


def postprocess(connection_info: Dict):
    logger.info(f"start cpu and memory postprocess")
    while True:
        time.sleep(30)
        try:
            insert_to_db(connection_info)
        except Exception as err:
            logger.warning(f'error in insert dumpsys data to db. Cause => {err}')


def insert_to_db(connection_info: Dict):
    cpu_usage = get_cpu_usage(connection_info, 5)
    memory_usage = get_memory_usage(connection_info, 20)
    json_data = construct_json_data(cpu_usage, memory_usage)

    logger.info(f'insert {json_data} to db')
    insert_to_mongodb('stb_info', json_data)


def construct_json_data(cpu_usage: str, memory_usage: str) -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(time.time(), remove_float_point=True),
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
    }
 

# return cpu usage (0 ~ 100)
def get_cpu_usage(connection_info: Dict, timeout: float) -> str:
    try:
        cpu_info = parse_cpu_info(connection_info, timeout)
        return str(cpu_info['total'])
    except Exception as err:
        logger.error(err)
        return ''


# return memory usage (0 ~ 100)
def get_memory_usage(connection_info: Dict, timeout: float) -> str:
    try:
        memory_info = parse_memory_info(connection_info, timeout)
        mem_usage_rate = (int(memory_info['Used_RAM'].replace(',', '')) / int(memory_info['Total_RAM'].replace(',', ''))) * 100
        return str(mem_usage_rate)
    except Exception as err:
        logger.error(err)
        return ''
