

import os
import asyncio
import redis.asyncio as redis
import copy
import pymongo
from bson.objectid import ObjectId

REDIS_HOST = os.getenv("REDIS_HOST", "192.168.1.45")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", '66b44dcb7f981904f8536b19e4464725')
CHANNEL_NAME = os.getenv("CHANNEL_NAME", 'command')

MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "admin")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", ".nextlab6318!")
MONGODB_SERVER = os.getenv("MONGODB_SERVER", "192.168.1.45")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_NAME = os.getenv("MONGODB_NAME", "prep-exec-analysis")
MONGODB_AUTHENTICATION_SOURCE = os.getenv("MONGODB_AUTHENTICATION_SOURCE", "admin")

MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "scenario")


async def get_redis_pool():
    return await redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_SERVER}:{MONGODB_PORT}/{MONGODB_NAME}?authSource={MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


def get_db():
    db = MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    return result_db


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
    # scenario: pymongo.collection.Collection = get_collection('scenario')
    blockrun: pymongo.collection.Collection = get_collection('blockrun')
    # res = col.find_one({'_id': ObjectId('64d9bf3caeb91b6a6ef87810')})
    # res = scenario.find_one({'id': '5e731960-616a-436e-9cad-84fdbb39bbf4'})



    # # print(len(exec_block_plan))

    # # # print(block['name'])
    # blockrun.insert_one({
    #     "testrun": '2023-08-14T054428F718593',
    #     "scenario": "5e731960-616a-436e-9cad-84fdbb39bbf4",
    #     "blocks": exec_block_plan
    # })

    res = blockrun.find_one({'scenario': '5e731960-616a-436e-9cad-84fdbb39bbf4'})
    for block in res['blocks']:
        print(block)
        ret = blockrun.update_one(
            { "scenario": '5e731960-616a-436e-9cad-84fdbb39bbf4', "blocks.idx": block['idx']},
            { "$set": { "blocks.$.run": True}}
        )
        print(ret.matched_count)


# async def main():
#     rd = await redis.Redis(
#         host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)

#     print(await rd.hgetall("testrun"))


# asyncio.run(main())
