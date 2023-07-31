import os
from ast import literal_eval
from redis import Redis, StrictRedis

# from ..scripts.util.common import get_dotenvs_value
from scripts.util.common import get_dotenvs_value

env_path = '../.env'
redis_host = os.environ.get('REDIS_HOST') or 'localhost'
redis_port = os.environ.get('REDIS_PORT') or get_dotenvs_value(env_path, 'REDIS_PORT')
redis_password = os.environ.get('REDIS_PASSWORD') or get_dotenvs_value(env_path, 'REDIS_PASSWORD')
default_redis_db = 0


def get_redis_connection(db=default_redis_db) -> Redis:
    return Redis(host=redis_host, port=redis_port, db=db, password=redis_password)


def get_strict_redis_connection(db=default_redis_db) -> StrictRedis:
    return StrictRedis(host=redis_host, port=redis_port, db=db, password=redis_password)


def hget_value(sr_connection: StrictRedis, name: str, key: str) -> any:
    value = sr_connection.hget(name, key)
    if type(value) == bytes:
        decoded = value.decode()
    else:
        decoded = value
    try:
        value = literal_eval(decoded)
    except:
        value = decoded
    return value


def hset_value(sr_connection: StrictRedis, name: str, key: str, value: str) -> any:
    value = sr_connection.hset(name, key, value)
