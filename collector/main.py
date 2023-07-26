from multiprocessing import Queue
from scripts.log_service.log_helper import LogHelper, init_log_helper


import time
from multiprocessing import Queue
from scripts.file_service.log_manage.log_manager import LogFileManager


log_queue = Queue(maxsize=10000)
log_helper = LogHelper()
init_log_helper(log_helper, log_queue)


##### TEST #####
connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}
manager = LogFileManager(connection_info = connection_info)
manager.start()
time.sleep(60)
manager.stop()