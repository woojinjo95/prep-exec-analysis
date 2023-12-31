import pymongo
from pymongo.collection import Collection
from typing import Tuple, List, Dict

from .config import Settings


def conn_mongodb() -> pymongo.MongoClient:
    client = pymongo.MongoClient(
        f"mongodb://{Settings.MONGODB_USERNAME}:{Settings.MONGODB_PASSWORD}@{Settings.MONGODB_SERVER}:{Settings.MONGODB_PORT}/{Settings.MONGODB_NAME}?authSource={Settings.MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


def get_mongodb_collection(col: str) -> Collection:
    db = Settings.MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[col]
    return target_collection


def insert_to_mongodb(col: str, data: Dict) -> Tuple[bool, str]:
    mongo_client = get_mongodb_collection(col)
    res = mongo_client.insert_one(data)
    # type(res) == pymongo.results.InsertOneResult

    inserted_id = str(res.inserted_id)
    acknowledged = res.acknowledged
    return acknowledged, inserted_id
