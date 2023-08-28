from scripts.connection.external import set_connection_info, get_connection_info


connection_info = {
    'host': '192.168.30.12',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}

set_connection_info(**connection_info)
result = get_connection_info()
print(result)
