import socket
from collections import defaultdict
from ....utils._exceptions import handle_errors

IPRROTO_MAP = {
    socket.IPPROTO_IP: 'ip',
    socket.IPPROTO_ICMP: 'icmp',
    socket.IPPROTO_TCP: 'tcp',
    socket.IPPROTO_UDP: 'udp',
    socket.IPPROTO_IGMP: 'igmp',
}


@handle_errors
def convert_protocol_enum_to_str(protocol_enum: int) -> str:
    if isinstance(protocol_enum, str):
        protocol = protocol_enum
    else:
        protocol = IPRROTO_MAP.get(protocol_enum, 'ip')

    return protocol
