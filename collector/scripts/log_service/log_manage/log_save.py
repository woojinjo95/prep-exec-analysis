import logging
import os
import time
import traceback
import glob
import re
from datetime import datetime
from typing import Union
from multiprocessing import Event

from .db_connection import LogManagerDBConnection


logger = logging.getLogger('connection')

db_conn = LogManagerDBConnection()
completed_log_dir = os.path.join('datas', 'stb_logs', 'completed_logs')
log_prefix_pattern = r'<Collector:\s(\d+\.\d+)>'

def save(stop_event: Event):
    logger.info(f"start log save")
    os.makedirs(completed_log_dir, exist_ok=True)

    while not stop_event.is_set():
        try:
            file_paths = sorted(glob.glob(os.path.join(completed_log_dir, '*.log')))
            if len(file_paths) > 0:
                save_log(file_paths[0])
        except Exception as e:
            logger.info(traceback.format_exc())
        finally:
            time.sleep(1)


def save_log(file_path: str):
    try:
        with open(file_path, 'rb') as f:
            logger.info(f'{file_path} try to save.')
            ##### Save log here
            insert_to_db(file_path)
            #####
            logger.info(f'{file_path} save complete.')
    except Exception as e:
        logger.info(traceback.format_exc())
    finally:
        os.remove(file_path)
        logger.info(f'{file_path} remove complete.')


def read_file_with_delimiter(filename, delimiter_pattern):
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
def LogDataGenerator(file_path: str, batch_size: int = 1000, no_time_count_limit: int = 10000):
    last_time = None
    batches = []
    no_time_count = 0

    for index, (line, log_time) in enumerate(read_file_with_delimiter(file_path, log_prefix_pattern)):
        if line.isspace():
            continue
        # print(f'index {index}\nline {line}\nlog_time {log_time}')
        
        if log_time is not None:  # time is in line
            last_time = log_time  # store
            no_time_count = 0
        else:
            no_time_count += 1
            if no_time_count > no_time_count_limit:  # too many no time data in lines
                raise Exception(f'No time data in {file_path} at line {index}')
        
        if last_time is not None:
            batches.append((last_time.timestamp(), line))

        if len(batches) >= batch_size:
            yield batches
            batches = []
    yield batches


def insert_to_db(file_path: str):
    for log_batch in LogDataGenerator(file_path):
        # print(log_batch)
        db_conn.save_datas(log_batch)
