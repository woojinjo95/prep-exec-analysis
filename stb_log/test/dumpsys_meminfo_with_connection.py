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



def parse_summary(chunk):
    summary_result = {'Total_RAM': None, 'Free_RAM': None, 'Used_RAM': None, 'Lost_RAM': None}
    for line in chunk:
        # summary_result check
        summary_match = None
        if 'Total RAM:' in line:
            summary_match = re.match(r'\s*Total RAM:\s*(?P<Total_RAM>[0-9\,\-]+)', line)
        elif 'Free RAM:' in line:
            summary_match = re.match(r'\s*Free RAM:\s*(?P<Free_RAM>[0-9\,\-]+)', line)
        elif 'Used RAM:' in line:
            summary_match = re.match(r'\s*Used RAM:\s*(?P<Used_RAM>[0-9\,\-]+)', line)
        elif 'Lost RAM:' in line:
            summary_match = re.match(r'\s*Lost RAM:\s*(?P<Lost_RAM>[0-9\,\-]+)', line)
        if summary_match is not None:
            summary_result.update(summary_match.groupdict())
    if any(k is None for k in summary_result.values()):
        summary_result = {}
    return summary_result


def get_meminfo():
    result = exec_command('dumpsys meminfo', 20, connection_info)
    return result.splitlines()
    # command = 'adb shell dumpsys meminfo'
    # result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)
    # return result.stdout.splitlines()


lines = get_meminfo()
print(lines)
summary = parse_summary(lines)
print(summary)

mem_usage_rate = (int(summary['Used_RAM'].replace(',', '')) / int(summary['Total_RAM'].replace(',', ''))) * 100
print(mem_usage_rate)
