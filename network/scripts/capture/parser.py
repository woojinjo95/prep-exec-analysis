import logging
import os
import socket
import time
from collections import deque
from typing import Iterable, List, Tuple

from pypacker import ppcap
from pypacker.layer12 import ethernet

from ..control.command import get_pid_list
from .dumper import (FILENAME, ROTATING_FILE_COUNT, TCPDUMP, dirpath,
                     get_pcap_file_list)

logger = logging.getLogger('capture')

GIGA = 10 ** 9


def parse_pcap_file(path: str):
    return ppcap.Reader(filename=path)


def convert_ip_bytes_string(ip_bytes: bytes):
    return socket.inet_ntoa(ip_bytes)


def get_base_info(packet_bytes: bytes) -> Tuple[int, int, int]:
    # mac_info = packet_bytes[:14]
    # ip_info = packet_bytes[14:34]
    # protocol = ip_info[9]
    # layer3_length = ip_info[2] * 0x100 + ip_info[3]

    iptype = packet_bytes[12:14]
    ip_total_legnth = packet_bytes[16] * 256 + packet_bytes[17]
    protocol = packet_bytes[23]

    return iptype, protocol, ip_total_legnth


def get_packet_info(packet_bytes: bytes) -> Tuple[str, str, str, int]:
    ip_src = convert_ip_bytes_string(packet_bytes[26:30])
    ip_dst = convert_ip_bytes_string(packet_bytes[30:34])
    protocol = packet_bytes[23]
    length = len(packet_bytes)
    return ip_src, ip_dst, protocol, length


def get_stale_pcap_chunck_files() -> List[str]:
    # return get_pcap_file_list(os.path.join(dirpath, 'pcaps_stale'))
    return get_pcap_file_list(os.path.join(dirpath, 'pcaps'))


def init_read_path_list(rotation_file_count: int = ROTATING_FILE_COUNT) -> Iterable:
    # padding: 10
    return deque(maxlen=(rotation_file_count + 10))


def get_timestamp_from_pcap_file_name(file_path: str) -> float:
    # FILENAME = 'result_%s.pcap'
    basename = os.path.basename(file_path)
    name, _ = os.path.splitext(basename)
    time_string = name.split('_')[1]
    timestamp = float(time_string)
    return timestamp


def get_completed_pcap_chunck_files(start_time: float, dump_interval: int) -> List[str]:
    file_list = get_pcap_file_list()
    if get_pid_list(TCPDUMP):
        completed_pcap_file_list = [file_path for file_path
                                    in file_list
                                    if get_timestamp_from_pcap_file_name(file_path) + dump_interval + 1 < time.time()]
    else:
        completed_pcap_file_list = file_list

    return completed_pcap_file_list


def write_pcap_file(dump_dir: str, start_time: float = None, end_time: float = None, interval: float = 10, dump_interval: int = 5) -> str:
    if not os.path.isdir(dump_dir):
        logger.error(f'{dump_dir} is not directory. cannot dump pcap file.')
        return ''

    if start_time is None:
        start_time = time.time()
    if end_time is None:
        end_time = start_time + interval

    logger.info(f'dump pcapfile from {start_time} to {end_time}')

    filename = os.path.join(dump_dir, f'network_{start_time}.pcap')
    with ppcap.Writer(filename=filename, linktype=ppcap.DLT_EN10MB) as pwriter:
        read_path = []
        timestamp = 0
        while timestamp < end_time:
            for file_path in get_completed_pcap_chunck_files(start_time, dump_interval):
                if file_path not in read_path:
                    reader = parse_pcap_file(file_path)
                    for ts, buffer in reader:
                        timestamp = ts / GIGA
                        if start_time < timestamp < end_time:
                            pwriter._timestamp = ts
                            pwriter.write(buffer)
                        elif timestamp > timestamp:
                            break
                read_path.append(file_path)
                time.sleep(0.1)

            if len(get_pid_list(TCPDUMP)) == 0:
                break
        print(timestamp)
