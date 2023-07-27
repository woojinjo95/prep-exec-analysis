import pymongo
from app.core.config import settings
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
    return res


def load_from_mongodb(collection, param, projection=None, sort_item=None):
    col = get_mongodb_collection(collection)
    res = col.find(param, projection)
    if sort_item:
        res.sort(sort_item)
    return list(res)


def load_by_id_from_mongodb(collection, id, projection=None):
    col = get_mongodb_collection(collection)
    res = col.find_one({'id': id}, projection)
    return res


def update_by_id_to_mongodb(collection, id, data):
    col = get_mongodb_collection(collection)
    return col.update_one({'id': id}, jsonable_encoder({'$set': data}))

# TODO : 몽고디비 CRUD 정리
def insert_by_id_to_mongodb(collection, id, data):
    col = get_mongodb_collection(collection)
    return col.update_one({'id': id}, jsonable_encoder({'$push': data}))


def update_by_multi_filter_in_mongodb(collection, param, data):
    col = get_mongodb_collection(collection)
    return col.update_one(param, jsonable_encoder({'$set': data}))


def delete_by_id_to_mongodb(collection, id):
    col = get_mongodb_collection(collection)
    return col.delete_one({'id': id})


def load_paginate_from_mongodb(collection, param, page, page_size, projection=None, sort_item=None):
    col = get_mongodb_collection(collection)
    res = col.find(param, projection)
    if sort_item:
        res.sort(sort_item)
    return {'items': res.skip(page_size * (page - 1)).limit(page_size),
            'total': len(list(col.find(param, projection)))}  # TODO 카운트 방식 변경
