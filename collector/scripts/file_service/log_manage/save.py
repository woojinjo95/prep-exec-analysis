import logging
import os
import time
import traceback
import glob
import re
from datetime import datetime
from typing import Union

from scripts.file_service.log_manage.db_connection import LogManagerDBConnection


logger = logging.getLogger('connection')

db_conn = LogManagerDBConnection()


def save():
    completed_log_dir = 'completed_logs'
    os.makedirs(completed_log_dir, exist_ok=True)

    while True:
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


def extract_time_data(line: str) -> Union[None, datetime]:
    pattern1 = r'(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})'  # matches "[ 07-24 04:35:29.422"
    pattern2 = r'Timestamp\s:\s(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{6})'  # matches "Timestamp : 2023-07-11 18:28:41.105968"

    match1 = re.search(pattern1, line)
    match2 = re.search(pattern2, line)

    if match1:
        # Format for pattern1 is "MM-DD HH:MM:SS.sss", so we assume current year
        return datetime.strptime(f"{datetime.now().year}-{match1.group(1)}", "%Y-%m-%d %H:%M:%S.%f")
    elif match2:
        # Format for pattern2 is "YYYY-MM-DD HH:MM:SS.ssssss"
        return datetime.strptime(match2.group(1), "%Y-%m-%d %H:%M:%S.%f")
    else:
        return None


# Return [(time, log_line),...]
# Raise: skip this file
def LogDataGenerator(file_path: str, batch_size: int = 1000, no_time_count_limit: int = 10000):
    last_time = None
    batches = []
    no_time_count = 0

    with open(file_path, 'rb') as f:
        for index, line in enumerate(f.readlines()):
            line = line.decode('utf-8')
            if line.isspace():
                continue

            log_time = extract_time_data(line)
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
        # db_conn.save_data(log_batch)

    # db_conn.save_data((time.time(), log_line))
