from typing import Dict, Tuple

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


def update_analysis_to_scenario(data: dict) -> Tuple[bool, str]:
    try:
        scenario_info = get_scenario_info()
        scenario_id = scenario_info['scenario_id']
        testrun_id = scenario_info['testrun_id']

        # Connect to MongoDB and get the collection
        mongo_client = get_mongodb_collection('scenario')

        # Find the index of the testrun with the specific id
        doc = mongo_client.find_one({'id': scenario_id})
        if doc is None:
            return False, "No document with the given parent_id found"

        testruns = doc.get('testruns', [])

        index = next((i for i, item in enumerate(testruns) if item.get('id') == testrun_id), None)
        if index is None:
            return False, "No testrun with the given testrun_id found"

        # Update the specific testrun
        update_query = {
            f'testruns.{index}.analysis.targets': data
        }

        res = mongo_client.update_one({'id': scenario_id}, {'$push': update_query})
        if res.matched_count == 0:
            return False, "No matching document found"

        acknowledged = res.acknowledged
        upserted_id = res.upserted_id  # This will be None if no document was inserted

        return acknowledged, upserted_id

    except Exception as e:
        return False, str(e)
