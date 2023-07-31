import pymongo
from app.core.config import settings
from fastapi.encoders import jsonable_encoder


def convert_to_dict(data):
    if not isinstance(data, dict):
        data = jsonable_encoder(data)
    return data


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_SERVER}:{settings.MONGODB_PORT}/{settings.MONGODB_NAME}?authSource={settings.MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


def get_mongodb_collection(col):
    db = settings.MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[col]
    return target_collection


def insert_to_mongodb(col, data):
    col = get_mongodb_collection(col)
    res = col.insert_one(convert_to_dict(data))
    return res


def load_from_mongodb(col, param={}, projection=None, sort_item=None):
    col = get_mongodb_collection(col)
    res = col.find(param, projection)
    if sort_item:
        res.sort(sort_item)
    return list(res)


def load_by_id_from_mongodb(col, id, projection=None):
    col = get_mongodb_collection(col)
    res = col.find_one({'id': id}, projection)
    return res


def update_by_id_to_mongodb(col, id, data):
    col = get_mongodb_collection(col)
    return col.update_one({'id': id}, {'$set': convert_to_dict(data)})

# TODO : 몽고디비 CRUD 정리


def insert_by_id_to_mongodb(col, id, data):
    col = get_mongodb_collection(col)
    return col.update_one({'id': id}, {'$push': convert_to_dict(data)})


def update_by_multi_filter_in_mongodb(col, param, data):
    col = get_mongodb_collection(col)
    return col.update_one(param, {'$set': convert_to_dict(data)})


def delete_by_id_to_mongodb(col, id):
    col = get_mongodb_collection(col)
    return col.delete_one({'id': id})


def load_paginate_from_mongodb(col, page, page_size, param={}, projection=None, sort_item=None):
    col = get_mongodb_collection(col)
    res = col.find(param, projection)
    if sort_item:
        res.sort(sort_item)
    return {'items': res.skip(page_size * (page - 1)).limit(page_size),
            'total': len(list(col.find(param, projection)))}  # TODO 카운트 방식 변경
