import logging
import traceback
from typing import Optional

from app import schemas
from app.api.utility import convert_iso_format
from app.crud.base import aggregate_from_mongodb, load_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


# Log Level Finder
@router.get("/log_level_finder", response_model=schemas.LogLevelFinder)
def get_data_of_log_level_finder(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    로그 레벨 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        log_level_finder_pipeline = [
            {'$match': {'scenario_id': scenario_id,
                        'timestamp': {'$gte': convert_iso_format(start_time), '$lte': convert_iso_format(end_time)}}},
            {'$project': {'_id': 0, 'lines': 1}},
            {'$unwind': {'path': '$lines'}},
            {'$project': {'timestamp': '$lines.timestamp', 'log_level': '$lines.log_level'}}
        ]
        log_level_finder = aggregate_from_mongodb(col='stb_log', pipeline=log_level_finder_pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": log_level_finder}


# CPU, Memory
@router.get("/cpu_and_memory", response_model=schemas.CpuAndMemory)
def get_data_of_cpu_and_memory(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    Cpu, Memory 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        time_range_param = {'scenario_id': scenario_id,
                            'timestamp': {'$gte': convert_iso_format(start_time),
                                          '$lte': convert_iso_format(end_time)}}
        cpu_and_memory = load_from_mongodb(col="stb_info", param=time_range_param, proj={'_id': 0})
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": cpu_and_memory}


# Event Log
@router.get("/event_log", response_model=schemas.EventLog)
def get_data_of_event_log(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    이벤트 로그 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        event_log_pipeline = [
            {'$match': {'scenario_id': scenario_id,
                        'timestamp': {'$gte': convert_iso_format(start_time),
                                      '$lte': convert_iso_format(end_time)}}},
            {'$project': {'_id': 0, 'lines': 1}},
            {'$unwind': {'path': '$lines'}},
            {'$replaceRoot': {'newRoot': '$lines'}}
        ]
        event_log = aggregate_from_mongodb(col='event_log', pipeline=event_log_pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": event_log}
    # TODO: 리턴에 무엇이 필요한지 확인하여 불필요한 항목 덜어내기


# Color Reference
@router.get("/color_reference", response_model=schemas.ColorReference)
def get_data_of_color_reference(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    컬러 레퍼런스 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        color_reference_param = {'scenario_id': scenario_id,
                                 'timestamp': {'$gte': convert_iso_format(start_time),
                                               '$lte': convert_iso_format(end_time)}}
        color_reference = load_from_mongodb(col="an_color_reference",
                                            param=color_reference_param,
                                            proj={'_id': 0, 'timestamp': 1, 'color_reference': 1})
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": color_reference}


# Freeze
@router.get("/freeze", response_model=schemas.Freeze)
def get_data_of_freeze(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    화면 멈춤 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        freeze_param = {'scenario_id': scenario_id,
                        'timestamp': {'$gte': convert_iso_format(start_time),
                                      '$lte': convert_iso_format(end_time)}}
        freeze = load_from_mongodb(col="an_freeze", param=freeze_param, proj={'_id': 0, 'timestamp': 1, 'freeze_type': 1})
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": freeze}


# Loudness
@router.get("/loudness", response_model=schemas.Loudness)
def get_data_of_loudness(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    ):
    """
    Loudness 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        loudness_pipeline = [{'$match': {'scenario_id': 'd70eede7-2faa-4345-aa46-ba36e1ab40fd'}},
                             {'$project': {'_id': 0, 'lines': 1}},
                             {'$unwind': {'path': '$lines'}},
                             {'$replaceRoot': {'newRoot': '$lines'}}
                             ]
        loudness = aggregate_from_mongodb(col='loudness', pipeline=loudness_pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": loudness}


# Video Analysis Result
@router.get("/video", response_model=schemas.VideoAnalysisResult)
def get_data_of_video(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    비디오 분석 결과 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        video_analysis_result = load_from_mongodb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": video_analysis_result}


# Log Pattern Maching
@router.get("/log_pattern_matching", response_model=schemas.LogPatternMatching)
def get_data_of_log_pattern_matching(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    로그 패턴 매칭 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        log_pattern_matching = load_from_mongodb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": log_pattern_matching}


# Measurement
@router.get("/measurement", response_model=schemas.Measurement)
def get_data_of_measurement(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    분석 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        measurement = load_from_mongodb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": measurement}


# Process Lifecycle
@router.get("/process_lifecycle", response_model=schemas.ProcessLifecycle)
def get_data_of_process_lifecycle(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    프로세스 활동주기 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        process_lifecycle = load_from_mongodb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": process_lifecycle}


# Network Filter
@router.get("/network_filter", response_model=schemas.NetworkFilter)
def get_data_of_network_filter(
    scenario_id: Optional[str] = None,
    # testrun_id: Optional[str] = None, # TODO: testrun_id 내용 추가되면 필터 추가 (시나리오 아이디랑 똑같이 레디스에서 디폴트값 참조)
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
):
    """
    네트워크 필터 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        network_filter = load_from_mongodb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": network_filter}
