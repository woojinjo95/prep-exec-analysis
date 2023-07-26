import logging
import os
import time
from datetime import datetime, timedelta
from typing import List
from multiprocessing import Event
from uuid import uuid4
import traceback
import shutil

from iterators import TimeoutIterator
from scripts.connection.stb_connection.connector import Connection
from scripts.connection.stb_connection.utils import close_client
from scripts.util.common import check_stop_events

from .format import CollectorConfig

logger = logging.getLogger('connection')


def collect(connection_info: dict, command_script: str, log_type: str, 
            stop_events: List[Event]):
    stop_event = Event()
    stop_events = (*stop_events, stop_event)

    conn = Connection(**connection_info)
    stdout_stop_event = Event()
    stdout = conn.exec_command(command_script, stdout_stop_event)
    timeout_stdout = TimeoutIterator(stdout, timeout=CollectorConfig.LOG_STREAM_TIMEOUT, sentinel=None)

    log_dir = 'logs'
    shutil.rmtree(log_dir, ignore_errors=True)
    os.makedirs(log_dir, exist_ok=True)
    completed_log_dir = 'completed_logs'
    os.makedirs(completed_log_dir, exist_ok=True)

    log_cell_lines = ""

    while not check_stop_events(stop_events):
        with open(os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{log_type}.log"),
                'w', buffering=1, encoding='utf-8-sig') as f:
            logger.info(f'{f.name} start dump file')
            start_time = time.time()

            for line in timeout_stdout:
                if check_stop_events(stop_events):
                    break
                end_condition = [f.tell() >= CollectorConfig.DUMP_FILESIZE_LIMIT,
                                time.time() - start_time >= CollectorConfig.DUMP_TIME_LIMIT]
                try:
                    # Timeout 안걸렸을 때
                    if line is not None:
                        # 다음 splitter가 등장하면 현재 cell 쓰고 cell 초기화
                        if log_cell_lines != "" and any([line.startswith(spliter) for spliter in CollectorConfig.LOG_CELL_SPLITER]):
                            f.write(log_cell_lines)
                            log_cell_lines = ""
                        # line 내용물 모음
                        log_cell_lines += line
                    # Top의 경우 Splitter가 없기 때문에 Timeout 걸린 직후 다음 cell 기다리는 동안 씀
                    elif log_cell_lines != "":
                        if log_type == 'top':
                            # Splitter 강제 주입
                            log_cell_lines = f"Timestamp : {str(datetime.now() - timedelta(seconds=CollectorConfig.LOG_STREAM_TIMEOUT))}\n" + \
                                log_cell_lines
                            f.write(log_cell_lines)
                            log_cell_lines = ""

                    # end 조건 만족할 때 끝내기
                    if any(end_condition):
                        break

                except Exception as e:
                    logger.info(f'Error Msg: {traceback.format_exc()}')
                    stop_event.set()
                    break

            # stop event로 종료 할 경우 남은 내용물 다 씀
            # stop event로 종료한게 아니라면, 다음 루프에서 log_cell_lines 내용물들이 다 써지게 되어있음
            if check_stop_events(stop_events) and log_cell_lines != "":
                # top 의 경우 제일 윗줄에 Timestamp 넣어서 씀
                if log_type == 'top':
                    log_cell_lines = f"Timestamp : {str(datetime.now() - timedelta(seconds=CollectorConfig.LOG_STREAM_TIMEOUT))}\n" + \
                        log_cell_lines
                f.write(log_cell_lines)
                log_cell_lines = ""

            file_size = f.tell()
            file_name = f.name
            logger.info(f'{f.name} finish dump file / size : {file_size} Byte')
            shutil.move(file_name, os.path.join(completed_log_dir, os.path.basename(file_name)))

            # 먼저 stdout이 비정상적으로 끊어지는 경우가 있다. (콜드부팅 등의 경우에) 이럴땐 그냥 나가기!
            if stdout_stop_event.is_set():
                break

    logger.info(f"finish collection")

    # clear stdout and conn
    stdout_stop_event.set()
    close_client(conn)
    del conn
    del timeout_stdout
    del stdout

    return
