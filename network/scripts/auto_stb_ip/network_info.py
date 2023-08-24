import re

from ..control.command import get_stdout


def get_ethernet_state(nic: str):
    return get_stdout(f'cat /sys/class/net/{nic}/operstate', log=False).strip()


def get_private_ip() -> str:
    bridge = 'br0'

    bridge_ipv4_info = get_stdout(f'ip -4 addr show {bridge}')

    bridge_ipv4 = re.search(r'(?<=inet\s)\d+(\.\d+){3}', bridge_ipv4_info)

    if bridge_ipv4:
        private_ip = bridge_ipv4.group()
    else:
        pass  # use 0.0.0.0

    return private_ip
