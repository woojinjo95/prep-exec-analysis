import logging
import time
from multiprocessing import Event
from typing import Dict

from ..utils._multi_process import ProcessMaintainer

logger = logging.getLogger('service')

from ..state.machine_state import (get_cpu_usage_average_in_percent,
                                   get_disk_usage_in_percent,
                                   get_machine_dut_lan_ip,
                                   get_machine_private_ip,
                                   get_memory_usage_in_percent,
                                   get_representive_temperature)


def get_machine_state() -> Dict:
    values = {'cpu_usage': get_cpu_usage_average_in_percent(),
              'cpu_temp': get_representive_temperature(),
              'memory_usage': get_memory_usage_in_percent(),
              'wan_ip': get_machine_private_ip(),
              'stb_ip': get_machine_dut_lan_ip(),
              'ssd_usage': get_disk_usage_in_percent(),
              }
    
    return values


def start_state_service(interval: float = 10) -> ProcessMaintainer:
    
    def state_service(interval: float, stop_event: Event, run_state_event: Event):
        while stop_event.is_set():
            state = get_machine_state()
            logger.debug(state)
            time.sleep(interval)

    proc = ProcessMaintainer(func=state_service, args=(interval, ), revive_interval=10, daemon=True)
    proc.start()

    return proc
