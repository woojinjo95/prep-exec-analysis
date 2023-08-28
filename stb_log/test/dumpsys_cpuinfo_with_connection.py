from scripts.connection.stb_connection.connector import Connection
from scripts.connection.stb_connection.utils import exec_command
import re
import subprocess



connection_info = {
    'host': '192.168.30.25',
    'port': 5555,
    'username': 'root',
    'password': '',
    'connection_mode': 'adb',
}
conn = Connection(**connection_info)
# result = exec_command('ls', 2, connection_info)
# print(result)



def parse_summary(chunk):
    result = {}
    for line in chunk:
        match = re.match(
            r'(?P<total>\d*\.?\d*)\%\s?TOTAL\s?:\s?((?P<user>\d*\.?\d*)\%\s?user)?(\s?\+\s?(?P<kernel>\d*\.?\d*)\%\s?kernel)?(\s?\+\s?(?P<iowait>\d*\.?\d*)\%\s?iowait)?(\s?\+\s?(?P<irq>\d*\.?\d*)\%\s?irq)?(\s?\+\s?(?P<softirq>\d*\.?\d*)\%\s?softirq)?', line)
        if match is not None:
            result = match.groupdict()
            break
    return {key: '0' if value is None else value for key, value in result.items()}


def get_cpuinfo():
    # command = 'adb shell dumpsys cpuinfo'
    # result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)
    # return result.stdout.splitlines()
    result = exec_command('dumpsys cpuinfo', 2, connection_info)
    return result.splitlines()


lines = get_cpuinfo()
summary = parse_summary(lines)
print(summary)