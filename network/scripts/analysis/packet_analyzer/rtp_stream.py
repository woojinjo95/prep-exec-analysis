import time
from collections import defaultdict, deque
from typing import Iterable

DELTA_MAX_COUNT = 2


def get_default_ip_info(start_timestamp: float = time.time(), start_rtp_sequence: int = -1) -> dict:
    ip_dict = {'active': True,
               'joined': False,
               'timestamp': start_timestamp,
               'start_timestamp': start_timestamp,
               'rtp_sequence': start_rtp_sequence,
               'join_time': 0,
               'leave_time': 0,
               'join_interval': 0,
               'leave_interval': 0,
               'count': 0,
               'bytes': 0,
               'bitrate': {'avg': 0,
                           'min': 0,
                           'max': 0, },
               'jitter': 0,
               'deltas': deque(maxlen=DELTA_MAX_COUNT),
               'rtp_errors': 0,
               'continuous_count': {},
               'errors': {'ts_sync_loss': 0,
                          'ts_consecutive': 0,
                          'sync_bytes': 0,
                          'pat': 0,
                          'pmt': 0,
                          'pid': 0,
                          'continuous_count': defaultdict(int), },
               'timer': {
                   'pat': start_timestamp,
                   'pmt': start_timestamp,
               },
               'stream_info':
               {
                   'pmt': {},
                   'pid': {},
               }
               }

    ip_dict['deltas'].append(0)

    return ip_dict


def calc_jitter(jitter: float, deltas: Iterable[float]):
    # RFC 1889
    return jitter + (abs(deltas[1] - deltas[0]) - jitter) / 16


def calc_bitrate(ip_dict: dict, packet_bytes: bytes):
    try:
        bitrate = ip_dict['count'] * len(packet_bytes) * 8 / (ip_dict['timestamp'] -
                                                              ip_dict['start_timestamp'])
        if ip_dict['count'] > 1000 and ip_dict['count'] % 20 == 19:
            ip_dict['bitrate']['avg'] = bitrate
            ip_dict['bitrate']['min'] = min(bitrate, ip_dict['bitrate']['min'])
            ip_dict['bitrate']['max'] = max(bitrate, ip_dict['bitrate']['max'])
        else:
            ip_dict['bitrate']['min'] = bitrate
    except ZeroDivisionError:
        pass
