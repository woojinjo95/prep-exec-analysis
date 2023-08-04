import logging

from datetime import datetime, timedelta
from app import schemas
from app.crud.base import aggregate_from_mongodb
from app.api.utility import get_multi_or_paginate_by_res
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/logcat", response_model=schemas.ReadLogcat)
def read_logcat_log(
    timeline: datetime,
    ) -> schemas.ReadLogcat:
    """
    Logcat 로그 조회
     - timeline: (datetime)YYYY-MM-DD HH:mm:SS
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
    return {"items": log_list}


@router.get("/network", response_model=schemas.NetworkPage)
def read_network_log(
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, ge=1, le=100, description="Page size")
    ) -> schemas.NetworkPage:
    """
    Network 로그 조회
    """
    return get_multi_or_paginate_by_res(col='network', page=page, page_size=page_size)

