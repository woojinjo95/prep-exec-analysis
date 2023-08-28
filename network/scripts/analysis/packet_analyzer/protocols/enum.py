import socket
from collections import defaultdict
from ....utils._exceptions import handle_errors

IPRROTO_MAP = {
    socket.IPPROTO_IP: 'IP',
    socket.IPPROTO_ICMP: 'ICMP',
    socket.IPPROTO_TCP: 'TCP',
    socket.IPPROTO_UDP: 'UDP',
    socket.IPPROTO_IGMP: 'IGMP',
}


@handle_errors
def convert_protocol_enum_to_str(protocol_enum: int) -> str:
    if isinstance(protocol_enum, str):
        protocol = protocol_enum
    else:
        protocol = IPRROTO_MAP.get(protocol_enum, f'Proto_{protocol_enum}')

    return protocol
