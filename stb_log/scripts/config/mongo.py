from scripts.connection.redis_conn import get_value
from scripts.config.constant import RedisDB


def get_scenario_id() -> str:
    scenario_id = get_value('testrun', 'scenario_id', '', db=RedisDB.hardware)
    return scenario_id
