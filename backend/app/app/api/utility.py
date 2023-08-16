import json
import math
import os
import time
from ast import literal_eval

from app.core.config import settings
from app.crud.base import load_from_mongodb, load_paginate_from_mongodb


def convert_pageset(page_param, res):
    page = page_param['page']
    page_size = page_param['page_size']
    total = page_param['total']
    pages = math.ceil(total / page_size)

    return {
        "total": total,
        "pages": pages,
        "prev": None if page == 1 or page > pages else page - 1,
        "next": None if page >= pages else page + 1,
        "items": res
    }


def paginate_from_mongodb(col, page, page_size=None, param={}, sorting_keyword=None, is_descending=False, proj=None):
    page_size = page_size if page_size else 30
    res = load_paginate_from_mongodb(
        col=col, page=page, page_size=page_size, param=param, proj=proj, sort_item=None
        if sorting_keyword is None else [(sorting_keyword, -1 if is_descending else 1)])
    page_param = {
        'page': page,
        'page_size': page_size,
        'total': res.get('total', 1)
    }
    return convert_pageset(page_param, list(res.get('items', [])))


def get_multi_or_paginate_by_res(col, page, page_size, sorting_keyword=None, is_descending=None, proj=None, param={}):
    if page:
        res_dict = paginate_from_mongodb(col=col,
                                         page=page, page_size=page_size,
                                         param=param,
                                         sorting_keyword=sorting_keyword,
                                         is_descending=is_descending,
                                         proj=proj)
    else:
        res = load_from_mongodb(col=col, param=param, proj=proj)
        res_dict = {
            "total": len(res),
            "pages": None,
            "prev": None,
            "next": None,
            "items": res
        }
    return res_dict


def classify_file_type(file_name):
    file_exp = file_name.split('.')[-1]
    if file_exp in ['jpg', 'png', 'jpeg', 'gif']:
        file_dir = os.path.join(settings.FILES_PATH, 'images')
    elif file_exp in ['mp4', 'avi']:
        file_dir = os.path.join(settings.FILES_PATH, 'videos')
    else:
        file_dir = os.path.join(settings.FILES_PATH, 'etc')
    return file_dir


def parse_bytes_to_value(value: bytes) -> any:
    decoded = value.decode() if isinstance(value, bytes) else value
    try:
        value = literal_eval(decoded)
    except:
        value = decoded
    return value


def set_redis_pub_msg(msg: str, data: dict = {}, service: str = 'backend', level: str = 'info'):
    return json.dumps({
        "service": service,
        "level": level,
        "time": time.time(),
        "msg": msg,
        "data": data
    })
