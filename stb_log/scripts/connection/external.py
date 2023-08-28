from typing import Dict

from scripts.connection.redis_conn import get_value, set_value, get_all
from scripts.config.constant import RedisDB


def get_scenario_info() -> Dict:
    return {
        'scenario_id': get_value('testrun', 'scenario_id', '', db=RedisDB.hardware),
        'testrun_id': get_value('testrun', 'id', '', db=RedisDB.hardware),
    }


def set_connection_info(host: str, port: int, username: str, password: str, connection_mode: str) -> Dict:
    set_value('connection_info', 'host', host)
    set_value('connection_info', 'port', port)
    set_value('connection_info', 'username', username)
    set_value('connection_info', 'password', password)
    set_value('connection_info', 'connection_mode', connection_mode)


def get_connection_info() -> Dict:
    return get_all('connection_info')


def set_module_status(module_name: str, status: str):
    set_value('module_status', module_name, status)
