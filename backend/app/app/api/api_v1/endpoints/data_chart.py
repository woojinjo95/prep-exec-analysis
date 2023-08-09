import logging

from datetime import datetime, timedelta
from app import schemas
from app.crud.base import aggregate_from_mongodb
from app.api.utility import get_multi_or_paginate_by_res, load_from_mongodb
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
def get_data_of_chart(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    데이터 차트 내용 조회
    """
    pipeline = [{'$match': {'time': {'$gte': start_time, '$lte': end_time}}}]
    # Log Level Finder
    log_level_finder_pipeline = pipeline + [
        {'$match': {'time': {'$gte': start_time, '$lte': end_time}}}, 
        {'$project': {'_id': 0, 'lines': 1}},
        {'$unwind': {'path': '$lines'}}, 
        {'$replaceRoot': {'newRoot': '$lines'}}, 
        {'$project': {'timestamp': 1, 'log_level': 1}}
    ]
    log_level_finder = aggregate_from_mongodb(col='stb_log', pipeline=log_level_finder_pipeline)

    # CPU, Memory
    cpu_memory = load_from_mongodb(col="cpu_memory", param={'time': {'$gte': start_time, '$lte': end_time}})

    # Color Reference
    # Event Log
    # Video Analysis Result
    # Log Pattern Maching
    # Measurement
    # Process Lifecycle
    # Network Filter

    return {"items": {"log_level_finder": log_level_finder, "cpu_memory": cpu_memory}}



@router.get("")
def get_data_of_cpu_and_memory(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    Cpu, Memory 데이터 차트 내용 조회
    """
    pipeline = [{'$match': {'time': {'$gte': start_time, '$lte': end_time}}}]
    
    result = aggregate_from_mongodb(col='####', pipeline=pipeline)
    return result