import time
import logging
from multiprocessing import Queue
import traceback

from scripts.log_service.log_helper import LogHelper, init_log_helper, terminate_log_helper
from scripts.log_service.log_manage.log_manager import LogFileManager


log_queue = Queue(maxsize=10000)
log_helper = LogHelper()
init_log_helper(log_helper, log_queue)

logger = logging.getLogger('main')


# connection info from redis (툴에서 사용자가 입력한 값을 가져옴)
connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}


def start_manager():
    try:
        manager = LogFileManager(connection_info=connection_info)
        manager.start()
        manager.join()
    except Exception as e:
        logger.error(f'LogFileManager error: {e}')
        logger.warning(traceback.format_exc())
    finally:
        if manager:
            manager.stop()


while True:
    logger.info('stb_log manager start')
    start_manager()
    logger.info('stb_log manager end')
    time.sleep(10)


terminate_log_helper(log_helper, log_queue)