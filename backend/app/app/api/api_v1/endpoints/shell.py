import logging
import traceback
from typing import Optional

from app import schemas
from app.api.utility import (convert_iso_format, parse_bytes_to_value,
                             set_redis_pub_msg, paginate_from_mongodb_aggregation)
from app.crud.base import aggregate_from_mongodb
from app.db.redis_session import RedisClient
from app.schemas.enum import ShellModeEnum
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.ShellList)
def get_shell_modes(
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None
) -> schemas.ShellList:
    """
    터미널 목록
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')

        pipeline = [{'$match': {'scenario_id': scenario_id, 'testrun_id': testrun_id}},
                    {'$group': {'_id': {'mode': '$mode', 'shell_id': '$shell_id'}}},
                    {'$replaceRoot': {'newRoot': "$_id"}}]
        res = aggregate_from_mongodb(col="shell_log", pipeline=pipeline)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': res}


@router.get("/logs", response_model=schemas.ShellLogList)
def get_shell_logs(
    shell_mode: ShellModeEnum,
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    터미널별 일정기간 로그 조회
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

        terminal_log_pipeline = [{'$match': {'timestamp': time_range,
                                             'scenario_id': scenario_id,
                                             'testrun_id': testrun_id,
                                             'mode': shell_mode.value}}]
        additional_pipeline = [{'$project': {'_id': 0, 'lines': 1}},
                               {'$unwind': {'path': '$lines'}},
                               {'$project': {'lines': {
                                   'timestamp': {'$dateToString': {'date': '$lines.timestamp'}},
                                   'module': '$lines.module',
                                   'message': '$lines.message'}}},
                               {'$replaceRoot': {'newRoot': '$lines'}}]
        terminal_log_pipeline.extend(additional_pipeline)
        result = paginate_from_mongodb_aggregation(col='shell_log',
                                                   pipeline=terminal_log_pipeline,
                                                   page=page,
                                                   page_size=page_size,
                                                   sort_by=sort_by,
                                                   sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return result


@router.post("/connect", response_model=schemas.Msg)
def connect_shell() -> schemas.Msg:
    """
    Connect shell.
    """
    conn_info = RedisClient.hgetall('stb_connection')
    if conn_info is None or parse_bytes_to_value(conn_info) is None:
        raise HTTPException(
            status_code=404, detail="The stb_connection does not exist in the system.")
    try:
        RedisClient.publish('command', set_redis_pub_msg(msg="connect_shell",
                                                         data={"mode": conn_info.get('mode', None),
                                                               "host": conn_info.get('host', None),
                                                               "port": conn_info.get('port', None),
                                                               "username": conn_info.get('username', None),
                                                               "password": conn_info.get('password', None)}))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Connect shell'}


@router.post("/disconnect", response_model=schemas.Msg)
def disconnect_shell() -> schemas.Msg:
    """
    Disconnect shell.
    """
    try:
        RedisClient.publish('command', set_redis_pub_msg(msg="disconnect_shell"))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Disconnect shell'}
