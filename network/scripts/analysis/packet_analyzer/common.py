import socket
from typing import Iterable

ETHERNET_IPV4_TYPE = b'\x08\x00'
ETHERNET_IPV6_TYPE = b'\x86\xdd'


def convert_ip_bytes_string(ip_bytes: bytes):
    return socket.inet_ntoa(ip_bytes)
