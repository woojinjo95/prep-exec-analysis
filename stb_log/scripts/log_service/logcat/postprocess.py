import logging
import re
import traceback
from multiprocessing import Event, Queue
from typing import Dict, List, Tuple

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.util._timezone import get_utc_datetime
from .db_connection import LogManagerDBConnection
from scripts.config.mongo import get_scenario_id

logger = logging.getLogger('logcat')

db_conn = LogManagerDBConnection()

log_chunk_pattern = r"\[\s(?P<timestamp>\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*(?P<pid>\d+)\s*:\s*(?P<tid>\d+)\s*(?P<log_level>[\w])\/(?P<module>.*)\s*\]\n(?P<message>.*)"


def postprocess(stop_event: Event, queue: Queue):
    logger.info(f"start log postprocess")

    for log_batch in LogBatchGenerator(queue):
        if stop_event.is_set():
            break
        try:
            json_data = construct_json_data(log_batch)
            insert_to_mongodb('stb_log', json_data)
            logger.info(f'insert datas to db')
        except Exception as err:
            logger.warning(f'error in insert. Cause => {err}')
            logger.warning(traceback.format_exc())

    logger.info(f"finish log postprocess")


def parse_log_chunk(chunk: str) -> Dict:
    match = re.search(log_chunk_pattern, chunk, re.DOTALL)  # re.DOTALL: include \n
    if match:
        return match.groupdict()
    else:
        return None


def LogChunkGenerator(queue: Queue) -> Tuple[float, str]:
    while True:
        timestamp, chunk = queue.get()
        yield timestamp, chunk


def LogBatchGenerator(queue: Queue):
    last_time = None
    batches = []

    for log_time, chunk in LogChunkGenerator(queue):
        parsed_chunk = parse_log_chunk(chunk)
        if not parsed_chunk:
            logger.warning(f'Invalid log chunk: {chunk}')
            continue

        if last_time is not None and int(log_time) != int(last_time): 
            yield batches
            batches = []

        batches.append({
            **parsed_chunk,
            'timestamp': log_time,
        })
        
        last_time = log_time


def construct_json_data(log_batch: List[Tuple[float, str]]) -> Dict:
    return {
        'scenario_id': get_scenario_id(),
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
 