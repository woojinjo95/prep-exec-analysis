import logging
import time
from multiprocessing import Event, Process

from ..configs.config import RedisDBEnum, get_value
from ..control.network_control.command_executor import traffic_change
from .brute_ping import brute_ping_ipv4
from .network_info import get_ethernet_state, get_private_ip

logger = logging.getLogger('main')
TIMEOUT = 0.1


class STBIPFinder:

    def __init__(self):
        self.start()
        pass

    def run(self):
        self.stop_event = Event()

        stb_nic = get_value('network', 'stb_nic')
        private_ip = get_private_ip()
        prev_state = 'down'
        stb_ip = None

        while not self.stop_event.is_set():
            current_state = get_ethernet_state(stb_nic)
            if (stb_ip is None or prev_state == 'down') and current_state == 'up':
                logger.info('New Settop nic conection detected! wait 5 seconds for stable connection')
                time.sleep(5)

                original = brute_ping_ipv4(private_ip, timeout=TIMEOUT)
                original_delay = get_value('hardware_configuration', 'packet_delay', db=RedisDBEnum.hardware)
                traffic_change(nic=stb_nic, delay=original_delay + 10)
                plus_fifty = brute_ping_ipv4(private_ip, timeout=TIMEOUT)
                traffic_change(nic=stb_nic, delay=original_delay)

                original_values = {k: v for k, v in original}
                for ip, ping_value in plus_fifty[::-1]:
                    if ping_value - original_values.get(ip, TIMEOUT) > (10 * 0.9) / 1000:
                        stb_ip = ip
                        logger.info(f'STB: {stb_ip}')
                        break
                else:
                    logger.error('Failed to find STB. maybe settop is not reachable')
                    logger.debug(f'Result: {original_values} / {plus_fifty}')

            else:
                time.sleep(0.5)
            if current_state == 'down':
                stb_ip = None

            prev_state = current_state

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        return self.process
