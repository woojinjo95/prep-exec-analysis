import logging
import re
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from typing import Dict

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.util._timezone import get_utc_datetime
from .cpu_info import parse_cpu_info
from .memory_info import parse_memory_info



logger = logging.getLogger('dumpsys')


def postprocess(connection_info: Dict):
    logger.info(f"start cpu and memory postprocess")

    scheduler = BlockingScheduler()
    scheduler.add_job(insert_to_db, 'interval', args=[connection_info], seconds=30)
    scheduler.start()


def insert_to_db(connection_info: Dict):
    cpu_usage = get_cpu_usage(connection_info, 5)
    memory_usage = get_memory_usage(connection_info, 20)
    json_data = construct_json_data(cpu_usage, memory_usage)

    logger.info(f'insert {json_data} to db')
    insert_to_mongodb('stb_info', json_data)


def construct_json_data(cpu_usage: str, memory_usage: str) -> Dict:
    cur_time = time.time()
    return {
        'timestamp': get_utc_datetime(re.sub(r'.\d{6}', '', str(cur_time))),
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
