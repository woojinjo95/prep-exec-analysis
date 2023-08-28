import time
import logging
import traceback
from typing import List
from threading import Event
from iterators import TimeoutIterator

from .connector import Connection

logger = logging.getLogger('connection')


def add_su_prefix_to_command_script(command_script: str, connection_mode: str) -> str:
    su_prefix = 'su root'
    if connection_mode == 'adb':
        return f'{su_prefix} {command_script}'
    else:
        return command_script


def close_client(conn: Connection):
    if conn.connection_mode == 'ssh':
        if conn.client:
            conn.client.close()
    elif conn.connection_mode == 'adb':
        if conn.session:
            conn.session.close()
    # logger.info('close client')


def exec_command(command_script: str, timeout: float, connection_info: dict, su_prefix: bool = False) -> str:
    command_result = ''
    try:
        conn = Connection(**connection_info)
        if su_prefix:
            command_script = add_su_prefix_to_command_script(command_script, conn.connection_mode)
        stdout_stop_event = Event()
        stdout = conn.exec_command(command_script, stdout_stop_event)
        start_time = time.time()

        timeout_stdout = TimeoutIterator(stdout, timeout=0.5, sentinel=None)
        for line in timeout_stdout:
            is_timed_out = time.time() - start_time >= timeout
            if is_timed_out:
                break
            elif line is None:
                continue
            else:
                command_result += line

        # clear stdout and conn
        stdout_stop_event.set()
        close_client(conn)
        del conn
        del timeout_stdout
        del stdout

    except Exception as e:
        logger.info(e)

    return command_result


def exec_command_generator(command_script: str, connection_info: dict,
                           stop_events: List[Event] = [], su_prefix: bool = False) -> str:
    try:
        conn = Connection(**connection_info)

        if su_prefix:
            command_script = add_su_prefix_to_command_script(command_script, conn.connection_mode)

        stdout_stop_event = Event()
        stdout = conn.exec_command(command_script, stdout_stop_event)
        timeout_stdout = TimeoutIterator(stdout, timeout=0.5, sentinel=None)

        for line in timeout_stdout:
            # check stop event
            if any([hasattr(event, 'is_set') and event.is_set() for event in stop_events]):
                break

            if line is None:
                continue
            else:
                yield line

    except Exception as e:
        logger.info(e)
        traceback.print_exc()
    
    finally:
        if stdout_stop_event:
            stdout_stop_event.set()
        if conn:
            close_client(conn)
        del conn
        del timeout_stdout
        del stdout
        logger.info('finish to exec command generator')


def check_connection(connection_info: dict) -> bool:
    try:
        # Connection 시도 후 끊기
        if connection_info['connection_mode'] == 'ssh':
            Connection(**connection_info).client.close()
        elif connection_info['connection_mode'] == 'adb':
            Connection(**connection_info).session.close()
        # Connection 시도 후 끊기가 정상적으로 동작할 경우 연결가능 상태
        is_connected = True
    except Exception as e:
        logger.info(e)
        # Connection 시도 후 끊기가 정상적으로 동작하지 않을 경우 연결불가 상태
        is_connected = False
    return is_connected
