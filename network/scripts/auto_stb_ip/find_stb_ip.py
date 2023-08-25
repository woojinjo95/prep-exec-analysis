import logging
import time
from multiprocessing import Event, Process

from ..configs.config import RedisDBEnum, get_value
from ..control.network_control.command_executor import traffic_change
from .brute_ping import brute_ping_ipv4
from ..info.network_info import get_ethernet_state, get_private_ip, EthernetState

logger = logging.getLogger('main')
TIMEOUT = 0.1
STABLE_DELAY = 5
UNIT_DELAY = 10


class STBIPFinder:

    def __init__(self):
        self.start()
        pass

    def run(self):
        self.stop_event = Event()

        stb_nic = get_value('network', 'stb_nic')
        private_ip = get_private_ip()
        prev_state = EthernetState.down
        stb_ip = None

        while not self.stop_event.is_set():
            current_state = get_ethernet_state(stb_nic)
            if (stb_ip is None or prev_state == EthernetState.down) and current_state == EthernetState.up:
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
                        stb_ip = ip
                        logger.info(f'STB: {stb_ip}')
                        break
                else:
                    logger.error('Failed to find STB. maybe STB is not reachable')
                    logger.debug(f'Result: {original_ip_values} / {augmented_ip_values}')

            else:
                time.sleep(0.5)
            if current_state == EthernetState.down:
                stb_ip = None

            prev_state = current_state

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        return self.process
