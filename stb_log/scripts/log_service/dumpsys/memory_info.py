import logging
import re
from typing import List

from scripts.connection.external import get_connection_info
from scripts.connection.stb_connection.utils import exec_command
from scripts.log_service.dumpsys.format import MemoryInfo
from scripts.util.common import convert_comma_separated_number_to_int
from scripts.config.config import get_setting_with_env

logger = logging.getLogger('dumpsys')


def get_meminfo() -> List[str]:
    connection_info = get_connection_info()
    result = exec_command('dumpsys meminfo', get_setting_with_env('MEMINFO_EXTRACTION_TIMEOUT', 20), connection_info)
    return result.splitlines()


def parse_mem_info_summary(chunk: List[str]) -> MemoryInfo:
    summary_result = {'total_ram': '', 'free_ram': '', 'used_ram': '', 'lost_ram': ''}
    for line in chunk:
        # summary_result check
        summary_match = None
        if 'Total RAM:' in line:
            summary_match = re.match(r'\s*Total RAM:\s*(?P<total_ram>[0-9\,\-]+)', line)
        elif 'Free RAM:' in line:
            summary_match = re.match(r'\s*Free RAM:\s*(?P<free_ram>[0-9\,\-]+)', line)
        elif 'Used RAM:' in line:
            summary_match = re.match(r'\s*Used RAM:\s*(?P<used_ram>[0-9\,\-]+)', line)
        elif 'Lost RAM:' in line:
            summary_match = re.match(r'\s*Lost RAM:\s*(?P<lost_ram>[0-9\,\-]+)', line)
        if summary_match is not None:
            summary_result.update(summary_match.groupdict())
    result = {key: '' if value is None else str(convert_comma_separated_number_to_int(value)) for key, value in summary_result.items()}
    return MemoryInfo(**result)


def parse_memory_info() -> MemoryInfo:
    try:
        lines = get_meminfo()
        mem_info = parse_mem_info_summary(lines)
        mem_info.memory_usage = str((int(mem_info.used_ram) / int(mem_info.total_ram)) * 100)
        return mem_info
    except Exception as e:
        logger.error(f'Error while parsing memory info: {e}')
        return MemoryInfo()
