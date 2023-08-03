import time
import logging
from multiprocessing import Queue
import traceback

from scripts.log_service.log_helper import LogHelper, init_log_helper, terminate_log_helper
from scripts.log_service.log_manage.log_manager import LogFileManager
from scripts.connection.redis import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel


log_queue = Queue(maxsize=10000)
log_helper = LogHelper()
init_log_helper(log_helper, log_queue)

logger = logging.getLogger('main')


# connection info from redis (사용자가 입력한 값을 가져옴)
connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}
log_type = 'logcat'


manager = LogFileManager(connection_info=connection_info, log_type=log_type)


def start_manager():
    try:
        manager.start()
        manager.join()
    except Exception as e:
        logger.error(f'LogFileManager error: {e}')
        logger.warning(traceback.format_exc())
    finally:
        logger.info('LogFileManager finally')
        if manager:
            manager.stop()


def stop_manager():
    manager.stop()


def command_parser(command: dict):
    ''' 
    PUBLISH command '{"streaming": "start"}'
    PUBLISH command '{"streaming": "stop"}'
    '''

    if command.get('streaming'):
        streaming_arg = command.get('streaming')
        if streaming_arg == 'start':
            start_manager()

        elif streaming_arg == 'stop':
            stop_manager()

        else:
            logger.warning(f'Unknown streaming args: {streaming_arg}')


with get_strict_redis_connection() as src:
    for command in Subscribe(src, RedisChannel.command):
        command_parser(command)


terminate_log_helper(log_helper, log_queue)




