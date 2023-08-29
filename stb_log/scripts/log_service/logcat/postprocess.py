import logging
import re
import traceback
import threading
from multiprocessing import Event, Queue
from typing import Dict, List, Tuple

from scripts.connection.mongo_db.crud import insert_to_mongodb
from scripts.util._timezone import get_utc_datetime
from scripts.connection.external import get_scenario_info
from scripts.connection.stb_connection.utils import exec_command

logger = logging.getLogger('logcat')

log_chunk_pattern = r"\[\s(?P<timestamp>\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*(?P<pid>\d+)\s*:\s*(?P<tid>\d+)\s*(?P<log_level>[\w])\/(?P<module>.*)\s*\]\n(?P<message>.*)"


def postprocess(connection_info: Dict, stop_event: Event, queue: Queue):
    logger.info(f"start log postprocess")

    for log_batch in LogBatchGenerator(queue):
        if stop_event.is_set():
            break
        th = threading.Thread(target=process_batch, args=(log_batch, connection_info), daemon=True)
        th.start()

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


def construct_json_data(log_batch: List[Tuple[float, str]], pid_name_dict: Dict[int, str]) -> Dict:
    scenario_info = get_scenario_info()
    return {
        'scenario_id': scenario_info['scenario_id'],
        'testrun_id': scenario_info['testrun_id'],
        'timestamp': get_utc_datetime(log_batch[0]['timestamp'], remove_float_point=True),
        'lines': [{
            'timestamp': get_utc_datetime(log_chunk['timestamp']),
            'module': str(log_chunk['module']).rstrip().replace('\n', ' '),
            'log_level': log_chunk['log_level'],
            'process_name': pid_name_dict.get(int(log_chunk['pid']), ''),
            'pid': log_chunk['pid'],
            'tid': log_chunk['tid'],
            'message': str(log_chunk['message']).rstrip().replace('\n', ' ') if log_chunk['message'] else '',
        } for log_chunk in log_batch],
    }
 

def get_process_names(pids: List[int], connection_info: Dict) -> Dict[int, str]:
    pid_str = '|'.join([str(pid) for pid in pids])
    command = f"ps -A | grep -E '{pid_str}'"
    result = exec_command(command, 2, connection_info)

    lines = result.strip().split("\n")
    pid_name_dict = {}
    for line in lines:
        parts = re.split(r'\s+', line)
        pid = int(parts[1])
        name = parts[-1]
        pid_name_dict[pid] = name
    return pid_name_dict


def process_batch(log_batch: List[Tuple[float, str]], connection_info: Dict):
    try:
        pids = list(set([int(log_chunk['pid']) for log_chunk in log_batch]))
        pid_name_dict = get_process_names(pids, connection_info)
        json_data = construct_json_data(log_batch, pid_name_dict)
        insert_to_mongodb('stb_log', json_data)
        logger.info(f'insert datas to db')
    except Exception as err:
        logger.warning(f'error in insert logcat data to db. Cause => {err}')
