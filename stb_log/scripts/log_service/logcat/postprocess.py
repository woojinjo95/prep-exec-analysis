import glob
import logging
import os
import re
import time
import traceback
from datetime import datetime
from multiprocessing import Event
from typing import Dict, List, Tuple, Union

from scripts.connection.mongo_db.crud import insert_many_to_mongodb
from scripts.util._timezone import get_utc_datetime
from .db_connection import LogManagerDBConnection
from scripts.config.mongo import get_scenario_id

logger = logging.getLogger('logcat')

db_conn = LogManagerDBConnection()

log_prefix_pattern = r'<Collector:\s(\d+\.\d+)>'
log_chunk_pattern = r"\[\s(?P<timestamp>\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*(?P<pid>\d+)\s*:\s*(?P<tid>\d+)\s*(?P<log_level>[\w])\/(?P<module>.*)\s*\]\n(?P<message>.*)"


def postprocess(log_type: str, stop_event: Event):
    logger.info(f"start log postprocess")
    completed_log_dir = os.path.join('datas', 'stb_logs', log_type, 'completed_logs')
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


def parse_log_chunk(chunk: str) -> Dict:
    match = re.search(log_chunk_pattern, chunk, re.DOTALL)  # re.DOTALL: include \n
    if match:
        return match.groupdict()
    else:
        return None


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

    for index, (chunk, log_time) in enumerate(LogChunkGenerator(file_path, log_prefix_pattern)):
        if chunk.isspace():
            continue

        # parse log line
        parsed_chunk = parse_log_chunk(chunk)
        if not parsed_chunk:
            logger.warning(f'Invalid log chunk: {chunk}')
            continue

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
            batches.append({
                **parsed_chunk,
                'timestamp': last_time.timestamp(),
            })

    yield batches


def insert_to_db(file_path: str):
    scenario_id = get_scenario_id()
    json_datas = []
    for log_batch in LogBatchGenerator(file_path):
        try:
            json_datas.append(construct_json_data(log_batch, scenario_id))
        except Exception as err:
            logger.warning(f'error in construct_json_data. Cause => {err}')
    try:
        insert_many_to_mongodb('stb_log', json_datas)
        logger.info(f'insert {len(json_datas)} datas to db')
    except Exception as err:
        logger.warning(f'error in insert_many_to_mongodb. Cause => {err}')


def construct_json_data(log_batch: List[Tuple[float, str]], scenario_id: str) -> Dict:
    return {
        'scenario_id': scenario_id,
        'timestamp': get_utc_datetime(log_batch[0]['timestamp'], remove_float_point=True),
        'lines': [{
            'timestamp': get_utc_datetime(log_chunk['timestamp']),
            'module': str(log_chunk['module']).rstrip().replace('\n', ' '),
            'log_level': log_chunk['log_level'],
            'process_name': log_chunk['pid'],
            'pid': log_chunk['pid'],
            'tid': log_chunk['tid'],
            'message': str(log_chunk['message']).rstrip().replace('\n', ' ') if log_chunk['message'] else '',
        } for log_chunk in log_batch],
    }
 