from typing import Dict

from scripts.config.constant import RedisDB
from scripts.connection.redis_conn import get_value
from scripts.connection.mongo_db.crud import load_by_id_from_mongodb


def get_scenario_info() -> Dict:
    return {
        'scenario_id': get_value('testrun', 'scenario_id', '', db=RedisDB.hardware),
        'testrun_id': get_value('testrun', 'id', '', db=RedisDB.hardware),
    }


def load_testrun() -> Dict:
    scenario_info = get_scenario_info()
    scenario = load_by_id_from_mongodb(col='scenario', id=scenario_info['scenario_id'])
    testruns = scenario['testruns']
    index = next((i for i, item in enumerate(testruns) if item.get('id') == scenario_info['testrun_id']))  # find first index of testrun_id
    return testruns[index]
