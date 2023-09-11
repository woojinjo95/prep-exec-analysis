import logging
import time
import traceback
from collections import defaultdict
from multiprocessing import Event
from typing import Dict

from ..configs.config import get_value
from ..configs.constant import RedisChannel
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from ..device.remocon.remocon_process import RemoconProcess
from ..state.machine_state import (get_cpu_usage_average_in_percent,
                                   get_current_running_state,
                                   get_disk_usage_in_percent,
                                   get_machine_dut_lan_ip,
                                   get_machine_private_ip,
                                   get_memory_usage_in_percent,
                                   get_representive_temperature)
from ..utils._multi_process import ProcessMaintainer

logger = logging.getLogger('service')

HARDWARE_CONFIG = 'hardware_configuration'
DUT_HDMI = 'enable_hdmi'
LCD = 'lcd'


def uptime() -> str:
    return str(round(time.monotonic()))


def get_machine_state() -> Dict:
    # key itself is function name of LCDString class
    # value is string or string() object
    values = {'ir_state': 'on' if get_value(HARDWARE_CONFIG, 'remote_control_type') == 'ir' else 'off',
              'bt_state': 'off',
              'uptime': uptime(),
              'set_status': get_current_running_state(),
              'wan_ip': get_machine_private_ip(),
              'stb_ip': get_machine_dut_lan_ip(),
              'video_input_state': 'on' if get_value(HARDWARE_CONFIG, DUT_HDMI) else 'off',  # temp
              'cpu_temp': get_representive_temperature(),
              #   'cpu_usage': get_cpu_usage_average_in_percent(),
              'memory_usage': get_memory_usage_in_percent(),
              'ssd_usage': get_disk_usage_in_percent(),
              }

    return values


def start_state_service(remocon_process: RemoconProcess, interval: int = 10) -> ProcessMaintainer:
    logger.info('Start state service')

    prev_state = defaultdict(str)

    def state_service(interval: int, stop_event: Event, run_state_event: Event):
        try:
            with get_strict_redis_connection() as src:
                while not stop_event.is_set():
                    current_state = get_machine_state()
                    logger.debug(current_state)
                    for element, value in current_state.items():
                        if prev_state[element] != value:
                            lcd_string = f'{element}:{value}'
                            remocon_process.put_command(key=lcd_string, _type=LCD)
                            # too many log in watcher, directly input data, log is in control.
                            # publish(src, RedisChannel.command, {'msg': 'lcd_control',
                            #                                     'data': {'func_arg': lcd_string}})

                    prev_state.update(current_state)

                    time.sleep(1)
                    for _ in range(interval - 1):
                        # update is update by 1 seconds
                        remocon_process.put_command(key=f'update:{uptime()}', _type=LCD)
                        time.sleep(1)

        except Exception as e:
            logger.error(e)
            logger.info(traceback.format_exc())

    proc = ProcessMaintainer(func=state_service, args=(interval, ), revive_interval=10, daemon=True)
    proc.start()

    return proc
