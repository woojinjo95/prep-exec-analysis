import time
import logging
from threading import Thread
from datetime import datetime, timedelta
from multiprocessing import Queue

from scripts.log_service.log_helper import LogHelper, init_log_helper, terminate_log_helper
from scripts.log_service.log_manage.log_manager import LogFileManager
from scripts.log_service.log_manage.log_handle import load_page, load


log_queue = Queue(maxsize=10000)
log_helper = LogHelper()
init_log_helper(log_helper, log_queue)

logger = logging.getLogger('main')


##### TEST #####
def dumper():
    connection_info = {
        'host': '192.168.30.25',
        'port': 5555,
        'username': 'root',
        'password': '',
        'connection_mode': 'adb',
    }
    manager = LogFileManager(connection_info=connection_info)
    manager.start()
    time.sleep(86400)  # 1 day
    manager.stop()


def searcher():
    while True:
        # get 5 minutes ago logs
        start = datetime.now() - timedelta(minutes=2, seconds=0)
        end = datetime.now() - timedelta(minutes=1, seconds=0)
        # get 1000 lines
        logs = load_page(start.timestamp(), end.timestamp(), 1, 1000)
        print(f'start : {start}, end : {end}, logs : {logs}')
        time.sleep(10)


searcher_thrd = Thread(target=searcher)
searcher_thrd.start()
dumper()



################



terminate_log_helper(log_helper, log_queue)
