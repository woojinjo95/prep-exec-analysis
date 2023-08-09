from typing import List, Dict
import subprocess
import re
import logging


logger = logging.getLogger('connection')


def get_meminfo() -> List[str]:
    command = 'adb shell dumpsys meminfo'
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)
    return result.stdout.splitlines()


def parse_mem_info_summary(chunk: List[str]) -> Dict:
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


def parse_memory_info() -> Dict:
    try:
        lines = get_meminfo()
        summary = parse_mem_info_summary(lines)
        return summary
    except Exception as e:
        logger.error(f'Error while parsing memory info: {e}')
        return {}
