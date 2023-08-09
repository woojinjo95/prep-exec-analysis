import re
import subprocess


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
    command = 'adb shell dumpsys cpuinfo'
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)
    return result.stdout.splitlines()


# def 


lines = get_cpuinfo()
summary = parse_summary(lines)
print(summary)

# mem_usage_rate = (int(summary['Used_RAM'].replace(',', '')) / int(summary['Total_RAM'].replace(',', ''))) * 100
# print(mem_usage_rate)
