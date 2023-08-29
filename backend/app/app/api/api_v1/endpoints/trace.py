import logging
import traceback
from typing import Optional

from app import schemas
from app.api.utility import convert_iso_format
from app.crud.base import aggregate_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/logcat", response_model=schemas.ReadLogcat)
def read_logcat(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
) -> schemas.ReadLogcat:
    """
    Logcat 로그 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                              '$lte': convert_iso_format(end_time)},
                                'scenario_id': scenario_id,
                                'testrun_id': testrun_id}},
                    {'$project': {'_id': 0, 'lines': 1}},
                    {'$unwind': {'path': '$lines'}},
                    {'$group': {'_id': None, 'items': {'$push': '$lines'}}}]
        aggregation_result = aggregate_from_mongodb(col='stb_log', pipeline=pipeline)
        log_list = aggregation_result[0].get('items', []) if aggregation_result != [] else aggregation_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": log_list}


@router.get("/network", response_model=schemas.ReadNetwork)
def read_network(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None, 
) -> schemas.ReadNetwork:
    """
    Network 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                              '$lte': convert_iso_format(end_time)},
                                'scenario_id': scenario_id,
                                'testrun_id': testrun_id}},
                    {'$project': {'_id': 0, 'lines': 1}},
                    {'$unwind': {'path': '$lines'}},
                    {'$group': {'_id': None, 'items': {'$push': '$lines'}}}]
        aggregation_result = aggregate_from_mongodb(col='network_trace', pipeline=pipeline)
        log_list = aggregation_result[0].get('items', []) if aggregation_result != [] else aggregation_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": log_list}
