import pymongo
from .config import Settings
from typing import Dict, List


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{Settings.MONGODB_USERNAME}:{Settings.MONGODB_PASSWORD}@{Settings.MONGODB_SERVER}:{Settings.MONGODB_PORT}/{Settings.MONGODB_NAME}?authSource={Settings.MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


def get_mongodb_collection(col: str) -> pymongo.collection.Collection:
    db = Settings.MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[col]
    return target_collection


def insert_to_mongodb(col, data: Dict) -> pymongo.results.InsertOneResult:
    col = get_mongodb_collection(col)
    res = col.insert_one(data)
    return res


def insert_many_to_mongodb(col, data_list: List[Dict]) -> pymongo.results.InsertManyResult:
    col = get_mongodb_collection(col)
    res = col.insert_many(data_list)
    return res


def aggregate_from_mongodb(col, pipeline):
    col = get_mongodb_collection(col)
    return list(col.aggregate(pipeline))
