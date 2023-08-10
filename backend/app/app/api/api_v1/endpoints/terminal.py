import logging
from datetime import datetime

from app import schemas
from app.crud.base import (load_from_mongodb, aggregate_from_mongodb)
from fastapi import APIRouter, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.TerminalList)
def get_terminal_modes() -> schemas.TerminalList:
    """
    터미널 목록
    """
    return {"items": load_from_mongodb(col="shell_log", proj={'_id': 0, 'lines': 0, 'time': 0})}


@router.get("/logs", response_model=schemas.TerminalLogList)
def get_terminal_logs(
    terminal_mode: str,
    start_time: str = Query(..., description="ex.2009-02-13T23:31:30"),
    end_time: str = Query(..., description="ex.2009-02-13T23:31:30"),
    ) -> schemas.TerminalLogList:
    """
    터미널별 일정기간 로그 조회
    """
    param = {'time': {'$gte': start_time, '$lte': end_time}, 'mode': terminal_mode}
    result = load_from_mongodb(col="shell_log", param=param, proj={'_id': 0, 'lines': 1})
    return {'items': result if result == [] else result[0]['lines']}
