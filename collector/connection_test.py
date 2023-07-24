from scripts.log_util.stb_connection.connector import Connection
from scripts.log_util.stb_connection.utils import exec_command

conn = Connection(host='192.168.30.25', port=5555, username='root', password='', connection_mode='adb')
result = exec_command('ls', 2, conn)
print(result)