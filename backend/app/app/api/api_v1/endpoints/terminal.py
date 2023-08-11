import logging

from app import schemas
from app.crud.base import aggregate_from_mongodb
from app.schemas.enum import ShellTypeEnum
from fastapi import APIRouter, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.TerminalList)
def get_terminal_modes() -> schemas.TerminalList:
    """
    터미널 목록
    """
    pipeline = [{'$group': {'_id': {'mode': '$mode', 'shell_id': '$shell_id'}}},
                {'$replaceRoot': {'newRoot': "$_id"}}]
    return{'items': aggregate_from_mongodb(col="shell_log", pipeline=pipeline)}



@router.get("/logs", response_model=schemas.TerminalLogList)
def get_terminal_logs(
    terminal_mode: ShellTypeEnum,
    shell_id: str,
    start_time: str = Query(..., description="ex.2009-02-13T23:31:30"),
    end_time: str = Query(..., description="ex.2009-02-13T23:31:30"),
    ) -> schemas.TerminalLogList:
    """
    터미널별 일정기간 로그 조회
    """

    pipeline = [{'$match': {'time': {'$gte': start_time, '$lte': end_time}, 'mode': terminal_mode.value, 'shell_id': shell_id}},
                {'$project': {'_id': 0, 'lines': 1}},
                {'$unwind': {'path': '$lines'}},
                {'$group': {'_id': None, 'lines': {'$push': '$lines'}}}]
    result = aggregate_from_mongodb(col="shell_log", pipeline=pipeline)
    return {'items': result if result == [] else result[0]['lines']}
