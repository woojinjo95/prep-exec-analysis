import logging
import uuid

from app import schemas
from app.api.utility import get_multi_or_paginate_by_res
from app.crud.base import (load_from_mongodb, )
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/terminal_list", response_model=schemas.TerminalList)
def get_terminal_names():
    result = load_from_mongodb(col="terminal_log", proj={'_id':0, 'terminal_name':1})
    # [
    # {
    #     '$group': {
    #         '_id': None, 
    #         'terminal_names': {
    #             '$push': '$terminal_name'
    #         }
    #     }
    # }
    # ]
    return {"terminal_names": result}


@router.get("")
def get_terminal_logs(
    terminal_name: str,
    start_time: str = Query(..., description="Start time (ex.2000-01-01T00:00:00)"),
    end_time: str = Query(..., description="End time (ex.2000-01-01T00:00:00)"),
    page: int = Query(1),
    page_size: int = Query(10)
    ):
    # ) -> schemas.TerminalLogsPage:
    """
    터미널별 일정기간 로그 조회
    """
    result = get_multi_or_paginate_by_res(col="terminal_log",
                                          page=page,
                                          page_size=page_size,
                                          param={"terminal_name":terminal_name, "logs.created_at":{"$gte":start_time, "$lte":end_time}},
                                          proj={'_id':0, 'terminal_name':0, 'logs':1})
    return result