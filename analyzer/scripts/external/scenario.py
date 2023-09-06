from typing import Dict
from datetime import datetime

from scripts.config.constant import RedisDB
from scripts.connection.redis_conn import get_value
from scripts.connection.mongo_db.crud import load_by_id_from_mongodb, get_mongodb_collection


def get_scenario_info() -> Dict:
    return {
        'scenario_id': get_value('testrun', 'scenario_id', '', db=RedisDB.hardware),
        'testrun_id': get_value('testrun', 'id', '', db=RedisDB.hardware),
    }


def load_testrun() -> Dict:
    scenario_info = get_scenario_info()
    scenario = load_by_id_from_mongodb(col='scenario', id=scenario_info['scenario_id'])
    testruns = scenario['testruns']
    index = next((i for i, item in enumerate(testruns) if item.get('id') == scenario_info['testrun_id']), None)  # find first index of testrun_id
    return testruns[index]


def update_analysis_to_scenario(analysis_item: dict, analysis_last_time: datetime):
    scenario_info = get_scenario_info()
    scenario_id = scenario_info['scenario_id']
    testrun_id = scenario_info['testrun_id']

    mongo_client = get_mongodb_collection('scenario')

    doc = mongo_client.find_one({'id': scenario_id})
    testruns = doc.get('testruns', [])
    index = next((i for i, item in enumerate(testruns) if item.get('id') == testrun_id), None)

    # Fetch the existing 'measure_targets' list from MongoDB
    testrun = testruns[index]
    existing_measure_targets = testrun.get('measure_targets', [])
    # Check if an item with the same type exists
    for i, target in enumerate(existing_measure_targets):
        if target.get('type') == analysis_item['type']:
            # Update the item if it exists
            update_query = {f'testruns.{index}.measure_targets.{i}': analysis_item}
            mongo_client.update_one({'id': scenario_id}, {'$set': update_query})
            break
    # If not found, append the new element
    else:
        update_query = {f'testruns.{index}.measure_targets': analysis_item}
        mongo_client.update_one({'id': scenario_id}, {'$push': update_query})


    update_query = {
        f'testruns.{index}.last_updated_timestamp': analysis_last_time
    }
    mongo_client.update_one({'id': scenario_id}, {'$set': update_query})
