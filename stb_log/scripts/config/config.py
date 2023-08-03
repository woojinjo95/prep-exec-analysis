from scripts.connection.redis import (get_strict_redis_connection,
                                           hget_value, hset_value)
 


def get_value(db: int, key: str, field: str = None, default: any = None) -> any:
    with get_strict_redis_connection(db) as src:
        return hget_value(src, key, field, default)


def set_value(db: int, key: str, field: str = None, value: any = None):
    with get_strict_redis_connection(db) as src:
        hset_value(src, key, field, value)
