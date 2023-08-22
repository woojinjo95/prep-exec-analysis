import logging
import time
from collections import defaultdict
from pprint import pformat
from socket import IPPROTO_IGMP, IPPROTO_UDP

from ...capture.parser import get_base_info, parse_pcap_file
from ...epg.epg import get_channel_info
from .analysis import check_iso_iec_structure, check_rtp_sequence
from .common import ETHERNET_IPV4_TYPE, convert_ip_bytes_string
from .model.local import check_valid_multicast_ip
from .protocols.igmp import IGMPConst, igmp_parser
from .protocols.mpeg2ts import mpeg2_ts_parser
from .rtp_stream import calc_bitrate, calc_jitter, get_default_ip_info
from ...mongo_db_update import InsertToMongoDB

GIGA = 10 ** 9


logger = logging.getLogger('analysis')
capture_logger = logging.getLogger('capture')


def read_pcap_file(path: str):
    index = 0
    capture_logger.info(f'Load pcap file: {path}')
    for timestamp_w_ns, packet_bytes in parse_pcap_file(path):
        index += 1
        timestamp = timestamp_w_ns / GIGA
        iptype, protocol, ip_total_legnth = get_base_info(packet_bytes)
        if iptype != ETHERNET_IPV4_TYPE:
            continue
        elif protocol == IPPROTO_IGMP:
            yield (timestamp, IPPROTO_IGMP, *igmp_parser(packet_bytes), packet_bytes)
        elif protocol == IPPROTO_UDP and ip_total_legnth >= 1316:  # 7 * 188 = 1316
            datas = mpeg2_ts_parser(packet_bytes)
            if datas[1][1] is not None:
                yield (timestamp, IPPROTO_UDP, *datas, packet_bytes)
        else:
            pass


def get_rtp_sequence_in_info(protocol: int, info: dict) -> int:
    rtp_sequence = info[0] if protocol == IPPROTO_UDP else -1
    return rtp_sequence


def add_new_stream_ip(stream_dict: dict, timestamp: float, protocol: int, ip: bytes, info: tuple):
    rtp_sequence = get_rtp_sequence_in_info(protocol, info)
    stream_dict[ip] = get_default_ip_info(timestamp, rtp_sequence)


def run_iptv_analysis(mongo_session: InsertToMongoDB, stream_dict: dict, timestamp: float, protocol: int, ip: bytes,
                      info: tuple, packet_bytes: bytes, archived_stream_dict: dict = None):
    ip_dict = stream_dict[ip]

    if not check_valid_multicast_ip(ip):
        del stream_dict[ip]
        return

    ip_dict['count'] += 1
    ip_dict['bytes'] += len(packet_bytes)

    if not ip_dict['joined']:
        if ip_dict['leave_time'] == 0:
            if protocol == IPPROTO_IGMP:
                if info == IGMPConst.join and ip_dict['join_time'] == 0:
                    ip_str = convert_ip_bytes_string(ip)
                    channel_info = get_channel_info(ip_str)
                    logger.info(f'UDP stream joined: {ip_str} ({channel_info}) in {timestamp}')
                    ip_dict['join_time'] = timestamp
            else:
                ip_dict['joined'] = True
                ip_dict['join_interval'] = timestamp - ip_dict['join_time'] if ip_dict['join_time'] != 0 else -1
                ip_dict['deltas'].appendleft(timestamp - ip_dict['timestamp'])

        elif protocol == IPPROTO_UDP:
            ip_dict['leave_interval'] = timestamp - ip_dict['leave_time']
        else:
            if info == IGMPConst.join:
                # IPPROTO_IGMP and already left state but re join -> re init ip_dict and archive previous state
                ip_str = convert_ip_bytes_string(ip)
                channel_info = get_channel_info(ip_str)
                logger.info(f'UDP stream re joined: {ip_str} ({channel_info}) in {timestamp}')
                ip_dict['active'] = False
                archived_stream_dict[ip].append(ip_dict)
                logger.info(f'Stream Archived!: {pformat(ip_dict, width=120)}')
                add_new_stream_ip(stream_dict, timestamp, protocol, ip, info)
                stream_dict[ip]['join_time'] = timestamp
            else:
                pass
                # IPPROTO_IGMP and already left state.

    else:
        if protocol == IPPROTO_IGMP and info == IGMPConst.leave:
            ip_str = convert_ip_bytes_string(ip)
            channel_info = get_channel_info(ip_str)
            logger.info(f'UDP stream leaved: {ip_str} ({channel_info}) in {timestamp}')
            ip_dict['joined'] = False
            ip_dict['leave_time'] = timestamp

        elif protocol == IPPROTO_UDP:
            ip_dict['deltas'].appendleft(timestamp - ip_dict['timestamp'])
            ip_dict['jitter'] = calc_jitter(ip_dict['jitter'], ip_dict['deltas'])

            calc_bitrate(ip_dict, packet_bytes)
            check_rtp_sequence(ip_dict, info)
            check_iso_iec_structure(ip_dict, timestamp, info)

        else:
            pass
            # IPPROTO_IGMP and joined already joined state.

    ip_dict['timestamp'] = timestamp


def change_stale_stream_state(current_timestamp: float, stream_dict: dict, archived_stream_dict: dict):
    thres_time = 0.5
    stale_ip_list = []
    for ip, ip_dict in stream_dict.items():
        if ip_dict['active'] and ip_dict['timestamp'] + thres_time < current_timestamp:
            ip_dict['active'] = False
            archived_stream_dict[ip].append(ip_dict)
            logger.info(f'Stream Archived!: {pformat(ip_dict, width=120)}')
            stale_ip_list.append(ip)
        else:
            pass

    # avoid list length change event in for loop
    for stale_ip in stale_ip_list:
        del stream_dict[stale_ip]


def init_archived_stream_dict() -> defaultdict:
    return defaultdict(list)


def read_pcap_and_update_dict(mongo_session: InsertToMongoDB, stream_dict: dict, path: str, archived_stream_dict: dict = None) -> dict:
    index = 0
    for timestamp, protocol, ip_target, info, packet_bytes in read_pcap_file(path):
        index += 1
        if ip_target not in stream_dict.keys():
            add_new_stream_ip(stream_dict, timestamp, protocol, ip_target, info)

        run_iptv_analysis(mongo_session, stream_dict, timestamp, protocol, ip_target, info, packet_bytes, archived_stream_dict)

        if index % 100 == 0:
            change_stale_stream_state(timestamp, stream_dict, archived_stream_dict)

    if index > 0:
        # no valid packet
        change_stale_stream_state(timestamp, stream_dict, archived_stream_dict)

    return stream_dict
