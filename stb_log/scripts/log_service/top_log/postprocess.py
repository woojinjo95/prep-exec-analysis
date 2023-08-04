import glob
import logging
import os
import re
import time
import traceback
from datetime import datetime
from multiprocessing import Event
from typing import Dict, List, Tuple, Union

from scripts.config.constant import RedisDB
from scripts.connection.mongo_db.crud import insert_many_to_mongodb
from scripts.connection.redis_conn import get_value
from scripts.util._timezone import timestamp_to_datetime_with_timezone_str


logger = logging.getLogger('connection')


log_prefix_pattern = r'<Collector:\s(\d+\.\d+)>'
log_chunk_pattern = r""


timezone = get_value('common', 'timezone', db=RedisDB.hardware)


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


def parse_cpu(chunk: str) -> float:
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
        usage = cpu - idle
        usage_rate = usage / total
        return usage_rate
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

        # parse log line
        cpu_rate = parse_cpu(chunk)
        if not cpu_rate:
            logger.warning(f'Cannot parse cpu rate. {chunk[:300]}')
            continue
        print(cpu_rate)
        yield cpu_rate

    #     if log_time is not None:  # time data exist in line
    #         if last_time is not None and int(log_time.timestamp()) != int(last_time.timestamp()): 
    #             # when the integer part of the timestamp (the seconds) changes,
    #             # yield the current batch and start a new one
    #             yield batches
    #             batches = []
    #         last_time = log_time  # store the last time
    #         no_time_count = 0
    #     else:
    #         no_time_count += 1
    #         if no_time_count > no_time_count_limit:  # too many no time data in lines
    #             raise Exception(f'No time data in {file_path} at line {index}')
        
    #     if last_time is not None:
    #         batches.append({
    #             **parsed_chunk,
    #             'timestamp': timestamp_to_datetime_with_timezone_str(last_time.timestamp(), timezone=timezone),
    #         })

    # yield batches


def insert_to_db(file_path: str):
    for batch in LogBatchGenerator(file_path):
        # print(batch)
        pass
        
    # json_datas = [construct_json_data(log_batch) for log_batch in LogBatchGenerator(file_path)]
    # logger.info(f'insert {len(json_datas)} datas to db')
    # insert_many_to_mongodb('stb_log', json_datas)


def construct_json_data(log_batch: List[Tuple[float, str]]) -> Dict:
    return {
        'time': re.sub(r'.\d{6}', '', log_batch[0]['timestamp']),
        'lines': [{
            'timestamp': log_chunk['timestamp'],
            'module': str(log_chunk['module']).rstrip().replace('\n', ' '),
            'log_level': log_chunk['log_level'],
            'process_name': log_chunk['pid'],
            'PID': log_chunk['pid'],
            'TID': log_chunk['tid'],
            'message': str(log_chunk['message']).rstrip().replace('\n', ' ') if log_chunk['message'] else '',
        } for log_chunk in log_batch],
    }
 