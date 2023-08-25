import subprocess
from collections import namedtuple

from ..connection.redis_connection import (get_strict_redis_connection,
                                           hget_value, hset_value)
from .constant import RedisDBEnum
from ..info.network_info import get_private_ip, get_gateway_ip, get_public_ip

NICInfo = namedtuple('nic_info', ('wan', 'stb', 'wifi'))


def get_default_nic_names() -> NICInfo:
    physical_devices_list = subprocess.check_output('ls -l /sys/class/net/ | grep -v virtual | awk -F\' \' \'{print $9}\'',
                                                    shell=True,
                                                    encoding='utf-8').split()
    physical_devices_list += [None] * 3  # padding
    wan, stb, wifi = physical_devices_list[:3]
    return NICInfo(wan, stb, wifi)


nic_info = get_default_nic_names()

settings = {'network': {
    'br_nic': 'br0',
    'wan_nic': nic_info.wan,
    'stb_nic': nic_info.stb,
    'wifi_nic': nic_info.wifi,
    'segment_interval': 10,
    'rotation_interval': 1800,
    'provider': 'sk',
}}

hardware_settings = {'hardware_configuration': {
    'ssh_port': 2345,
    'private_ip': get_private_ip(),
    'public_ip': get_public_ip(),
    'gateway_ip': get_gateway_ip('br0'),
    'dut_ip': '',
}}


def initialize_keys(db: int, settings: dict):
    with get_strict_redis_connection(db) as con:
        for key, fields in settings.items():
            for field, value in fields.items():
                if hget_value(con, key, field) is None:
                    hset_value(con, key, field, value)


def init_configs():
    initialize_keys(RedisDBEnum.hardware, hardware_settings)
    initialize_keys(RedisDBEnum.media, settings)
