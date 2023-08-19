import re
import socket
import struct
import subprocess

from typing import Tuple
from ipaddress import IPv4Network

import psutil
from pypacker import ppcap

MTU = 1500
GIGA = 10 ** 9


def check_ipv4(n: str) -> bool:
    try:
        socket.inet_pton(socket.AF_INET, n)
        return True
    except socket.error:
        return False


def convert_ip_bytes_string(ip_bytes: bytes) -> str:
    return socket.inet_ntoa(ip_bytes)


def parse_pcap_file(path: str) -> ppcap.Reader:
    return ppcap.Reader(filename=path)


def check_base_info(packet_bytes: bytes) -> Tuple[bytes, int, int]:
    # mac_info = packet_bytes[:14]
    # ip_info = packet_bytes[14:34]
    # protocol = ip_info[9]
    # layer3_length = ip_info[2] * 0x100 + ip_info[3]

    iptype = packet_bytes[12:14]
    ip_total_legnth = packet_bytes[16] * 256 + packet_bytes[17]
    protocol = packet_bytes[23]

    return iptype, protocol, ip_total_legnth


def get_nic_mac_dict() -> dict:
    mac_addresses = {}
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac_addresses[interface] = addr.address
    return mac_addresses


def get_default_gateway_address() -> str:
    # only work on linux
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def get_subnet_mask(interface: str) -> str:
    for addr in psutil.net_if_addrs()[interface]:
        if addr.family == socket.AF_INET:
            return addr.netmask
    return None


def are_ips_on_same_network(ip1: str, ip2: str, subnet_mask: str) -> bool:
    network1 = IPv4Network(f'{ip1}/{subnet_mask}', strict=False)
    network2 = IPv4Network(f'{ip2}/{subnet_mask}', strict=False)
    return network1 == network2


def get_nic_connected_to_gateway(gateway_ip: str) -> str:
    # Get local IP addresses and their corresponding NICs
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                local_ip = addr.address
                subnet_mask = get_subnet_mask(interface)
                if subnet_mask and are_ips_on_same_network(local_ip, gateway_ip, subnet_mask):
                    return interface
    else:
        return None


def get_hw_address(ip: str) -> str:
    try:
        arp_output = subprocess.check_output(['arp', '-n', ip])
        mac_address_pattern = re.compile(r"(([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2}))")
        match = mac_address_pattern.search(arp_output.decode("utf-8"))
        return match.group(1) if match else None
    except:
        return None


def convert_mac_to_bytes(mac_address: str) -> bytes:
    return bytes(int(byte, 16) for byte in mac_address.split(':'))