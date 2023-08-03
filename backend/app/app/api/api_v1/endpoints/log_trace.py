import logging

from app import schemas
from app.crud.base import (load_from_mongodb, load_paginate_from_mongodb)
from app.api.utility import get_multi_or_paginate_by_res
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/logcat_trace", response_model=schemas.LogcatPage)
def read_logcat_log(
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, ge=1, le=100, description="Page size")
    ) -> schemas.LogcatPage:
    """
    Logcat 로그 조회
    """
    return get_multi_or_paginate_by_res(col='logcat', page=page, page_size=page_size)


@router.get("/network_trace", response_model=schemas.NetworkPage)
def read_network_log(
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, ge=1, le=100, description="Page size")
    ) -> schemas.NetworkPage:
    """
    Network 로그 조회
    """
    return get_multi_or_paginate_by_res(col='network', page=page, page_size=page_size)

