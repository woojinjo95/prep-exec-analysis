import logging
import time
from multiprocessing import Event

from ..configs.config import RedisDBEnum, RedisDBField, get_value, set_value
from ..info.network_info import (EthernetState, get_ethernet_state,
                                 get_gateway_ip, get_private_ip, get_public_ip)
from ..utils._multi_process import ProcessMaintainer

logger = logging.getLogger('info')
STABLE_DELAY = 10


def get_target_ip(name: str) -> str:
    return get_value(RedisDBField.hardware_config, name, '', db=RedisDBEnum.hardware)


def set_target_ip(name: str, target_ip: str):
    set_value(RedisDBField.hardware_config, name, target_ip, db=RedisDBEnum.hardware)


def device_network_state_finder(stop_event: Event, run_state_event: Event):
    br_nic = get_value('network', 'br_nic', 'br0')
    prev_state = EthernetState.down

    while not stop_event.is_set():
        current_state = get_ethernet_state(br_nic)
        private_ip = get_target_ip('private_ip')
        if (private_ip == '' or prev_state == EthernetState.down) and current_state == EthernetState.up:
            logger.info(f'New conection detected! wait {STABLE_DELAY} seconds for stable connection')
            time.sleep(STABLE_DELAY)

            private_ip = get_private_ip()
            public_ip = get_public_ip()
            gateway_ip = get_gateway_ip(br_nic)

            set_target_ip('private_ip', private_ip)
            set_target_ip('public_ip', public_ip)
            set_target_ip('gateway_ip', gateway_ip)

            logger.info(f'Device ip updated : {private_ip} / {public_ip} / {gateway_ip}')

        else:
            time.sleep(1)

        if current_state == EthernetState.down:
            dut_ip = ''
            set_target_ip(private_ip, dut_ip)

        prev_state = current_state


def device_network_state_process() -> ProcessMaintainer:
    process = ProcessMaintainer(func=device_network_state_finder, revive_interval=1)
    process.start()
    return ProcessMaintainer
