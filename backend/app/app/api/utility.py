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


def paginate_from_mongodb(col, page, page_size=None, param={}, sorting_keyword=None, is_descending=None, proj=None):
    page_size = page_size if page_size else 30
    res = load_paginate_from_mongodb(col=col,
                                     page=page,
                                     page_size=page_size,
                                     param=param,
                                     proj=proj,
                                     sort_item=None if sorting_keyword is None else [(sorting_keyword, -1 if json.load(is_descending) else 1)])
    page_param = {
        'page': page,
        'page_size': page_size,
        'total': res.get('total', 1)
    }
    return convert_pageset(page_param, list(res.get('items', [])))


def get_multi_or_paginate_by_res(col, page, page_size, param={}):
    if page:
        res_dict = paginate_from_mongodb(col=col,
                                         page=page, page_size=page_size,
                                         param=param)
    else:
        res = load_from_mongodb(col=col, param=param)
        res_dict = {
            "total": len(res),
            "pages": None,
            "prev": None,
            "next": None,
            "items": res
        }
    return res_dict
