import os
from ast import literal_eval

from scripts.connection.redis_conn import (get_strict_redis_connection,
                                           hget_value, hset_value)
from .constant import RedisDB


def get_value(key: str, field: str = None, default: any = None, db: int = RedisDB.stb_log) -> any:
    with get_strict_redis_connection(db) as src:
        return hget_value(src, key, field, default)


def set_value(key: str, field: str = None, value: any = None, db: int = RedisDB.stb_log):
    with get_strict_redis_connection(db) as src:
        hset_value(src, key, field, value)


def get_setting_with_env(key: str, default: str = None):
    try:
        value = os.getenv(key, default)
        if value is None:
            return None
        try:
            decoded = literal_eval(value)
        except Exception:
            decoded = value
        return decoded
    except Exception:
        return default
    