import logging
import os
from ast import literal_eval

from redis import StrictRedis

from .constant import RedisDBEnum
from ..utils.docker import is_running_in_docker

logger = logging.Logger('main')


REDIS_HOST = os.getenv("REDIS_HOST", "redis") if is_running_in_docker() else 'localhost'
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


def get_strict_redis_connection(db=RedisDBEnum.media) -> StrictRedis:

    if len(REDIS_PASSWORD) > 0:
        return StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=db, password=REDIS_PASSWORD)
    else:
        return StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=db)


def parse_bytes_to_value(value: bytes) -> any:
    decoded = value.decode() if isinstance(value, bytes) else value
    try:
        value = literal_eval(decoded)
    except:
        value = decoded
    return value


def hget_value(sr_connection: StrictRedis, key: str, field: str = None, default: any = None) -> any:
    if field is None:
        return hget_all(sr_connection, key)
    value = sr_connection.hget(key, field)
    value = parse_bytes_to_value(value)
    if value is None:
        value = default
    return value


def hget_all(sr_connection: StrictRedis, name: str) -> dict:
    values = sr_connection.hgetall(name)
    result = {}
    for key, value in values.items():
        result[str(parse_bytes_to_value(key))] = parse_bytes_to_value(value)
    return result


def hset_value(sr_connection: StrictRedis, key: str, field: str, value: any):
    if value == 'None' or value == None:
        logger.warning(f'Nonetype or string "None" is interpreted as key is not exist.')
    value = sr_connection.hset(key, field, str(value))


def get_value(key: str, field: str = None, default: any = None, db=RedisDBEnum.media) -> any:
    with get_strict_redis_connection(db) as src:
        return hget_value(src, key, field, default)


def set_value(key: str, field: str = None, value: any = None, db=RedisDBEnum.media):
    with get_strict_redis_connection(db) as src:
        hset_value(src, key, field, value)
