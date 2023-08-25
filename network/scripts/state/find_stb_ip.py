import logging
import time
from multiprocessing import Event, Process

from ..configs.config import RedisDBEnum, get_value, set_value, RedisDBField
from ..control.network_control.command_executor import traffic_change
from .brute_ping import brute_ping_ipv4
from ..info.network_info import get_ethernet_state, get_private_ip, EthernetState

logger = logging.getLogger('info')
TIMEOUT = 0.1
STABLE_DELAY = 5
UNIT_DELAY = 10


def get_dut_ip() -> str:
    return get_value(RedisDBField.hardware_config, 'dut_ip', '', db=RedisDBEnum.hardware)


def set_dut_ip(dut_ip: str):
    set_value(RedisDBField.hardware_config, 'dut_ip', dut_ip, db=RedisDBEnum.hardware)


def stb_ip_finder(stop_event: Event):
    stb_nic = get_value('network', 'stb_nic')
    prev_state = EthernetState.down

    while not stop_event.is_set():
        current_state = get_ethernet_state(stb_nic)
        dut_ip = get_dut_ip()
        if (dut_ip == '' or prev_state == EthernetState.down) and current_state == EthernetState.up:
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
                    logger.info(f'STB: {dut_ip}')
                    set_dut_ip(dut_ip)
                    break
            else:
                logger.error('Failed to find STB. maybe STB is not reachable')
                logger.debug(f'Result: {original_ip_values} / {augmented_ip_values}')

        else:
            time.sleep(0.5)
        if current_state == EthernetState.down:
            dut_ip = ''
            set_dut_ip(dut_ip)

        prev_state = current_state


def stb_ip_finder_process(stop_event: Event = Event()) -> Event:
    process = Process(target=stb_ip_finder, args=(stop_event, ))
    process.start()
    return stop_event
