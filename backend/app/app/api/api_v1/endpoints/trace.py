import logging

from app import schemas
from app.crud.base import aggregate_from_mongodb
from fastapi import APIRouter, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/logcat", response_model=schemas.ReadLogcat)
def read_logcat(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00')
    ) -> schemas.ReadLogcat:
    """
    Logcat 로그 조회
    """
    pipeline = [{'$match': {'time': {'$gte': start_time, '$lte': end_time}}},
                {'$unwind': {'path': '$lines'}},
                {'$group': {'_id': None, 'items': {'$push': '$lines'}}},
                ]
    aggregation_result = aggregate_from_mongodb(col='stb_log', pipeline=pipeline)
    log_list = aggregation_result[0].get('items', []) if aggregation_result != [] else aggregation_result
    return {"items": log_list}


@router.get("/network", response_model=schemas.ReadNetwork)
def read_network(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00')
    ) -> schemas.ReadNetwork:
    """
    Network 조회
    """
    pipeline = [{'$match': {'time': {'$gte': start_time, '$lte': end_time}}},
                {'$unwind': {'path': '$lines'}},
                {'$group': {'_id': None,'items': {'$push': '$lines'}}},
                ]
    aggregation_result = aggregate_from_mongodb(col='network', pipeline=pipeline)
    log_list = aggregation_result[0].get('items', []) if aggregation_result != [] else aggregation_result
    return {"items": log_list}

