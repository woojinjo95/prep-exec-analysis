import glob
import logging
import os
import re
import time
import traceback
from multiprocessing import Event
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import signal

from scripts.config.constant import RedisDB
from scripts.connection.mongo_db.crud import insert_many_to_mongodb
from scripts.connection.redis_conn import get_value
from scripts.util._timezone import timestamp_to_datetime_with_timezone_str
from scripts.util._signal import run_with_timeout, TimeoutError
from .cpu_info import parse_cpu_info
from .memory_info import parse_memory_info



logger = logging.getLogger('connection')

timezone = get_value('common', 'timezone', db=RedisDB.hardware)


# get cpu and memory info and insert to mongodb
def postprocess(stop_event: Event):
    logger.info(f"start cpu and memory postprocess")

    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', seconds=10)
    scheduler.start()

    while not stop_event.is_set():
        try:
            scheduled_task()
        except Exception as e:
            logger.error(f"cpu and memory postprocess error: {e}")
            logger.warning(traceback.format_exc())
        finally:
            time.sleep(10)

    scheduler.shutdown()
    logger.info(f"finish cpu and memory postprocess")


def scheduled_task():
    try:
        run_with_timeout(get_cpu_usage, 10)  # Assuming a timeout of 10 seconds. Adjust as necessary.
    except TimeoutError as te:
        logger.error(str(te))


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
