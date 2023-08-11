from ..connection.redis_connection import (get_strict_redis_connection,
                                           hget_value, hset_value)
from .constant import RedisDBEnum


def get_value(key: str, field: str = None, default: any = None, db=RedisDBEnum.media) -> any:
    with get_strict_redis_connection(db) as src:
        return hget_value(src, key, field, default)


def set_value(key: str, field: str = None, value: any = None, db=RedisDBEnum.media):
    with get_strict_redis_connection(db) as src:
        hset_value(src, key, field, value)
