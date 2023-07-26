import time
import logging
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
# Dump
connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}
manager = LogFileManager(connection_info = connection_info)

manager.start()
try:
    time.sleep(60)
except KeyboardInterrupt:
    pass
finally:
    manager.stop()
    logger.info('stop')

# Search
start = datetime.now() - timedelta(seconds=60)
end = datetime.now()
print(start, end)
logs = load_page(start.timestamp(), end.timestamp(), 1, 10)
print(logs)

################

terminate_log_helper(log_helper, log_queue)
