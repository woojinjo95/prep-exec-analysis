import re

from scripts.connection.stb_connection.connector import Connection
from scripts.connection.stb_connection.utils import exec_command

connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}

##### adb command
# conn = Connection(**connection_info)
# result = exec_command('ps -p 3518', 2, connection_info)
# print(result)


##### parse pid
# s = "USER           PID  PPID     VSZ    RSS WCHAN            ADDR S NAME                       system        3518     1   11020   4072 0                   0 S android.hardware.memtrack@1.0-service"
# match = re.search(r'S (\S+)$', s)
# if match:
#     process_name = match.group(1)
#     print(process_name)
# else:
#     print("Process name not found!")


##### fetch multi pid
# conn = Connection(**connection_info)


# command = "ps -A | grep -E '3518|5611|32504'"
# result = exec_command(command, 2, connection_info)
# print(result)

# lines = result.strip().split("\n")

# pid_name_dict = {}
# for line in lines:
#     parts = re.split(r'\s+', line)
#     pid = parts[1]
#     name = parts[-1]
#     pid_name_dict[pid] = name

# print(pid_name_dict)


##### with function
def get_process_names(pids, connection_info):
    pid_str = '|'.join([str(pid) for pid in pids])
    command = f"ps -A | grep -E '{pid_str}'"
    result = exec_command(command, 2, connection_info)

    lines = result.strip().split("\n")
    pid_name_dict = {}
    for line in lines:
        parts = re.split(r'\s+', line)
        pid = int(parts[1])
        name = parts[-1]
        pid_name_dict[pid] = name
    return pid_name_dict


process_names = get_process_names([4458, 5611, 32504], connection_info)
print(process_names)