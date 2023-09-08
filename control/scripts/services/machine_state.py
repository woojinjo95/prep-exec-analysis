import logging
import time
import traceback
from collections import defaultdict
from multiprocessing import Event
from typing import Dict

from ..configs.config import get_value
from ..configs.constant import RedisChannel
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from ..state.machine_state import (get_cpu_usage_average_in_percent,
                                   get_disk_usage_in_percent,
                                   get_machine_dut_lan_ip,
                                   get_machine_private_ip,
                                   get_memory_usage_in_percent,
                                   get_representive_temperature)
from ..utils._multi_process import ProcessMaintainer

logger = logging.getLogger('service')

HARDWARE_CONFIG = 'hardware_configuration'
DUT_HDMI = 'enable_hdmi'


def get_machine_state() -> Dict:
    # key itself is function name of LCDString class
    # value is string or string() object
    values = {'uptime': str(round(time.monotonic())),
              'ir_state': 'on' if get_value(HARDWARE_CONFIG, 'remote_control_type') == 'ir' else 'off',
              'bt_state': 'on',
              'set_status': 'Ready',
              'wan_ip': get_machine_private_ip(),
              'stb_ip': get_machine_dut_lan_ip(),
              'video_input_state': 'on' if get_value(HARDWARE_CONFIG, DUT_HDMI) else 'off',  # temp
              'cpu_temp': get_representive_temperature(),
              #   'cpu_usage': get_cpu_usage_average_in_percent(),
              'memory_usage': get_memory_usage_in_percent(),
              'ssd_usage': get_disk_usage_in_percent(),
              }

    return values


def start_state_service(interval: float = 10) -> ProcessMaintainer:
    logger.info('Start state service')

    prev_state = defaultdict(str)

    def state_service(interval: float, stop_event: Event, run_state_event: Event):
        try:
            with get_strict_redis_connection() as src:
                while not stop_event.is_set():
                    current_state = get_machine_state()
                    logger.debug(current_state)
                    for element, value in current_state.items():
                        if prev_state[element] != value:
                            publish(src, RedisChannel.command, {'msg': 'lcd_control',
                                                                'data': {'func_arg': f'{element}:{value}'}})

                    prev_state.update(current_state)

                    time.sleep(interval)
        except Exception as e:
            logger.error(e)
            logger.info(traceback.format_exc())

    proc = ProcessMaintainer(func=state_service, args=(interval, ), revive_interval=10, daemon=True)
    proc.start()

    return proc
