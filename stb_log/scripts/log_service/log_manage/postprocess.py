import logging
import os
import time
import traceback
import glob
import re
from datetime import datetime
from typing import Union, Tuple, List, Dict
from multiprocessing import Event

from .db_connection import LogManagerDBConnection
from scripts.connection.mongo_db.crud import insert_to_mongodb


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
    logger.info(f"finish log postprocess")


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
        logger.info(f'insert {len(log_batch)} datas to db')

        json_data = construct_json_data(log_batch)
        # write_json(f'stb_log_{datetime.fromtimestamp(log_batch[0][0]).strftime("%Y-%m-%d %H:%M:%S")}.json', json_data)
        insert_to_mongodb('stb_log', json_data)


def construct_json_data(log_batch: List[Tuple[float, str]]) -> Dict:
    return {
        'time': int(log_batch[0][0]),  # first log time(second) in batch
        'readable_time': datetime.fromtimestamp(log_batch[0][0]).strftime('%Y-%m-%d %H:%M:%S'),  # first log time in batch
        'lines': [{
            'time': time_data,
            'raw': line,
        } for time_data, line in log_batch],
    }
