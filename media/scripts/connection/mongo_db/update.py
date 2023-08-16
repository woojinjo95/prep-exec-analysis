from typing import Tuple

from .create import get_mongodb_collection


def update_to_mongodb(col: str, scenario_id: str, data: dict) -> Tuple[bool, str]:
    mongo_client = get_mongodb_collection(col)
    res = mongo_client.update_one({'id': scenario_id},
                                  {'$push': data})

    ''' mongo_client = get_mongodb_collection(col)
mongo_client.update_one({'id': 'scenario id'},
                        {'$push': {
                            'testrun.raw.videos': [
                                {
                                    'name': 'video name',
                                    'path': 'video path',
                                    'stat_path': 'json_path',
                                    'created_at': 1691640995.8489983
                                }
                            ]
                        }})
    '''
    upserted_id = res.upserted_id
    acknowledged = res.acknowledged
    return acknowledged, upserted_id
