import logging
import socket
from typing import Dict, List

from .command_executor import (ebtables_block, ebtables_clear, ebtables_init,
                               traffic_change, traffic_clear, traffic_init)
from ...analysis.packet_analyzer.model.local import check_valid_multicast_ip


logger = logging.getLogger('network_control')


def change_traffic_control(nic: str, bandwidth: float, delay: float, loss: float, duplicate: float, corrupt: float) -> dict:
    return traffic_change(nic, bandwidth, delay, loss, duplicate, corrupt)


def change_packet_block(nic: str, packet_blocks: List[Dict]) -> List[Dict]:
    result = []
    for packet_block in packet_blocks:
        ip = packet_block.get('ip')
        port = packet_block.get('port')
        protocol = packet_block.get('protocol', 'all')
        filter_type = packet_block.get('filter_type', 'source')
        if ip and check_valid_multicast_ip(socket.inet_aton(ip)):
            filter_type = 'destination'
        command = packet_block.get('command', 'add')
        result.append(ebtables_block(nic, ip, port, protocol, filter_type, command))

    return result


def reset_network(nic):
    execute_result = False

    traffic_clear(nic)
    traffic_init(nic)
    ebtables_clear()
    ebtables_init(nic)

    execute_result = True
    logger.info('Network control reset')

    return execute_result
