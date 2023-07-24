import time
import logging
from threading import Event
from iterators import TimeoutIterator

from .connector import Connection
from .format import ConnectionInfo

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
    logger.info('close client')


def exec_command(command_script: str, timeout: float, connection_info: ConnectionInfo, su_prefix: bool = False) -> str:
    command_result = ''
    try:
        conn = Connection(connection_info.host, connection_info.port, connection_info.username, connection_info.password, connection_info.connection_mode)
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
