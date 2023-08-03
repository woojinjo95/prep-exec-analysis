import time
import logging
from multiprocessing import Queue
import threading
import traceback

from scripts.log_service.log_helper import LogHelper, init_log_helper, terminate_log_helper
from scripts.log_service.log_manage.log_manager import LogFileManager
from scripts.connection.redis import get_strict_redis_connection
from scripts.connection.redis_pubsub import Subscribe
from scripts.config.constant import RedisChannel, RedisDB


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


def command_parser(command: dict, stop_event: threading.Event):
    ''' 
    PUBLISH command '{"streaming": "start"}'
    PUBLISH command '{"streaming": "stop"}'
    '''

    if command.get('streaming'):
        streaming_arg = command.get('streaming')
        logger.info(f'command_parser: {streaming_arg}')

        if streaming_arg == 'start':
            if manager.is_alive():
                logger.warning('LogFileManager is already alive')
                return
            else:
                logger.info('start_manager')
                manager.start()

        elif streaming_arg == 'stop':
            logger.info('stop_manager')
            manager.stop()

        else:
            logger.warning(f'Unknown streaming args: {streaming_arg}')


stop_event = threading.Event()

with get_strict_redis_connection(RedisDB.hardware) as src:
    for command in Subscribe(src, RedisChannel.command):
        command_parser(command, stop_event)


terminate_log_helper(log_helper, log_queue)




