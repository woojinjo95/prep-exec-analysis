from datetime import datetime
from scripts.file_service.log_manage.log_manager import LogFileManager


manager = LogFileManager(connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
})

manager.save_datas([(datetime.now().timestamp(), 'test1'), (datetime.now().timestamp(), 'test2')])
print(manager.load_data(datetime.now().timestamp() - 5000, datetime.now().timestamp() + 5000))
