from datetime import datetime, timedelta
import json
import logging
import os
import time
from .config import CollectorConfig

import requests

from scripts.connection.stb_connection.connector import Connection
from threading import Event
from iterators import TimeoutIterator

logger = logging.getLogger('connection')


# command_info example: {"slot_idx": 0, "logging_item_id": "5c6acc85-da88-45c4-9ccb-8a080d760128", "log_type": "top", "command_script": "top -b -d 10", "command_script_id": 10, "logging_session_id": null, "status": "starting", "retry_count": 185, "process_maintainer": 139790489789728}


def collect(connection_info: dict, command_info, upload_queue, stop_event, is_running):

    is_running.set()
    log_collector_rd_json = hget('log_collecting_list', command_info['logging_item_id'])
    log_collector_rd_json['retry_count'] += 1
    hset('log_collecting_list', command_info['logging_item_id'], log_collector_rd_json)
    # redis에서 connection info 받아옴
    conn = Connection(**connection_info)
    stdout_stop_event = Event()
    stdout = conn.exec_command(command_info['command_script'], stdout_stop_event)
    timeout_stdout = TimeoutIterator(stdout, timeout=CollectorConfig.LOG_STREAM_TIMEOUT, sentinel=None)
    directory_path = f"log/{command_info['slot_idx']}"
    os.makedirs(directory_path, exist_ok=True)

    log_cell_lines = ""
    chunk_count = 1
    json_for_session_id = {'logging_item_id': command_info['logging_item_id']}
    headers = current_access_token_headers()
    logging_session_id = requests.post(f'{LOG_BACKEND_API_URL}/logging_sessions',
                                       json=json_for_session_id, headers=headers).json()['id']
    log_collector_rd_json['logging_session_id'] = logging_session_id
    hset('log_collecting_list', command_info['logging_item_id'], log_collector_rd_json)
    while not stop_event.is_set():
        if chunk_count == CollectorConfig.SESSION_UPDATE_CHUNK_CNT + 1:
            json_for_session_id = {'logging_item_id': command_info['logging_item_id']}
            headers = current_access_token_headers()
            logging_session_id = requests.post(f'{LOG_BACKEND_API_URL}/logging_sessions',
                                               json=json_for_session_id, headers=headers).json()['id']
            log_collector_rd_json['logging_session_id'] = logging_session_id
            hset('log_collecting_list', command_info['logging_item_id'], log_collector_rd_json)
            chunk_count = 1
        log_collector_rd_json['status'] = 'running'
        log_collector_rd_json['retry_count'] = 0
        hset('log_collecting_list', command_info['logging_item_id'], log_collector_rd_json)
        with open(f"{directory_path}/{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{command_info['log_type']}.log",
                  'w', buffering=1, encoding='utf-8-sig') as f:
            logger.info(f'{f.name} start dump file')
            start_time = time.time()
            collector_chunk_start_time = datetime.now().isoformat()
            for line in timeout_stdout:
                if stop_event.is_set():
                    break
                # while not stop_event.is_set():
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
                        if command_info['log_type'] == 'top':
                            # Splitter 강제 주입
                            log_cell_lines = f"Timestamp : {str(datetime.now() - timedelta(seconds=CollectorConfig.LOG_STREAM_TIMEOUT))}\n" + \
                                log_cell_lines
                            f.write(log_cell_lines)
                            log_cell_lines = ""

                    # end 조건 만족할 때 끝내기
                    if any(end_condition):
                        break

                except Exception as e:
                    logger.info(f'Error Msg: {e}')
                    stop_event.set()
                    break

            if chunk_count == CollectorConfig.SESSION_UPDATE_CHUNK_CNT or stop_event.is_set():
                is_finish = True
            else:
                is_finish = False

            # stop event로 종료 할 경우 남은 내용물 다 씀
            # stop event로 종료한게 아니라면, 다음 루프에서 log_cell_lines 내용물들이 다 써지게 되어있음
            if stop_event.is_set() and log_cell_lines != "":
                # top 의 경우 제일 윗줄에 Timestamp 넣어서 씀
                if command_info['log_type'] == 'top':
                    log_cell_lines = f"Timestamp : {str(datetime.now() - timedelta(seconds=CollectorConfig.LOG_STREAM_TIMEOUT))}\n" + \
                        log_cell_lines
                f.write(log_cell_lines)
                log_cell_lines = ""

            file_size = f.tell()
            file_name = f.name
            if file_size > 0:
                logger.info(f'{f.name} {logging_session_id} finish dump file / size : {file_size}Byte')
                upload_queue.put((f.name, logging_session_id, chunk_count, is_finish, collector_chunk_start_time))
                chunk_count += 1
            else:
                logger.info(f'{f.name} {logging_session_id} skip this file. {file_size}Byte')
                os.remove(file_name)
                time.sleep(2)
                # finish collection & close this connection

            # 먼저 stdout이 비정상적으로 끊어지는 경우가 있다. (콜드부팅 등의 경우에) 이럴땐 그냥 나가기!
            if stdout_stop_event.is_set():
                break

    log_collector_rd_json['status'] = 'stopping'
    hset('log_collecting_list', command_info['logging_item_id'], log_collector_rd_json)
    logger.info(f"{command_info['logging_item_id']} {logging_session_id} finish collection")

    # clear stdout and conn
    stdout_stop_event.set()
    close_client(conn)
    del conn
    del timeout_stdout
    del stdout

    is_running.clear()
    log_collector_rd_json['status'] = 'retrying'
    hset('log_collecting_list', command_info['logging_item_id'], log_collector_rd_json)
    return
