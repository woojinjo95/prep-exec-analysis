import logging
import time
from datetime import datetime, timedelta
from multiprocessing import Event, Queue

from iterators import TimeoutIterator
from scripts.connection.stb_connection.connector import Connection
from scripts.connection.stb_connection.utils import close_client

from .config import CollectorConfig

logger = logging.getLogger('collector')


def put_log_cell(queue: Queue, cell: str):
    if queue.qsize() < CollectorConfig.LOG_QUEUE_MAX_SIZE:
        queue.put((time.time(), cell))
    else:
        logger.warning(f"log queue is full. queue size: {queue.qsize()}")


def collect(connection_info: dict, command_script: str, log_type: str, stop_event: Event, queue: Queue):
    logger.info(f"start log collection. connection_info: {connection_info}, command_script: {command_script}, log_type: {log_type}")

    conn = Connection(**connection_info)
    stdout = conn.exec_command(command_script, stop_event)
    timeout_stdout = TimeoutIterator(stdout, timeout=CollectorConfig.LOG_STREAM_TIMEOUT, sentinel=None)

    log_cell_lines = ""

    logger.info('start log collection loop')

    for line in timeout_stdout:
        if stop_event.is_set():
            break
        # Timeout 안걸렸을 때
        if line is not None:
            # 다음 splitter가 등장하면 현재 cell 쓰고 cell 초기화
            if log_cell_lines != "" and any([line.startswith(spliter) for spliter in CollectorConfig.LOG_CELL_SPLITER]):
                put_log_cell(queue, log_cell_lines)
                log_cell_lines = ""
            # line 내용물 모음
            log_cell_lines += line
        # Top의 경우 Splitter가 없기 때문에 Timeout 걸린 직후 다음 cell 기다리는 동안 씀
        elif log_cell_lines != "":
            if log_type == 'top':
                # Splitter 강제 주입
                log_cell_lines = f"Timestamp : {str(datetime.now() - timedelta(seconds=CollectorConfig.LOG_STREAM_TIMEOUT))}\n" + \
                    log_cell_lines
                put_log_cell(queue, log_cell_lines)
                log_cell_lines = ""

    # finalize
    if log_cell_lines != "":
        # top 의 경우 제일 윗줄에 Timestamp 넣어서 씀
        if log_type == 'top':
            log_cell_lines = f"Timestamp : {str(datetime.now() - timedelta(seconds=CollectorConfig.LOG_STREAM_TIMEOUT))}\n" + \
                log_cell_lines
        put_log_cell(queue, log_cell_lines)
        log_cell_lines = ""

    logger.info(f"finish log collection")

    # clear stdout and conn
    close_client(conn)
    del conn
    del timeout_stdout
    del stdout
