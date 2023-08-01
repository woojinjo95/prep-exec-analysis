import logging
import os
import time
import traceback
import glob
import re
from datetime import datetime
from typing import Union, Tuple
from multiprocessing import Event

from .db_connection import LogManagerDBConnection


logger = logging.getLogger('connection')

db_conn = LogManagerDBConnection()
completed_log_dir = os.path.join('datas', 'stb_logs', 'completed_logs')
log_prefix_pattern = r'<Collector:\s(\d+\.\d+)>'


def postprocess(stop_event: Event):
    logger.info(f"start log postprocess")
    os.makedirs(completed_log_dir, exist_ok=True)

    while not stop_event.is_set():
        try:
            file_paths = sorted(glob.glob(os.path.join(completed_log_dir, '*.log')))
            if len(file_paths) > 0:
                postprocess_log(file_paths[0])
        except Exception as e:
            logger.info(traceback.format_exc())
        finally:
            time.sleep(1)


def postprocess_log(file_path: str):
    try:
        with open(file_path, 'rb') as f:
            logger.info(f'{file_path} try to postprocess.')
            insert_to_db(file_path)
            logger.info(f'{file_path} postprocess complete.')
    except Exception as e:
        logger.info(traceback.format_exc())
    finally:
        os.remove(file_path)
        logger.info(f'{file_path} remove complete.')


def LogChunkGenerator(filename, delimiter_pattern) -> Tuple[str, Union[datetime, None]]:
    with open(filename, 'r') as f:
        buf = ""
        while True:
            match = re.search(delimiter_pattern, buf)
            if match:
                pos = match.start()
                time_data = datetime.fromtimestamp(float(match.group(1)))
                yield buf[:pos], time_data
                buf = buf[match.end():]
            else:
                chunk = f.read(4096)
                if not chunk:
                    # end of file
                    yield buf, None
                    break
                buf += chunk


# Return [(time, log_line),...]
# Raise: skip this file
def LogBatchGenerator(file_path: str, no_time_count_limit: int = 10000):
    last_time = None
    batches = []
    no_time_count = 0

    for index, (line, log_time) in enumerate(LogChunkGenerator(file_path, log_prefix_pattern)):
        if line.isspace():
            continue
        # print(f'index {index}\nline {line}\nlog_time {log_time}')
        
        if log_time is not None:  # time data exist in line
            if last_time is not None and int(log_time.timestamp()) != int(last_time.timestamp()): 
                # when the integer part of the timestamp (the seconds) changes,
                # yield the current batch and start a new one
                yield batches
                batches = []
            last_time = log_time  # store the last time
            no_time_count = 0
        else:
            no_time_count += 1
            if no_time_count > no_time_count_limit:  # too many no time data in lines
                raise Exception(f'No time data in {file_path} at line {index}')
        
        if last_time is not None:
            batches.append((last_time.timestamp(), line))

    yield batches


def insert_to_db(file_path: str):
    for log_batch in LogBatchGenerator(file_path):
        # print(log_batch)
        db_conn.save_datas(log_batch)
