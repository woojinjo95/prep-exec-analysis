import pymongo
from app.core.config import settings
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_SERVER}:{settings.MONGODB_PORT}/{settings.MONGODB_NAME}?authSource={settings.MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client

def get_mongodb_collection(collection):
    db = settings.MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[collection]
    return target_collection


def insert_to_mongodb(collection, data):
    col = get_mongodb_collection(collection)
    res = col.insert_one(jsonable_encoder(data))
    return str(res.inserted_id)


def load_from_mongodb(collection, param, projection=None, sort_item=None):
    col = get_mongodb_collection(collection)
    res = col.find(param, projection)
    if sort_item is not None:
        res.sort(sort_item)
    return list(res)


def load_by_id_from_mongodb(collection, id, projection=None):
    col = get_mongodb_collection(collection)
    res = col.find_one({'_id': ObjectId(id)}, projection)
    return res


def update_by_id_to_mongodb(collection, id, data):
    col = get_mongodb_collection(collection)
    return col.update_one({'_id': ObjectId(id)}, jsonable_encoder({'$set': data}))


def delete_by_id_to_mongodb(collection, id):
    col = get_mongodb_collection(collection)
    return col.delete_one({'_id': ObjectId(id)})

# TODO 페이지네이션 함수 추가