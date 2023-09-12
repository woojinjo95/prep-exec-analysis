import logging
import traceback
from typing import Optional

from app import schemas
from app.api.utility import convert_iso_format, paginate_from_mongodb_aggregation
from app.crud.base import aggregate_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/logcat", response_model=schemas.ReadLogcat)
def read_logcat(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
) -> schemas.ReadLogcat:
    """
    Logcat 로그 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        time_range = {}
        if start_time:
            time_range['$gte'] = convert_iso_format(start_time)
        if end_time:
            time_range['$lte'] = convert_iso_format(end_time)

        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')

        logcat_pipeline = [{'$match': {'timestamp': time_range,
                                       'scenario_id': scenario_id,
                                       'testrun_id': testrun_id}}]

        additional_pipeline = [
            {'$project': {'_id': 0, 'lines': 1}},
            {'$unwind': {'path': '$lines'}},
            {'$project': {'lines': {
                'timestamp': {'$dateToString': {'date': '$lines.timestamp'}},
                'module': '$lines.module',
                'log_level': '$lines.log_level',
                'process_name': '$lines.process_name',
                'pid': '$lines.pid',
                'tid': '$lines.tid',
                'message': '$lines.message'}}},
            {'$replaceRoot': {'newRoot': '$lines'}}]
        logcat_pipeline.extend(additional_pipeline)
        result = paginate_from_mongodb_aggregation(col='stb_log',
                                                   pipeline=logcat_pipeline,
                                                   page=page,
                                                   page_size=page_size,
                                                   sort_by=sort_by,
                                                   sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return result


@router.get("/network", response_model=schemas.ReadNetwork)
def read_network(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
) -> schemas.ReadNetwork:
    """
    Network 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        time_range = {}
        if start_time:
            time_range['$gte'] = convert_iso_format(start_time)
        if end_time:
            time_range['$lte'] = convert_iso_format(end_time)

        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')

        network_pipeline = [{'$match': {'timestamp': time_range,
                                        'scenario_id': scenario_id,
                                        'testrun_id': testrun_id}}]
        additional_pipeline = [
            {'$project': {'_id': 0, 'lines': 1}},
            {'$unwind': {'path': '$lines'}},
            {'$project': {'lines': {
                'timestamp': {'$dateToString': {'date': '$lines.timestamp'}},
                'src': '$lines.src',
                'dst': '$lines.dst',
                'protocol': '$lines.protocol',
                'length': '$lines.length',
                'info': '$lines.info'}}},
            {'$replaceRoot': {'newRoot': '$lines'}}]
        network_pipeline.extend(additional_pipeline)
        result = paginate_from_mongodb_aggregation(col='network_trace',
                                                   pipeline=network_pipeline,
                                                   page=page,
                                                   page_size=page_size,
                                                   sort_by=sort_by,
                                                   sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return result
