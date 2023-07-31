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


# stb 로그에 포함된 타임 데이터 추출
def extract_stb_log_time_data(line: str) -> Union[None, datetime]:
    pattern1 = r'(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})'  # matches "[ 07-24 04:35:29.422" / logcat
    # 탑 로그의 타임스탬프는 콜렉터에서 강제 주입했던거라 사실상 stb 자체의 타임스탬프가 아니라서 넣지 않음.

    match1 = re.search(pattern1, line)

    if match1:
        # Format for pattern1 is "MM-DD HH:MM:SS.sss", so we assume current year
        return datetime.strptime(f"{datetime.now().year}-{match1.group(1)}", "%Y-%m-%d %H:%M:%S.%f")
    else:
        return None
    

# 콜렉터에서 주입한 타임 데이터 추출
def extract_log_collector_time_data(line: str) -> Union[None, datetime]:
    pattern = r'<Collector:\s(\d+\.\d+)>'  # matches "<Collector: 1627096529.422>"
    match = re.search(pattern, line)
    if match:
        return datetime.fromtimestamp(float(match.group(1)))
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

            log_time = extract_log_collector_time_data(line)
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
