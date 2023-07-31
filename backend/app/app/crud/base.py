from app.core.config import settings
from app.db.session import db_session
from fastapi.encoders import jsonable_encoder


def convert_to_dict(data):
    if not isinstance(data, dict):
        data = jsonable_encoder(data)
    return data


def get_mongodb_collection(col):
    db = settings.MONGODB_NAME
    result_db = db_session[db]
    target_collection = result_db[col]
    return target_collection


def insert_to_mongodb(col, data):
    col = get_mongodb_collection(col)
    res = col.insert_one(convert_to_dict(data))
    return res


def load_from_mongodb(col, param={}, proj=None, sort_item=None):
    col = get_mongodb_collection(col)
    res = col.find(param, proj)
    if sort_item:
        res.sort(sort_item)
    return list(res)


def load_by_id_from_mongodb(col, id, proj=None):
    col = get_mongodb_collection(col)
    res = col.find_one({'id': id}, proj)
    return res


def load_one_from_mongodb(col, proj=None):
    col = get_mongodb_collection(col)
    res = col.find_one(projection=proj)
    return res


def load_paginate_from_mongodb(col, page, page_size, param={}, proj=None, sort_item=None):
    col = get_mongodb_collection(col)
    res = col.find(param, proj)
    if sort_item:
        res.sort(sort_item)
    return {'items': res.skip(page_size * (page - 1)).limit(page_size),
            'total': col.count_documents(param)}


def update_to_mongodb(col, param, data):
    col = get_mongodb_collection(col)
    return col.update_one(param, {'$set': convert_to_dict(data)})


def update_by_id_to_mongodb(col, id, data):
    col = get_mongodb_collection(col)
    return col.update_one({'id': id}, {'$set': convert_to_dict(data)})


def update_many_to_mongodb(col, param={}, data={}):
    col = get_mongodb_collection(col)
    return col.update_many(param, {'$set': convert_to_dict(data)})


def insert_by_id_to_mongodb_array(col, id, data):
    col = get_mongodb_collection(col)
    return col.update_one({'id': id}, {'$push': convert_to_dict(data)})


def delete_part_to_mongodb(col, param, data):
    col = get_mongodb_collection(col)
    return col.update_one(param, {'$pull': convert_to_dict(data)})


def delete_part_by_id_to_mongodb(col, id, data):
    col = get_mongodb_collection(col)
    return col.update_one({'id': id}, {'$pull': convert_to_dict(data)})


def delete_by_id_to_mongodb(col, id):
    col = get_mongodb_collection(col)
    return col.delete_one({'id': id})
