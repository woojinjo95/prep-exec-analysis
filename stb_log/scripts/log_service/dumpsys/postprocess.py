import logging
import re
import time
import traceback
from multiprocessing import Event
from apscheduler.schedulers.blocking import BlockingScheduler
from typing import Dict

from scripts.config.constant import RedisDB
from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.connection.redis_conn import get_value
from scripts.util._timezone import timestamp_to_datetime_with_timezone_str
from scripts.util._signal import run_with_timeout, TimeoutError
from .cpu_info import parse_cpu_info
from .memory_info import parse_memory_info



logger = logging.getLogger('connection')

timezone = get_value('common', 'timezone', db=RedisDB.hardware)


def postprocess():
    logger.info(f"start cpu and memory postprocess")

    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_task, 'interval', seconds=10)
    scheduler.start()


def scheduled_task():
    try:
        run_with_timeout(insert_to_db, 10)
    except TimeoutError as te:
        logger.error(str(te))


def insert_to_db():
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
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
def get_cpu_usage() -> float:
    try:
        cpu_info = parse_cpu_info()
        return float(cpu_info['total'])
    except Exception as err:
        logger.error(err)
        return 0


# return memory usage (0 ~ 100)
def get_memory_usage() -> float:
    try:
        memory_info = parse_memory_info()
        mem_usage_rate = (int(memory_info['Used_RAM'].replace(',', '')) / int(memory_info['Total_RAM'].replace(',', ''))) * 100
        return mem_usage_rate
    except Exception as err:
        logger.error(err)
        return 0
