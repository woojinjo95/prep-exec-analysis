import logging
from typing import Optional

from app import schemas
from app.db.redis_session import RedisClient
from app.crud.base import aggregate_from_mongodb, load_from_mongodb
from fastapi import APIRouter, Query

logger = logging.getLogger(__name__)
router = APIRouter()


# Log Level Finder
@router.get("/log_level_finder", response_model=schemas.LogLevelFinder)
def get_data_of_log_level_finder(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    로그 레벨 데이터 조회
    """
    log_level_finder_pipeline = [
        {'$match': {'scenario_id': scenario_id, 'timestamp': {'$gte': start_time, '$lte': end_time}}}, 
        {'$project': {'_id': 0, 'lines': 1}},
        {'$unwind': {'path': '$lines'}},
        {'$project': {'timestamp': '$lines.timestamp', 'log_level': '$lines.log_level'}}
    ]
    log_level_finder = aggregate_from_mongodb(col='stb_log', pipeline=log_level_finder_pipeline)
    return {"items": log_level_finder}


# CPU, Memory
@router.get("/cpu_and_memory", response_model=schemas.CpuAndMemory)
def get_data_of_cpu_and_memory(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    Cpu, Memory 데이터 조회
    """
    time_range_param = {'scenario_id': scenario_id, 'timestamp': {'$gte': start_time, '$lte': end_time}}
    cpu_and_memory = load_from_mongodb(col="stb_info", param=time_range_param, proj={'_id': 0})
    return {"items": cpu_and_memory}


# Color Reference
@router.get("/color_reference", response_model=schemas.ColorReference)
def get_data_of_color_reference(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    컬러 레퍼런스 데이터 조회
    """
    color_reference = load_from_mongodb()
    return {"items": color_reference}


# Event Log
@router.get("/event_log", response_model=schemas.EventLog)
def get_data_of_event_log(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    이벤트 로그 데이터 조회
    """
    event_log = load_from_mongodb()
    return {"items": event_log}


# Video Analysis Result
@router.get("/video_analysis_result", response_model=schemas.VideoAnalysisResult)
def get_data_of_video_analysis_result(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    비디오 분석 결과 데이터 조회
    """
    video_analysis_result = load_from_mongodb()
    return {"items": video_analysis_result}


# Log Pattern Maching
@router.get("/log_pattern_matching", response_model=schemas.LogPatternMatching)
def get_data_of_log_pattern_matching(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    로그 패턴 매칭 데이터 조회
    """
    log_pattern_matching = load_from_mongodb()
    return {"items": log_pattern_matching}


# Measurement
@router.get("/measurement", response_model=schemas.Measurement)
def get_data_of_measurement(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    분석 데이터 조회
    """
    measurement = load_from_mongodb()
    return {"items": measurement}


# Process Lifecycle
@router.get("/process_lifecycle", response_model=schemas.ProcessLifecycle)
def get_data_of_process_lifecycle(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    프로세스 활동주기 데이터 조회
    """
    process_lifecycle = load_from_mongodb()
    return {"items": process_lifecycle}


# Network Filter
@router.get("/network_filter", response_model=schemas.NetworkFilter)
def get_data_of_network_filter(
    scenario_id: Optional[str] = RedisClient.hget('testrun', 'scenario_id'),
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    네트워크 필터 데이터 조회
    """
    network_filter = load_from_mongodb()
    return {"items": network_filter}

