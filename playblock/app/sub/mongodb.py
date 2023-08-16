import os
import pymongo
from bson.objectid import ObjectId


MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "admin")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", ".nextlab6318!")
MONGODB_SERVER = os.getenv("MONGODB_SERVER", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_NAME = os.getenv("MONGODB_NAME", "prep-exec-analysis")
MONGODB_AUTHENTICATION_SOURCE = os.getenv("MONGODB_AUTHENTICATION_SOURCE", "admin")

MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "scenario")


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_SERVER}:{MONGODB_PORT}/{MONGODB_NAME}?authSource={MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


def get_collection(collection=MONGODB_COLLECTION_NAME) -> pymongo.collection.Collection:
    db = MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[collection]
    return target_collection

# class Block:
#     type: str
#     name: str
#     args: list[dict]
#     delay_time: int
#     id: str

# class BlockGroup:
#     repeat_cnt: int
#     block: list[Block]

# class Scenario:
#     _id: ObjectId
#     block_group: list[BlockGroup]
#     repeat_cnt: int -> 신규 / 데이터구조가 아니라 실행시 반복 설정일 수 있음



if __name__ == '__main__':
    col: pymongo.collection.Collection = get_collection()
    res = col.find_one({'_id': ObjectId('64d9bf3caeb91b6a6ef87810')})

    exec_block_plan = []
    for loop_cnt in range(res['repeat_cnt']):
        print(f"name: {res['name']} loop_cnt: {loop_cnt}")
        for block_group in res['block_group']:
            for block_loop_cnt in range(block_group['repeat_cnt']):
                for block_item in block_group['block']:
                    print(f"block: {block_item['name']} block_loop_cnt: {block_loop_cnt}")
                    exec_block_plan.append(block_item)
    
    print(len(exec_block_plan))