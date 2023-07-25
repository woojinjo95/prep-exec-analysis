import time
from threading import Thread
import random
from datetime import datetime, timedelta
from scripts.file_service.log_manage.log_manager import LogFileManager


manager = LogFileManager(connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
})

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


##### Test2 #####
def start_make_data(timeout: float):
    start_time = time.time()
    while True:
        if time.time() > start_time + timeout:
            break
        time.sleep(random.random())
        manager.save_datas([(time.time(), 'test')])
th = Thread(target=start_make_data(5))
th.start()

start_time = datetime.now() - timedelta(minutes=1)
end_time = datetime.now()
print(f'start_time: {start_time}, end_time: {end_time}')
start_timestamp = start_time.timestamp()
end_timestamp = end_time.timestamp()

datas = manager.load_data(start_timestamp, end_timestamp)
datas = [(datetime.fromtimestamp(data[0]).strftime('%Y-%m-%d %H:%M:%S'), data[1]) for data in datas]
print(datas)

th.join()
