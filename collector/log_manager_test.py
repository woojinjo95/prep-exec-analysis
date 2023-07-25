import time
from threading import Thread
import random
from multiprocessing import Event
from datetime import datetime, timedelta
from scripts.file_service.log_manage.log_manager import LogFileManager
from scripts.log_service.log_collect.collector import Collector


connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}

manager = LogFileManager(connection_info = connection_info)

##### Test1 #####
# start_time = datetime.now()
# end_time = datetime.now() + timedelta(minutes=1)
# print(f'start_time: {start_time}, end_time: {end_time}')

# start_timestamp = start_time.timestamp()
# end_timestamp = end_time.timestamp()

# manager.save_datas([(start_timestamp, 'test1'), (end_timestamp, 'test2')])
# datas = manager.load_data(start_timestamp, end_timestamp)
# datas = [(datetime.fromtimestamp(data[0]).strftime('%Y-%m-%d %H:%M:%S'), data[1]) for data in datas]
# print(datas)


# ##### Test2 #####
# def start_make_data(timeout: float):
#     start_time = time.time()
#     while True:
#         if time.time() > start_time + timeout:
#             break
#         time.sleep(random.random())
#         # manager.db_conn.save_data([(time.time(), 'test')])
#         manager.save('test')
# th = Thread(target=start_make_data(5))
# th.start()

# start_time = datetime.now() - timedelta(minutes=1)
# end_time = datetime.now()
# print(f'start_time: {start_time}, end_time: {end_time}')
# start_timestamp = start_time.timestamp()
# end_timestamp = end_time.timestamp()

# # datas = manager.db_conn.load_data(start_timestamp, end_timestamp)
# # datas = manager.db_conn.load_data_with_paging(start_timestamp, end_timestamp, 1, 6)
# datas = manager.load_page(start_timestamp, end_timestamp, 1, 6)
# datas = [(datetime.fromtimestamp(data[0]).strftime('%Y-%m-%d %H:%M:%S'), data[1]) for data in datas]
# print(datas)

# th.join()


##### Test3 #####
collector = Collector(connection_info, 'logcat -v long', 'logcat', Event())
collector.collect()