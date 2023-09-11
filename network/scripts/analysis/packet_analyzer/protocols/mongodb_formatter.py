def format_igmp_join(timestamp: float, ip: str, channel_info: str) -> dict:
    return {'type': 'igmp_join',
            'timestamp': timestamp,
            'ip': ip,
            'channel_info': channel_info}


def format_igmp_leave(timestamp: float, ip: str, channel_info: str) -> dict:
    return {'type': 'igmp_leave',
            'timestamp': timestamp,
            'ip': ip,
            'channel_info': channel_info}


def format_udp_stream_start(timestamp: float, ip: str, channel_info: str) -> dict:
    return {'type': 'udp_start',
            'timestamp': timestamp,
            'ip': ip,
            'channel_info': channel_info}


def format_udp_stream_stop(timestamp: float, ip: str, channel_info: str) -> dict:
    return {'type': 'udp_stop',
            'timestamp': timestamp,
            'ip': ip,
            'channel_info': channel_info}


def format_udp_stream_stop_and_summary(timestamp: float, ip: str, channel_info: str, summary: dict) -> dict:
    return {'type': 'udp_start',
            'timestamp': timestamp,
            'ip': ip,
            'channel_info': channel_info,
            'summary': summary}