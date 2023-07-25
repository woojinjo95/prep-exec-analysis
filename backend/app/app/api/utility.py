import json
import math

from app.crud.base import load_paginate_from_mongodb, load_from_mongodb


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


def paginate_from_mongodb(collection, param, page, page_size=None, sorting_keyword=None, is_descending=None, projection=None):
    page_size = page_size if page_size else 30
    res = load_paginate_from_mongodb(collection=collection,
                                     param=param,
                                     page=page,
                                     page_size=page_size,
                                     projection=projection,
                                     sort_item=None if sorting_keyword is None else [(sorting_keyword, -1 if json.load(is_descending) else 1)])
    page_param = {
        'page': page,
        'page_size': page_size,
        'total': res.get('total', 1)
    }
    print(page_param)
    return convert_pageset(page_param, list(res.get('items', [])))


def get_multi_or_paginate_by_res(collection, param, page, page_size):
    if page:
        res_dict = paginate_from_mongodb(collection=collection, param=param,
                                         page=page, page_size=page_size)
    else:
        res = load_from_mongodb(collection=collection, param=param)
        res_dict = {
            "total": len(res),
            "pages": None,
            "prev": None,
            "next": None,
            "items": res
        }
    return res_dict
