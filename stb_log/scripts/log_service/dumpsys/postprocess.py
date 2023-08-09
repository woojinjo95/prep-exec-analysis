import logging
import re
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from typing import Dict

from scripts.config.constant import RedisDB
from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.connection.redis_conn import get_value
from scripts.util._timezone import timestamp_to_datetime_with_timezone_str
from scripts.config.config import get_setting_with_env
from .cpu_info import parse_cpu_info
from .memory_info import parse_memory_info



logger = logging.getLogger('connection')

timezone = get_value('common', 'timezone', db=RedisDB.hardware)


def postprocess(connection_info: Dict):
    logger.info(f"start cpu and memory postprocess")

    scheduler = BlockingScheduler()
    scheduler.add_job(insert_to_db, 'interval', args=[connection_info], seconds=10)
    scheduler.start()


def insert_to_db(connection_info: Dict):
    timeout = get_setting_with_env("DUMPSYS_EXECUTION_TIMEOUT", 20)
    
    cpu_usage = get_cpu_usage(connection_info, timeout)
    memory_usage = get_memory_usage(connection_info, timeout)
    json_data = construct_json_data(cpu_usage, memory_usage)

    logger.info(f'insert {json_data} to db')
    insert_to_mongodb('stb_info', json_data)


def construct_json_data(cpu_usage: float, memory_usage: float) -> Dict:
    cur_time = timestamp_to_datetime_with_timezone_str(time.time(), timezone)
    return {
        'time': re.sub(r'.\d{6}', '', cur_time),
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
    }
 

# return cpu usage (0 ~ 100)
def get_cpu_usage(connection_info: Dict, timeout: float) -> float:
    try:
        cpu_info = parse_cpu_info(connection_info, timeout)
        return float(cpu_info['total'])
    except Exception as err:
        logger.error(err)
        return 0


# return memory usage (0 ~ 100)
def get_memory_usage(connection_info: Dict, timeout: float) -> float:
    try:
        memory_info = parse_memory_info(connection_info, timeout)
        mem_usage_rate = (int(memory_info['Used_RAM'].replace(',', '')) / int(memory_info['Total_RAM'].replace(',', ''))) * 100
        return mem_usage_rate
    except Exception as err:
        logger.error(err)
        return 0
