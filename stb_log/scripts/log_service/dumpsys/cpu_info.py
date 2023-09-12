from typing import List, Dict
import re
import logging
from scripts.connection.stb_connection.utils import exec_command
from scripts.log_service.dumpsys.format import CPUInfo
from scripts.connection.external import get_connection_info


logger = logging.getLogger('dumpsys')


def get_cpuinfo() -> List[str]:
    connection_info = get_connection_info()
    result = exec_command('dumpsys cpuinfo', 5, connection_info)
    return result.splitlines()


def parse_cpu_info_summary(chunk: List[str]) -> CPUInfo:
    result = {'total': '', 'user': '', 'kernel': '', 'iowait': '', 'irq': '', 'softirq': ''}
    for line in chunk:
        match = re.match(
            r'(?P<total>\d*\.?\d*)\%\s?TOTAL\s?:\s?((?P<user>\d*\.?\d*)\%\s?user)?(\s?\+\s?(?P<kernel>\d*\.?\d*)\%\s?kernel)?(\s?\+\s?(?P<iowait>\d*\.?\d*)\%\s?iowait)?(\s?\+\s?(?P<irq>\d*\.?\d*)\%\s?irq)?(\s?\+\s?(?P<softirq>\d*\.?\d*)\%\s?softirq)?', line)
        if match is not None:
            result.update(match.groupdict())
            break
    result = {key: '' if value is None else value for key, value in result.items()}
    return CPUInfo(**result)


def parse_cpu_info() -> CPUInfo:
    try:
        lines = get_cpuinfo()
        cpu_info = parse_cpu_info_summary(lines)
        cpu_info.cpu_usage = cpu_info.total
        return cpu_info
    except Exception as e:
        logger.error(f'Error while parsing cpu info: {e}')
        return CPUInfo()
