import logging
import time
from multiprocessing import Event

from ..utils._multi_process import ProcessMaintainer

from ..configs.config import RedisDBEnum, RedisDBField, get_value, set_value
from ..control.network_control.command_executor import traffic_change
from ..info.network_info import (EthernetState, get_ethernet_state,
                                 get_mac_address, get_private_ip)
from .brute_ping import brute_ping_ipv4

logger = logging.getLogger('info')
TIMEOUT = 0.1
STABLE_DELAY = 5
UNIT_DELAY = 10


def get_dut_ip() -> str:
    return get_value(RedisDBField.hardware_config, 'dut_ip', '', db=RedisDBEnum.hardware)


def get_dut_mac() -> str:
    return get_value(RedisDBField.hardware_config, 'dut_mac', '', db=RedisDBEnum.hardware)


def get_dut_power_state():
    return get_value(RedisDBField.hardware_config, 'enable_dut_power', '', db=RedisDBEnum.hardware)


def set_dut_ip(dut_ip: str):
    set_value(RedisDBField.hardware_config, 'dut_ip', dut_ip, db=RedisDBEnum.hardware)


def set_dut_mac(dut_mac: str):
    set_value(RedisDBField.hardware_config, 'dut_mac', dut_mac, db=RedisDBEnum.hardware)


def set_dut_net_state(state: bool):
    set_value(RedisDBField.hardware_config, 'dut_net_state', state, db=RedisDBEnum.hardware)


def stb_ip_finder(stop_event: Event, run_state_event: Event):
    stb_nic = get_value('network', 'stb_nic')
    prev_state = EthernetState.down

    while not stop_event.is_set():
        current_state = get_ethernet_state(stb_nic)
        dut_ip = get_dut_ip()

        if current_state == EthernetState.up:
            set_dut_net_state(True)
            if dut_ip == '' or prev_state == EthernetState.down:
                private_ip = get_private_ip()
                logger.info(f'New stb nic conection detected! wait {STABLE_DELAY} seconds for stable connection')
                time.sleep(STABLE_DELAY)

                original_delay = get_value('hardware_configuration', 'packet_delay', db=RedisDBEnum.hardware)
                bridge = get_value('network', 'br_nic', 'br0')

                original_ip_values = brute_ping_ipv4(private_ip, timeout=TIMEOUT, interface=bridge)
                traffic_change(nic=stb_nic, delay=original_delay + UNIT_DELAY)
                augmented_ip_values = brute_ping_ipv4(private_ip, timeout=TIMEOUT, interface=bridge)
                traffic_change(nic=stb_nic, delay=original_delay)

                for ip, ping_value in list(augmented_ip_values.items())[::-1]:
                    if ping_value - original_ip_values.get(ip, TIMEOUT) > (UNIT_DELAY * 0.9) / 1000:
                        dut_ip = ip
                        dut_mac = get_mac_address(dut_ip)
                        set_dut_mac(dut_mac)
                        logger.info(f'STB: {dut_ip} / {dut_mac}')
                        break
                else:
                    logger.error('Failed to find STB. maybe STB is not reachable')
                    logger.debug(f'Result: {original_ip_values} / {augmented_ip_values}')

        else:
            set_dut_net_state(False)
            if get_dut_power_state():
                dut_ip = ''
                set_dut_ip(dut_ip)

        prev_state = current_state
        time.sleep(0.5)


def stb_ip_finder_process() -> ProcessMaintainer:
    process = ProcessMaintainer(target=stb_ip_finder)
    process.start()
    return process
