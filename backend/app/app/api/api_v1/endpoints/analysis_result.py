import logging
import traceback
from typing import Optional

from app import schemas
from app.api.utility import convert_iso_format, parse_bytes_to_value
from app.crud.base import aggregate_from_mongodb, load_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


# Log Level Finder
@router.get("/log_level_finder", response_model=schemas.LogLevelFinder)
def get_data_of_log_level_finder(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    log_level: Optional[str] = Query(None, description='ex)V,D,I,W,E,F,S'),
):
    """
    로그 레벨 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if log_level is None:
            log_level = parse_bytes_to_value(RedisClient.hget('analysis_config:log_level_finder', 'targets'))
        else:
            log_level = log_level.split(',')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        log_level_finder_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                               '$lte': convert_iso_format(end_time)},
                                                 'scenario_id': scenario_id,
                                                 'testrun_id': testrun_id}},
                                     {'$project': {'_id': 0, 'timestamp': 1, 'log_level': '$lines.log_level'}},
                                     {'$unwind': {'path': '$log_level'}},
                                     {'$match': {'log_level': {'$in': log_level}}}]
        log_level_finder = aggregate_from_mongodb(col='stb_log', pipeline=log_level_finder_pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": log_level_finder}


# CPU
@router.get("/cpu", response_model=schemas.Cpu)
def get_data_of_cpu_and_memory(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
):
    """
    Cpu 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        time_range_param = {'timestamp': {'$gte': convert_iso_format(start_time),
                                          '$lte': convert_iso_format(end_time)},
                            'scenario_id': scenario_id,
                            'testrun_id': testrun_id}
        project = {'_id': 0, 'timestamp': 1, 'cpu_usage': 1, 'total': 1,
                   'user': 1, 'kernel': 1, 'iowait': 1, 'irq': 1, 'softirq': 1}
        cpu = load_from_mongodb(col="stb_info", param=time_range_param, proj=project)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": cpu}


# Memory
@router.get("/memory", response_model=schemas.Memory)
def get_data_of_cpu_and_memory(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
):
    """
    Memory 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        time_range_param = {'timestamp': {'$gte': convert_iso_format(start_time),
                                          '$lte': convert_iso_format(end_time)},
                            'scenario_id': scenario_id,
                            'testrun_id': testrun_id}
        project = {'_id': 0, 'timestamp': 1, 'memory_usage': 1,
                   'total_ram': 1, 'free_ram': 1, 'used_ram': 1, 'lost_ram': 1}
        memory = load_from_mongodb(col="stb_info", param=time_range_param, proj=project)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": memory}


# Event Log
@router.get("/event_log", response_model=schemas.EventLog)
def get_data_of_event_log(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
):
    """
    이벤트 로그 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        event_log_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                        '$lte': convert_iso_format(end_time)},
                                          'scenario_id': scenario_id,
                                          'testrun_id': testrun_id}},
                              {'$project': {'_id': 0, 'lines': 1}},
                              {'$unwind': {'path': '$lines'}},
                              {'$replaceRoot': {'newRoot': '$lines'}}]
        event_log = aggregate_from_mongodb(col='event_log', pipeline=event_log_pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": event_log}


# Color Reference
@router.get("/color_reference", response_model=schemas.ColorReference)
def get_data_of_color_reference(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
):
    """
    컬러 레퍼런스 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        color_reference_param = {'timestamp': {'$gte': convert_iso_format(start_time),
                                               '$lte': convert_iso_format(end_time)},
                                 'scenario_id': scenario_id,
                                 'testrun_id': testrun_id}
        color_reference = load_from_mongodb(col="an_color_reference",
                                            param=color_reference_param,
                                            proj={'_id': 0, 'timestamp': 1, 'color_reference': 1})
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": color_reference}


# Freeze
@router.get("/freeze", response_model=schemas.Freeze)
def get_data_of_freeze(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    freeze_type: Optional[str] = Query(None, description='ex)Black,White'),
):
    """
    화면 멈춤 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        freeze_param = {'timestamp': {'$gte': convert_iso_format(start_time),
                                      '$lte': convert_iso_format(end_time)},
                        'scenario_id': scenario_id,
                        'testrun_id': testrun_id}
        if freeze_type is not None:
            freeze_type = freeze_type.split(',')
            freeze_param['freeze_type'] = {'$in': freeze_type}
        freeze = load_from_mongodb(col="an_freeze",
                                   param=freeze_param,
                                   proj={'_id': 0, 'timestamp': 1, 'freeze_type': 1, 'duration': 1})
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": freeze}


# Loudness
@router.get("/loudness", response_model=schemas.Loudness)
def get_data_of_loudness(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
):
    """
    Loudness 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        loudness_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                       '$lte': convert_iso_format(end_time)},
                                         'scenario_id': scenario_id,
                                         'testrun_id': testrun_id}},
                             {'$project': {'_id': 0, 'lines': 1}},
                             {'$unwind': {'path': '$lines'}},
                             {'$replaceRoot': {'newRoot': '$lines'}},
                             {'$project': {'timestamp': '$timestamp', 'm': '$M', 'i': '$I'}}
                             ]
        loudness = aggregate_from_mongodb(col='loudness', pipeline=loudness_pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": loudness}


# Measurement_resume (warm boot)
@router.get("/resume", response_model=schemas.MeasurementBoot)
def get_data_of_resume(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    target: Optional[str] = None,
):
    """
    분석 데이터 조회 : Resume(Warm booting)
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        measurement_param = {'timestamp': {'$gte': convert_iso_format(start_time),
                                           '$lte': convert_iso_format(end_time)},
                             'scenario_id': scenario_id,
                             'testrun_id': testrun_id}
        if target is not None:
            measurement_param[''] = target
            # TODO: 항목명 확인해서 기입
        measurement_proj = {'_id': 0, 'timestamp': 1, 'measure_time': 1}
        measurement = load_from_mongodb(col='an_warm_boot', param=measurement_param, proj=measurement_proj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": measurement}


# Measurement_resume (cold boot)
@router.get("/boot", response_model=schemas.MeasurementBoot)
def get_data_of_boot(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    target: Optional[str] = None,
):
    """
    분석 데이터 조회 : Boot(Cold booting)
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        measurement_param = {'timestamp': {'$gte': convert_iso_format(start_time),
                                           '$lte': convert_iso_format(end_time)},
                             'scenario_id': scenario_id,
                             'testrun_id': testrun_id}
        if target is not None:
            measurement_param[''] = target
            # TODO: 항목명 확인해서 기입
        measurement_proj = {'_id': 0, 'timestamp': 1, 'measure_time': 1}
        measurement = load_from_mongodb(col='an_cold_boot', param=measurement_param, proj=measurement_proj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": measurement}


# Log Pattern Maching
@router.get("/log_pattern_matching", response_model=schemas.LogPatternMatching)
def get_data_of_log_pattern_matching(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    log_pattern_name: Optional[str] = Query(None, description='ex)LogPattern3,LogPattern16'),
):
    """
    로그 패턴 매칭 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                              '$lte': convert_iso_format(end_time)},
                                'scenario_id': scenario_id,
                                'testrun_id': testrun_id}},
                    {'$project': {'_id': 0, 'timestamp': '$timestamp', 'message': '$message', 'items': '$user_config.items'}}, 
                    {'$unwind': {'path': '$items'}},
                    {'$project': {'timestamp': '$timestamp', 'log_pattern_name': '$items.name', 'log_level': '$items.level', 'message': '$message'}}]
        if log_pattern_name is not None:
            log_pattern_name = log_pattern_name.split(',')
            pipeline.append({'$match': {'$in': log_pattern_name}})
        log_pattern_matching = aggregate_from_mongodb(col='an_log_pattern', pipeline=pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": log_pattern_matching}


# Process Lifecycle
# @router.get("/process_lifecycle", response_model=schemas.ProcessLifecycle)
def get_data_of_process_lifecycle(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
):
    """
    프로세스 활동주기 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        process_lifecycle = load_from_mongodb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": process_lifecycle}


# Network Filter
# @router.get("/network_filter", response_model=schemas.NetworkFilter)
def get_data_of_network_filter(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
):
    """
    네트워크 필터 데이터 조회
    """
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        network_filter = load_from_mongodb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": network_filter}
