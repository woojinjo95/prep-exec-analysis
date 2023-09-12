from typing import Tuple

from ..configs.config import get_value, set_value
from ..configs.constant import RedisChannel
from ..connection.redis_pubsub import get_strict_redis_connection, publish
from .main import get_epg_data


def get_epg_data_with_provider(provider: str, *args):
    epg_data = get_epg_data(*args)

    if len(epg_data) > 0:
        channel_info_dict = {ip: [_id, number, name, port, region] for _id, number, provider, ip, port, name, region in epg_data}

        set_value('channel_info', provider, channel_info_dict)

    with get_strict_redis_connection() as redis_connection:
        publish(redis_connection, RedisChannel.command, {'msg': 'epg_update_response',
                                                         'data': {'log': f'Provider {provider}\'s list updated: {len(channel_info_dict)}'}})


def get_channel_info(ip_str: str) -> str:
    provider = get_value('network', 'provider')
    channel_dict = get_value('channel_info', provider, {})

    channel_info = channel_dict.get(ip_str, None)
    if channel_info is None:
        channel_info_str = ''
    else:
        _id, number, name, port, region = channel_info
        channel_info_str = f'{name} ({number}), id: {_id}'

    return channel_info_str 
