import os

import pymongo
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST", "")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "")

MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
MONGODB_SERVER = os.getenv("MONGODB_SERVER", "")
MONGODB_PORT = os.getenv("MONGODB_PORT", 27017)
MONGODB_NAME = os.getenv("MONGODB_NAME", "")
MONGODB_AUTHENTICATION_SOURCE = os.getenv("MONGODB_AUTHENTICATION_SOURCE", "")


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


def get_collection(collection) -> pymongo.collection.Collection:
    db = MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[collection]
    return target_collection
