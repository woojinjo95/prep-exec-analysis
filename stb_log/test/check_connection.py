from scripts.connection.stb_connection.utils import check_connection


connection_info = {
    'host': '192.168.30.12',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}

result = check_connection(connection_info)
print(result)

