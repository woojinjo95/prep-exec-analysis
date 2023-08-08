import logging

from app import schemas
from app.crud.base import (load_from_mongodb, aggregate_from_mongodb)
from fastapi import APIRouter, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", response_model=schemas.TerminalList)
def get_terminal_names() -> schemas.TerminalList:
    """
    터미널 목록
    """
    return {"items": load_from_mongodb(col="terminal_log", proj={'_id': 0, 'logs': 0})}


@router.get("/logs", response_model=schemas.TerminalLogList)
def get_terminal_logs(
    terminal_name: str,
    start_time: str = Query(..., description="ex.2009-02-13T23:31:30+00:00"),
    end_time: str = Query(..., description="ex.2009-02-13T23:31:30+00:00"),
    ) -> schemas.TerminalLogList:
    """
    터미널별 일정기간 로그 조회
    """
    pipeline = [{'$match': {'terminal_name': terminal_name}}, 
                {'$project': {'_id': 0, 'logs': 1}}, 
                {'$unwind': {'path': '$logs'}}, 
                {'$match': {'logs.created_at': {'$gte': start_time, '$lte': end_time}}}, 
                {'$replaceRoot': {'newRoot': '$logs'}}
                ]
    return {"items": aggregate_from_mongodb(col="terminal_log", pipeline=pipeline)}
