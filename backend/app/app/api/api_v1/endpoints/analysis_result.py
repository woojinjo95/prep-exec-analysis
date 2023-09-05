import itertools
import logging
import traceback
from typing import Optional

from app import schemas
from app.api.utility import (convert_iso_format, parse_bytes_to_value,
                             paginate_from_mongodb_aggregation)
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
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    로그 레벨 데이터 조회
    """
    try:
        if log_level is None:
            log_level = parse_bytes_to_value(RedisClient.hget('analysis_config:log_level_finder', 'targets'))
        else:
            log_level = log_level.split(',')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        log_level_finder_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                               '$lte': convert_iso_format(end_time)},
                                                 'scenario_id': scenario_id,
                                                 'testrun_id': testrun_id}},
                                     {'$project': {'_id': 0, 'lines.timestamp': 1, 'lines.log_level': 1}},
                                     {'$unwind': {'path': '$lines'}},
                                     {'$replaceRoot':{'newRoot': '$lines'}},
                                     {'$match': {'log_level': {'$in': log_level}}}]

        log_level_finder = paginate_from_mongodb_aggregation(col='stb_log',
                                                             pipeline=log_level_finder_pipeline,
                                                             page=page,
                                                             page_size=page_size,
                                                             sort_by=sort_by,
                                                             sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return log_level_finder


# CPU
@router.get("/cpu", response_model=schemas.Cpu)
def get_data_of_cpu(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    Cpu 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        cpu_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                  '$lte': convert_iso_format(end_time)},
                                    'scenario_id': scenario_id,
                                    'testrun_id': testrun_id}},
                        {'$project': {'_id': 0, 'timestamp': 1, 'cpu_usage': 1, 'total': 1,
                                      'user': 1, 'kernel': 1, 'iowait': 1, 'irq': 1, 'softirq': 1}}]

        cpu = paginate_from_mongodb_aggregation(col='stb_info',
                                                pipeline=cpu_pipeline,
                                                page=page,
                                                page_size=page_size,
                                                sort_by=sort_by,
                                                sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return cpu


# Memory
@router.get("/memory", response_model=schemas.Memory)
def get_data_of_memory(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    Memory 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        memory_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                     '$lte': convert_iso_format(end_time)},
                                       'scenario_id': scenario_id,
                                       'testrun_id': testrun_id}},
                           {'$project': {'_id': 0, 'timestamp': 1, 'memory_usage': 1,
                                         'total_ram': 1, 'free_ram': 1, 'used_ram': 1, 'lost_ram': 1}}]

        memory = paginate_from_mongodb_aggregation(col='stb_info',
                                                   pipeline=memory_pipeline,
                                                   page=page,
                                                   page_size=page_size,
                                                   sort_by=sort_by,
                                                   sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return memory


# Event Log
@router.get("/event_log", response_model=schemas.EventLog)
def get_data_of_event_log(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    이벤트 로그 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        event_log_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                        '$lte': convert_iso_format(end_time)},
                                          'scenario_id': scenario_id,
                                          'testrun_id': testrun_id}},
                              {'$project': {'_id': 0, 'lines': 1}},
                              {'$unwind': {'path': '$lines'}},
                              {'$match': {'lines.msg': {'$in': ['remocon_response', 'on_off_control_response', 'network_emulation_response', 'shell', 'config']}}},
                              {'$replaceRoot': {'newRoot': '$lines'}}]

        event_log = paginate_from_mongodb_aggregation(col='event_log',
                                                      pipeline=event_log_pipeline,
                                                      page=page,
                                                      page_size=page_size,
                                                      sort_by=sort_by,
                                                      sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return event_log


# Color Reference
@router.get("/color_reference", response_model=schemas.ColorReference)
def get_data_of_color_reference(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    컬러 레퍼런스 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        color_reference_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                              '$lte': convert_iso_format(end_time)},
                                                'scenario_id': scenario_id,
                                                'testrun_id': testrun_id}},
                                    {'$project': {'_id': 0, 'timestamp': 1, 'color_reference': 1}}]

        color_reference = paginate_from_mongodb_aggregation(col='an_color_reference',
                                                            pipeline=color_reference_pipeline,
                                                            page=page,
                                                            page_size=page_size,
                                                            sort_by=sort_by,
                                                            sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return color_reference


# Freeze
@router.get("/freeze", response_model=schemas.Freeze)
def get_data_of_freeze(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    화면 멈춤 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')

        freeze_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                     '$lte': convert_iso_format(end_time)},
                                       'scenario_id': scenario_id,
                                       'testrun_id': testrun_id}},
                           {'$project': {'_id': 0, 'timestamp': 1, 'freeze_type': 1, 'duration': 1}}]

        freeze = paginate_from_mongodb_aggregation(col='an_freeze',
                                                   pipeline=freeze_pipeline,
                                                   page=page,
                                                   page_size=page_size,
                                                   sort_by=sort_by,
                                                   sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return freeze


# Loudness
@router.get("/loudness", response_model=schemas.Loudness)
def get_data_of_loudness(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    Loudness 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        loudness_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                       '$lte': convert_iso_format(end_time)},
                                         'scenario_id': scenario_id,
                                         'testrun_id': testrun_id}},
                             {'$project': {'_id': 0, 'lines': 1}},
                             {'$unwind': {'path': '$lines'}},
                             {'$replaceRoot': {'newRoot': '$lines'}},
                             {'$project': {'timestamp': '$timestamp', 'm': '$M', 'i': '$I'}}]

        loudness = paginate_from_mongodb_aggregation(col='loudness',
                                                     pipeline=loudness_pipeline,
                                                     page=page,
                                                     page_size=page_size,
                                                     sort_by=sort_by,
                                                     sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return loudness


# Measurement_resume (warm boot)
@router.get("/resume", response_model=schemas.Resume)
def get_data_of_resume(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    분석 데이터 조회 : Resume(Warm booting)
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        measurement_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                          '$lte': convert_iso_format(end_time)},
                                            'scenario_id': scenario_id,
                                            'testrun_id': testrun_id}},
                                {'$project': {'_id': 0, 'timestamp': 1, 'measure_time': 1, 'target': '$user_config.type'}}]

        measurement_resume = paginate_from_mongodb_aggregation(col='an_warm_boot',
                                                               pipeline=measurement_pipeline,
                                                               page=page,
                                                               page_size=page_size,
                                                               sort_by=sort_by,
                                                               sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return measurement_resume


# Measurement_resume (cold boot)
@router.get("/boot", response_model=schemas.Boot)
def get_data_of_boot(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    분석 데이터 조회 : Boot(Cold booting)
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        measurement_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                          '$lte': convert_iso_format(end_time)},
                                            'scenario_id': scenario_id,
                                            'testrun_id': testrun_id}},
                                {'$project': {'_id': 0, 'timestamp': 1, 'measure_time': 1, 'target': '$user_config.type'}}]

        measurement_boot = paginate_from_mongodb_aggregation(col='an_cold_boot',
                                                             pipeline=measurement_pipeline,
                                                             page=page,
                                                             page_size=page_size,
                                                             sort_by=sort_by,
                                                             sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return measurement_boot


# Log Pattern Maching
@router.get("/log_pattern_matching", response_model=schemas.LogPatternMatching)
def get_data_of_log_pattern_matching(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    로그 패턴 매칭 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        log_pattern_matching_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                                   '$lte': convert_iso_format(end_time)},
                                                     'scenario_id': scenario_id,
                                                     'testrun_id': testrun_id}},
                                         {'$project': {'_id': 0, 'log_level': 1, 'timestamp': 1, 'message': 1,
                                                       'regex': '$matched_target.regular_expression',
                                                       'color': '$matched_target.color', 'log_pattern_name': '$matched_target.name'}}]

        log_pattern_matching = paginate_from_mongodb_aggregation(col='an_log_pattern',
                                                                 pipeline=log_pattern_matching_pipeline,
                                                                 page=page,
                                                                 page_size=page_size,
                                                                 sort_by=sort_by,
                                                                 sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return log_pattern_matching


# Process Lifecycle
# @router.get("/process_lifecycle", response_model=schemas.ProcessLifecycle)
def get_data_of_process_lifecycle(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    프로세스 활동주기 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        process_lifecycle = load_from_mongodb()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": process_lifecycle}


# Network Filter
# @router.get("/network_filter", response_model=schemas.NetworkFilter)
def get_data_of_network_filter(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = False
):
    """
    네트워크 필터 데이터 조회
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        network_filter = load_from_mongodb()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": network_filter}


# Data Summary
@router.get("/summary", response_model=schemas.DataSummary)
def get_summary_data_of_measure_result(
    start_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(..., description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None
):
    """
    분석 결과 데이터 개요
    """
    try:
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')

        result = {}
        basic_pipeline = [{'$match': {'timestamp': {'$gte': convert_iso_format(start_time),
                                                    '$lte': convert_iso_format(end_time)},
                                      'scenario_id': scenario_id,
                                      'testrun_id': testrun_id}}]

        active_analysis_list = RedisClient.scan_iter(match="analysis_config:*")
        for active_analysis in itertools.chain(active_analysis_list, ['loudness']):
            active_analysis = active_analysis.split(':')[-1]

            pipeline = []
            additional_pipeline = []
            if active_analysis == 'log_level_finder':
                collection = 'stb_log'
                additional_pipeline = [{'$project': {'_id': 0, 'lines.log_level': 1}},
                                       {'$unwind': {'path': '$lines'}},
                                       {'$group': {'_id': '$lines.log_level', 'total': {'$sum': 1}}},
                                       {'$group': {'_id': None, 'results': {'$push': {'target': '$_id', 'total': '$total'}}}},
                                       {'$project': {'_id': 0, 'results': 1, 'color': '#0106FF'}}]  # TODO: color 색상코드 관리 필요
            elif active_analysis == 'freeze':
                collection = 'an_freeze'
                additional_pipeline = [{'$group': {'_id': '$freeze_type', 'total': {'$sum': 1}, 'color': {'$first': '$user_config.color'}}},
                                       {'$group': {'_id': '$color', 'results': {'$push': {'total': '$total', 'error_type': '$_id'}}}},
                                       {'$project': {'_id': 0, 'color': '$_id', 'results': 1}}]
            elif active_analysis == 'resume':
                collection = 'an_warm_boot'
                additional_pipeline = [{'$group': {'_id': '$user_config.type', 'total': {'$sum': 1}, 'avg_time': {'$avg': '$measure_time'}, 'color': {'$first': '$user_config.color'}}},
                                       {'$group': {'_id': '$color', 'results': {'$push': {'target': '$_id', 'total': '$total', 'avg_time': '$avg_time'}}}},
                                       {'$project': {'_id': 0, 'color': '$_id', 'results': 1}}]
            elif active_analysis == 'boot':
                collection = 'an_cold_boot'
                additional_pipeline = [{'$group': {'_id': None, 'total': {'$sum': 1}, 'avg_time': {'$avg': '$measure_time'}, "target":{'$first': '$user_config.type'}}},
                                       {'$project': {'_id': 0}}]
            elif active_analysis == 'log_pattern_matching':
                collection = 'an_log_pattern'
                additional_pipeline = [{'$project': {'_id': 0, 'list': ['$matched_target.name', '$matched_target.color'], 'color': '$user_config.color'}},
                                       {'$group': {'_id': '$list', 'total': {'$sum': 1}, 'color': {'$first': '$color'}}},
                                       {'$group': {'_id': '$color', 'results': {'$push': {'total': '$total', 'log_pattern_name': {'$arrayElemAt': ['$_id', 0]}, 'color': {'$arrayElemAt': ['$_id', 1]}}}}},
                                       {'$project': {'_id': 0, 'color': '$_id', 'results': 1}}]
            elif active_analysis == 'macroblock':
                continue
            elif active_analysis == 'channel_change_time':
                continue
            elif active_analysis == 'process_lifecycle_analysis':
                continue
            elif active_analysis == 'network_filter':
                continue
            else:
                collection = 'loudness'
                additional_pipeline = [{'$project': {'_id': 0, 'lines': 1}},
                                       {'$unwind': {'path': '$lines'}},
                                       {'$group': {'_id': None, 'lkfs': {'$avg': '$lines.I'}}},
                                       {'$project': {'_id': 0, 'lkfs': 1, 'color': '#FF9900'}}] # TODO: color 색상코드 관리 필요
            pipeline = basic_pipeline + additional_pipeline
            aggregation = aggregate_from_mongodb(col=collection, pipeline=pipeline)
            if len(aggregation) == 0:
                continue
            result[active_analysis] = aggregation[0]
        timestamp_pipeline = [{'$match': {'id': scenario_id}},
                              {'$project': {'_id': 0, 'testruns': 1}},
                              {'$unwind': {'path': '$testruns'}},
                              {'$match': {'testruns.id': testrun_id}},
                              {'$project': {'last_timestamp': '$testruns.analysis.last_timestamp'}}]
        last_timestamp = aggregate_from_mongodb(col='scenario', pipeline=timestamp_pipeline)
        last_timestamp = last_timestamp[0] if len(last_timestamp) > 0 else None
        result['last_timestamp'] = last_timestamp['last_timestamp'].strftime('%Y-%m-%dT%H:%M:%S.%fZ') if last_timestamp is not None else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": result}
