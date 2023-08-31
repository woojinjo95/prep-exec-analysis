# from dataframe import dumpsys_meminfo_df_from_rawfile


# file_path = './a.txt'
# summary, detail = dumpsys_meminfo_df_from_rawfile(file_path)
# print(summary['Total_RAM'])


import re
import subprocess
import shutil
import os


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


# file_path = './a.txt'

# command = f'adb shell dumpsys meminfo > {file_path}'
# subprocess.call(command, shell=True)

# with open(file_path, 'r') as f:
#     lines = f.readlines()
#     summary = parse_summary(lines)
#     print(summary)
#     mem_usage_rate = (int(summary['Used_RAM'].replace(',', '')) / int(summary['Total_RAM'].replace(',', ''))) * 100
#     print(mem_usage_rate)

# os.remove(file_path)





import subprocess

def get_meminfo():
    command = 'adb shell dumpsys meminfo'
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)
    return result.stdout.splitlines()


lines = get_meminfo()
summary = parse_summary(lines)
print(summary)

mem_usage_rate = (int(summary['Used_RAM'].replace(',', '')) / int(summary['Total_RAM'].replace(',', ''))) * 100
print(mem_usage_rate)
