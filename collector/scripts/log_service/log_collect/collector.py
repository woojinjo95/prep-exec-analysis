import logging
import os
import time
from datetime import datetime, timedelta
from typing import List
from multiprocessing import Event, Queue
from uuid import uuid4
import traceback

from iterators import TimeoutIterator
from scripts.connection.stb_connection.connector import Connection
from scripts.connection.stb_connection.utils import close_client

from .format import CollectorConfig

logger = logging.getLogger('connection')


def check_stop_events(stop_events) -> bool:
    return any([stop_event.is_set() for stop_event in stop_events if hasattr(stop_event, 'is_set')])


def collect(connection_info: dict, command_script: str, log_type: str, 
            stop_events: List[Event]):
    # is_running.set()
    stop_event = Event()
    stop_events = (*stop_events, stop_event)

    output_dir = 'logs'
    logging_session_id = str(uuid4())
    status = 'stopping'

    conn = Connection(**connection_info)
    stdout_stop_event = Event()
    stdout = conn.exec_command(command_script, stdout_stop_event)
    timeout_stdout = TimeoutIterator(stdout, timeout=CollectorConfig.LOG_STREAM_TIMEOUT, sentinel=None)
    directory_path = output_dir
    os.makedirs(directory_path, exist_ok=True)

    log_cell_lines = ""
    chunk_count = 1

    while not check_stop_events(stop_events):
        if chunk_count == CollectorConfig.SESSION_UPDATE_CHUNK_CNT + 1:
            chunk_count = 1
        status = 'running'

        with open(f"{directory_path}/{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{log_type}.log",
                'w', buffering=1, encoding='utf-8-sig') as f:
            logger.info(f'{f.name} start dump file')
            start_time = time.time()
            collector_chunk_start_time = datetime.now().isoformat()

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

            if chunk_count == CollectorConfig.SESSION_UPDATE_CHUNK_CNT or check_stop_events(stop_events):
                is_finish = True
            else:
                is_finish = False

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
            if file_size > 0:
                logger.info(f'{f.name} {logging_session_id} finish dump file / size : {file_size}Byte')
                # upload_queue.put((f.name, logging_session_id, chunk_count, is_finish, collector_chunk_start_time))
                chunk_count += 1
            else:
                logger.info(f'{f.name} {logging_session_id} skip this file. {file_size}Byte')
                os.remove(file_name)
                time.sleep(2)
                # finish collection & close this connection

            # 먼저 stdout이 비정상적으로 끊어지는 경우가 있다. (콜드부팅 등의 경우에) 이럴땐 그냥 나가기!
            if stdout_stop_event.is_set():
                break

    status = 'stopping'
    logger.info(f"{logging_session_id} finish collection")
    # is_running.clear()

    # clear stdout and conn
    stdout_stop_event.set()
    close_client(conn)
    del conn
    del timeout_stdout
    del stdout

    return
