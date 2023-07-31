import time
import logging
from threading import Thread
from multiprocessing import Event
from datetime import datetime, timedelta
from multiprocessing import Queue

from scripts.log_service.log_helper import LogHelper, init_log_helper, terminate_log_helper
from scripts.log_service.log_manage.log_manager import LogFileManager
from scripts.log_service.log_manage.log_handle import load_page


log_queue = Queue(maxsize=10000)
log_helper = LogHelper()
init_log_helper(log_helper, log_queue)

logger = logging.getLogger('main')


##### TEST #####
def dumper(stop_event):
    try:
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
    except Exception as e:
        logger.info(e)
    finally:
        if manager:
            manager.stop()
        stop_event.set()


def searcher(stop_event):
    while True:
        if stop_event.is_set():
            break
        # get 5 minutes ago logs
        start = datetime.now() - timedelta(minutes=2, seconds=0)
        end = datetime.now() - timedelta(minutes=1, seconds=0)
        # get all lines in page
        page = 1
        while True:
            logs = load_page(start.timestamp(), end.timestamp(), page, 1000)
            if len(logs) == 0:
                break
            print(f'start : {start}, \nend : {end}, \npage: {page}, \nstart_log : {logs[0] if len(logs) > 0 else ""}, \nend_log : {logs[-1] if len(logs) > 0 else ""}, \nlen : {len(logs)}')
            page += 1
        time.sleep(10)


stop_event = Event()
searcher_thrd = Thread(target=searcher, args=(stop_event,))
searcher_thrd.start()

dumper(stop_event)
print('dump end')



################



terminate_log_helper(log_helper, log_queue)
