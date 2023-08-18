from ..connection.redis_connection import (get_strict_redis_connection,
                                           hget_value, hset_value)
from .constant import RedisDBEnum

settings = {'network': {
    'target_nic': 'enx00e09900866a',
    'segment_interval': 10,
    'rotation_interval': 1800,
    'provider': 'sk',
}}

hardware_settings = {'hardware_configuration': {'ssh_port': 2345}}


def initialize_keys(db: int, settings: dict):
    with get_strict_redis_connection(db) as con:
        for key, fields in settings.items():
            for field, value in fields.items():
                if hget_value(con, key, field) is None:
                    hset_value(con, key, field, value)


def init_configs():
    initialize_keys(RedisDBEnum.hardware, hardware_settings)
    initialize_keys(RedisDBEnum.media, settings)
