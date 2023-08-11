import os
import time
from typing import List

from .parser import parse_epg_pcapfile, ChannelInfo
from .getter import join_multicast_and_dump_pcap


def ip_address_to_hex(ip_address: str) -> str:
    return ''.join('{:02x}'.format(int(byte)) for byte in ip_address.split('.'))


def get_epg_data(epg_ip: str, epg_port: int, duration: int = 10, dump_path: str = '', remove_dumped: bool = False) -> List[ChannelInfo]:
    dump_path = dump_path if dump_path else os.path.dirname(__file__)
    abs_dump_path = os.path.abspath(dump_path)
    start_time = int(time.time())

    ip_hex = ip_address_to_hex(epg_ip)
    pcap_file_name = os.path.join(abs_dump_path, f'epg_packet_dump_{ip_hex}_{start_time}.pcap')

    join_multicast_and_dump_pcap(epg_ip, epg_port, duration, pcap_file_name)
    epg_data = parse_epg_pcapfile(pcap_file_name, epg_ip)

    if remove_dumped and os.path.exists(pcap_file_name):
        os.remove(pcap_file_name)

    return epg_data


# sk  get_epg_data('239.192.60.43', 49200)
# lg  get_epg_data('233.18.145.128', 5040)
