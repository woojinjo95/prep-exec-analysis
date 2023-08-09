from typing import List, Dict
import re
import subprocess
import logging


logger = logging.getLogger('connection')


def get_cpuinfo() -> List[str]:
    command = 'adb shell dumpsys cpuinfo'
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)
    return result.stdout.splitlines()


def parse_cpu_info_summary(chunk: List[str]) -> Dict:
    result = {}
    for line in chunk:
        match = re.match(
            r'(?P<total>\d*\.?\d*)\%\s?TOTAL\s?:\s?((?P<user>\d*\.?\d*)\%\s?user)?(\s?\+\s?(?P<kernel>\d*\.?\d*)\%\s?kernel)?(\s?\+\s?(?P<iowait>\d*\.?\d*)\%\s?iowait)?(\s?\+\s?(?P<irq>\d*\.?\d*)\%\s?irq)?(\s?\+\s?(?P<softirq>\d*\.?\d*)\%\s?softirq)?', line)
        if match is not None:
            result = match.groupdict()
            break
    return {key: '0' if value is None else value for key, value in result.items()}


def parse_cpu_info() -> Dict:
    try:
        lines = get_cpuinfo()
        summary = parse_cpu_info_summary(lines)
        return summary
    except Exception as e:
        logger.error(f'Error while parsing cpu info: {e}')
        return {}
