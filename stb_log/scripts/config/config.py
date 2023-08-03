from scripts.connection.redis import (get_strict_redis_connection,
                                           hget_value, hset_value)
from .constant import RedisDB


def get_value(key: str, field: str = None, default: any = None, db: int = RedisDB.stb_log) -> any:
    with get_strict_redis_connection(db) as src:
        return hget_value(src, key, field, default)


def set_value(key: str, field: str = None, value: any = None, db: int = RedisDB.stb_log):
    with get_strict_redis_connection(db) as src:
        hset_value(src, key, field, value)
