import logging

from datetime import datetime, timedelta
from app import schemas
from app.crud.base import (load_from_mongodb, load_paginate_from_mongodb, aggregate_from_mongodb)
from app.api.utility import get_multi_or_paginate_by_res, convert_pageset
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/logcat_trace", response_model=schemas.LogcatPage)
def read_logcat_log(
    timeline: datetime,
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, ge=1, le=100, description="Page size"),
    ):
    """
    Logcat 로그 조회
     - timeline: (datetime)YYYY-MM-DD HH:mm:SS
     - page: (int)Page number
     - page_size: (int)Page size
    """
    second_range = 10
    start_time = timeline - timedelta(seconds=second_range)
    end_time = timeline + timedelta(seconds=second_range)
    pipeline = [
        {
            '$match': {
                'time': {
                    '$gte': str(start_time), 
                    '$lte': str(end_time)
                }
            }
        }, {
            '$unwind': {
                'path': '$lines'
            }
        }, {
            '$group': {
                '_id': None,
                'items': {
                    '$push': '$lines'
                }
            }
        }, {
            '$project': {'_id': 0}
        }
    ]
    log_list = list(aggregate_from_mongodb(col='logcat', pipeline=pipeline))[0].get('items', [])
    page_param = {
        'page': page,
        'page_size': page_size,
        'total': len(log_list)
    }
    # TODO: 페이징 안되고 있음, 파이프라인 내에서 페이징 필요
    current_index = page_param['total']
    return convert_pageset(page_param=page_param, res= log_list)




@router.get("/network_trace", response_model=schemas.NetworkPage)
def read_network_log(
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, ge=1, le=100, description="Page size")
    ) -> schemas.NetworkPage:
    """
    Network 로그 조회
    """
    return get_multi_or_paginate_by_res(col='network', page=page, page_size=page_size)

