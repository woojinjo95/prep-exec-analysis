import json
import logging
import traceback

from app import schemas
from app.api.utility import parse_bytes_to_value, set_redis_pub_msg
from app.crud.base import aggregate_from_mongodb
from app.db.redis_session import RedisClient
from app.schemas.enum import ShellModeEnum
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.ShellList)
def get_shell_modes() -> schemas.ShellList:
    """
    터미널 목록
    """
    pipeline = [{'$group': {'_id': {'mode': '$mode', 'shell_id': '$shell_id'}}},
                {'$replaceRoot': {'newRoot': "$_id"}}]
    return {'items': aggregate_from_mongodb(col="shell_log", pipeline=pipeline)}


@router.get("/logs", response_model=schemas.ShellLogList)
def get_shell_logs(
    shell_mode: ShellModeEnum,
    shell_id: str,
    start_time: str = Query(..., description="ex.2009-02-13T23:31:30"),
    end_time: str = Query(..., description="ex.2009-02-13T23:31:30"),
) -> schemas.ShellLogList:
    """
    터미널별 일정기간 로그 조회
    """
    pipeline = [{'$match': {'time': {'$gte': start_time, '$lte': end_time}, 'mode': shell_mode.value, 'shell_id': shell_id}},
                {'$project': {'_id': 0, 'lines': 1}},
                {'$unwind': {'path': '$lines'}},
                {'$group': {'_id': None, 'lines': {'$push': '$lines'}}}]
    result = aggregate_from_mongodb(col="shell_log", pipeline=pipeline)
    return {'items': result if result == [] else result[0]['lines']}


@router.post("/connect", response_model=schemas.Msg)
def connect_shell() -> schemas.Msg:
    """
    Connect shell.
    """
    conn_info = RedisClient.hget('hardware_configuration', 'stb_connection')
    if conn_info is None or parse_bytes_to_value(conn_info) is None:
        raise HTTPException(
            status_code=404, detail="The stb_connection does not exist in the system.")
    try:
        conn_info = json.loads(conn_info)
        RedisClient.publish('command', set_redis_pub_msg(msg="connect_shell",
                                                         data={"mode": conn_info.get('type', None),
                                                               "host": conn_info.get('ip', None),
                                                               "port": conn_info.get('port', None),
                                                               "username": conn_info.get('username', None),
                                                               "password": conn_info.get('password', None)}))
        # TODO shell 응답
    except Exception as e:
        pass
        # raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Connect shell'}


@router.post("/disconnect", response_model=schemas.Msg)
def disconnect_shell() -> schemas.Msg:
    """
    Disconnect shell.
    """
    try:
        RedisClient.publish('command', set_redis_pub_msg(msg="disconnect_shell"))
    # TODO shell 응답
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())

    return {'msg': 'Disconnect shell'}
