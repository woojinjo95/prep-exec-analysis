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


'''

  pipeline = [{'$match': {'id': scenario_id, 'testruns.id': testrun_id}},
                        {'$unwind': "$testruns"},
                        {'$match': {"testruns.id": testrun_id}},
                        {'$unwind': "$testruns.raw.videos"},
                        {'$project': {'_id': 0, "path": "$testruns.raw.videos.path"}}]
            video = aggregate_from_mongodb(col='scenario', pipeline=pipeline)

            video_basename = os.path.basename(self.output_video_path)
            json_basenmae = os.path.basename(self.output_json_path)
'''


def update_video_info_to_scenario(col: str, scenario_id: str, testrun_id: str, data: dict) -> Tuple[bool, str]:

    try:
        # Connect to MongoDB and get the collection
        mongo_client = get_mongodb_collection(col)

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
            f'testruns.{index}.raw.videos': data
        }

        res = mongo_client.update_one({'id': scenario_id}, {'$push': update_query})
        if res.matched_count == 0:
            return False, "No matching document found"

        acknowledged = res.acknowledged
        upserted_id = res.upserted_id  # This will be None if no document was inserted

        return acknowledged, upserted_id

    except Exception as e:
        return False, str(e)
