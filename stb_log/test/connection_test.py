from scripts.connection.stb_connection.connector import Connection
from scripts.connection.stb_connection.utils import exec_command

connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}
conn = Connection(**connection_info)
result = exec_command('ls', 2, connection_info)
print(result)
