import glob
import logging
import os
import re
import time
import traceback
from typing import Union, List, Dict
from multiprocessing import Event
import subprocess

from scripts.config.constant import RedisDB
from scripts.connection.mongo_db.crud import insert_many_to_mongodb
from scripts.connection.redis_conn import get_value
from scripts.util._timezone import timestamp_to_datetime_with_timezone_str


logger = logging.getLogger('connection')


log_prefix_pattern = r'<Collector:\s(\d+\.\d+)>'
log_chunk_pattern = r""


timezone = get_value('common', 'timezone', db=RedisDB.hardware)


# get cpu and memory info and insert to mongodb
def postprocess():
    logger.info(f"start cpu and memory postprocess")

    logger.info(f"finish cpu and memory postprocess")


def get_cpu_usage(chunk: str) -> Union[float, None]:
    # 400%cpu  38%user   3%nice  55%sys 300%idle   0%iow   0%irq   4%sirq   0%host
    match = re.search(r"(\d+)%cpu\s+(\d+)%user\s+(\d+)%nice\s+(\d+)%sys\s+(\d+)%idle\s+(\d+)%iow\s+(\d+)%irq\s+(\d+)%sirq\s+(\d+)%host", chunk)
    if match:
        cpu = float(match.group(1))
        user = float(match.group(2))
        nice = float(match.group(3))
        sys = float(match.group(4))
        idle = float(match.group(5))
        iow = float(match.group(6))
        irq = float(match.group(7))
        sirq = float(match.group(8))
        host = float(match.group(9))
        
        total = cpu
        usage = total - idle
        usage_rate = usage / total
        return usage_rate
    else:
        return None
