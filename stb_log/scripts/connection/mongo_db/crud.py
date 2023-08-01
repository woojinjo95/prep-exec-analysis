import pymongo
from .config import Settings
from scripts.util.common import convert_to_dict


def conn_mongodb():
    client = pymongo.MongoClient(
        f"mongodb://{Settings.MONGODB_USERNAME}:{Settings.MONGODB_PASSWORD}@{Settings.MONGODB_SERVER}:{Settings.MONGODB_PORT}/{Settings.MONGODB_NAME}?authSource={Settings.MONGODB_AUTHENTICATION_SOURCE}&readPreference=primary&ssl=false")
    return client


def get_mongodb_collection(col):
    db = Settings.MONGODB_NAME
    client = conn_mongodb()
    result_db = client[db]
    target_collection = result_db[col]
    return target_collection


def insert_to_mongodb(col, data):
    col = get_mongodb_collection(col)
    res = col.insert_one(data)
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


def delete_part_by_id_to_mongodb(col, id, data):
    col = get_mongodb_collection(col)
    return col.update_one({'id': id}, {'$pull': convert_to_dict(data)})


def load_paginate_from_mongodb(col, page, page_size, param={}, projection=None, sort_item=None):
    col = get_mongodb_collection(col)
    res = col.find(param, projection)
    if sort_item:
        res.sort(sort_item)
    return {'items': res.skip(page_size * (page - 1)).limit(page_size),
            'total': len(list(col.find(param, projection)))}  # TODO 카운트 방식 변경
