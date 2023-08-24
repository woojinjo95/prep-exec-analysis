import re

from scripts.connection.stb_connection.connector import Connection
from scripts.connection.stb_connection.utils import exec_command

##### adb command
# connection_info = {
#     'host': '192.168.30.25',
#     'port': 5555,
#     'username': 'root',
#     'password': '',
#     'connection_mode': 'adb',
# }
# conn = Connection(**connection_info)
# result = exec_command('ps -p 3518', 2, connection_info)
# print(result)


##### parse pid
s = "USER           PID  PPID     VSZ    RSS WCHAN            ADDR S NAME                       system        3518     1   11020   4072 0                   0 S android.hardware.memtrack@1.0-service"
match = re.search(r'S (\S+)$', s)
if match:
    process_name = match.group(1)
    print(process_name)
else:
    print("Process name not found!")
