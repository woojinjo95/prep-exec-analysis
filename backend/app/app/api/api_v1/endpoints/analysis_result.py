import io
import json
import logging
import os
import tarfile
import traceback
import uuid
from datetime import datetime
from typing import Optional

from app import schemas
from app.api.utility import (analysis_collection, convert_data_in,
                             deserialize_datetime,
                             get_config_from_scenario_mongodb,
                             make_basic_match_pipeline,
                             paginate_from_mongodb_aggregation,
                             serialize_datetime)
from app.crud.base import (aggregate_from_mongodb, insert_one_to_mongodb,
                           load_from_mongodb)
from app.db.redis_session import RedisClient
from fastapi import APIRouter, File, HTTPException, Query, Response, UploadFile
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


# Log Level Finder
@router.get("/log_level_finder", response_model=schemas.LogLevelFinder)
def get_data_of_log_level_finder(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    로그 레벨 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        log_level_finder_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                              testrun_id=testrun_id,
                                                              start_time=start_time,
                                                              end_time=end_time)

        config = get_config_from_scenario_mongodb(scenario_id=scenario_id,
                                                  testrun_id=testrun_id,
                                                  target='log_level_finder')
        if config == {}:
            raise HTTPException(status_code=404, detail='Not Found LogLevelFinder Configurataion')
        log_level = config.get('targets', [])

        additional_pipeline = [
            {'$project': {'_id': 0, 'lines.timestamp': 1, 'lines.log_level': 1}},
            {'$unwind': {'path': '$lines'}},
            {'$replaceRoot': {'newRoot': '$lines'}},
            {'$match': {'log_level': {'$in': log_level}}},
            {'$project': {'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'log_level': 1}}]
        log_level_finder_pipeline.extend(additional_pipeline)
        log_level_finder = paginate_from_mongodb_aggregation(col=analysis_collection['log_level_finder'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    Cpu 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        cpu_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                 testrun_id=testrun_id,
                                                 start_time=start_time,
                                                 end_time=end_time)

        additional_pipeline = [
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'cpu_usage': 1, 'total': 1, 'user': 1, 'kernel': 1,
                          'iowait': 1, 'irq': 1, 'softirq': 1}}]
        cpu_pipeline.extend(additional_pipeline)
        cpu = paginate_from_mongodb_aggregation(col=analysis_collection['cpu'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    Memory 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        memory_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                    testrun_id=testrun_id,
                                                    start_time=start_time,
                                                    end_time=end_time)

        additional_pipeline = [
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'memory_usage': 1,
                          'total_ram': 1, 'free_ram': 1,
                          'used_ram': 1, 'lost_ram': 1}}]
        memory_pipeline.extend(additional_pipeline)

        memory = paginate_from_mongodb_aggregation(col=analysis_collection['memory'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    이벤트 로그 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        event_log_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                       testrun_id=testrun_id,
                                                       start_time=start_time,
                                                       end_time=end_time)

        event_log_type_list = ['remocon_response', 'on_off_control_response',
                               'network_emulation_response', 'shell_response',
                               'capture_board_response', 'config_response']
        additional_pipeline = [
            {'$project': {'_id': 0, 'lines': 1}},
            {'$unwind': {'path': '$lines'}},
            {'$match': {'lines.msg': {'$in': event_log_type_list}}},
            {'$replaceRoot': {'newRoot': '$lines'}},
            {'$project': {'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'service': 1, 'msg': 1, 'data': 1}}]
        event_log_pipeline.extend(additional_pipeline)

        event_log = paginate_from_mongodb_aggregation(col=analysis_collection['event_log'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    컬러 레퍼런스 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        color_reference_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                             testrun_id=testrun_id,
                                                             start_time=start_time,
                                                             end_time=end_time)

        color_reference_pipeline = [
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'color_reference': 1}}]

        color_reference = paginate_from_mongodb_aggregation(col=analysis_collection['color_reference'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    화면 멈춤 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        freeze_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                    testrun_id=testrun_id,
                                                    start_time=start_time,
                                                    end_time=end_time)

        config = get_config_from_scenario_mongodb(scenario_id=scenario_id,
                                                  testrun_id=testrun_id,
                                                  target='freeze')
        if config == {}:
            raise HTTPException(status_code=404, detail='Not Found Freeze Configurataion')
        duration = config.get('duration', 3)

        additional_pipeline = [
            {'$match': {'user_config.duration': duration}},
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'freeze_type': 1,
                          'duration': 1}}]
        freeze_pipeline.extend(additional_pipeline)

        freeze = paginate_from_mongodb_aggregation(col=analysis_collection['freeze'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    Loudness 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        loudness_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                      testrun_id=testrun_id,
                                                      start_time=start_time,
                                                      end_time=end_time)

        additional_pipeline = [
            {'$project': {'_id': 0, 'lines': 1}},
            {'$unwind': {'path': '$lines'}},
            {'$replaceRoot': {'newRoot': '$lines'}},
            {'$project': {'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'm': '$M', 'i': '$I'}}]
        loudness_pipeline.extend(additional_pipeline)

        loudness = paginate_from_mongodb_aggregation(col=analysis_collection['loudness'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    분석 데이터 조회 : Resume(Warm booting)
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        measurement_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                         testrun_id=testrun_id,
                                                         start_time=start_time,
                                                         end_time=end_time)

        config = get_config_from_scenario_mongodb(scenario_id=scenario_id,
                                                  testrun_id=testrun_id,
                                                  target='resume')
        if config == {}:
            raise HTTPException(status_code=404, detail='Not Found Resume Configurataion')
        type = config.get('type', '')
        frame = config.get('frame', {})

        additional_pipeline = [
            {'$match': {'user_config.type': type, 'user_config.frame': frame}},
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'measure_time': 1,
                          'target': '$user_config.type'}}]
        measurement_pipeline.extend(additional_pipeline)

        measurement_resume = paginate_from_mongodb_aggregation(col=analysis_collection['resume'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    분석 데이터 조회 : Boot(Cold booting)
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        measurement_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                         testrun_id=testrun_id,
                                                         start_time=start_time,
                                                         end_time=end_time)

        config = get_config_from_scenario_mongodb(scenario_id=scenario_id,
                                                  testrun_id=testrun_id,
                                                  target='boot')
        if config == {}:
            raise HTTPException(status_code=404, detail='Not Found Boot Configurataion')
        frame = config.get('frame', {})

        additional_pipeline = [
            {'$match': {'user.config.frame': frame}},
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'measure_time': 1,
                          'target': '$user_config.type'}}]
        measurement_pipeline.extend(additional_pipeline)

        measurement_boot = paginate_from_mongodb_aggregation(col=analysis_collection['boot'],
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    pattern_name: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    로그 패턴 매칭 데이터 조회
    """
    if start_time is None and end_time is None:
        raise HTTPException(status_code=400, detail='Need at least one time parameter')

    log_pattern_matching_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                              testrun_id=testrun_id,
                                                              start_time=start_time,
                                                              end_time=end_time)
    if pattern_name:
        name_pipeline = [{'$match': {'matched_target.name': {'$in': pattern_name.split(',')}}}]
        log_pattern_matching_pipeline.extend(name_pipeline)
    else:
        config = get_config_from_scenario_mongodb(scenario_id=scenario_id,
                                                  testrun_id=testrun_id,
                                                  target='log_pattern_matching')
        if config == {}:
            raise HTTPException(status_code=404, detail='Not Found LogPatternMatching Configurataion')
        name_pipeline = [
            {'$match': {'user_config.items': {'$in': config.get('items', [])}}}]
        log_pattern_matching_pipeline.extend(name_pipeline)

    additional_pipeline = [
        {'$project': {'_id': 0,
                      'log_level': 1,
                      'timestamp': {'$dateToString': {'date': '$timestamp'}},
                      'message': 1,
                      'regex': '$matched_target.regular_expression',
                      'color': '$matched_target.color',
                      'log_pattern_name': '$matched_target.name'}}]
    log_pattern_matching_pipeline.extend(additional_pipeline)

    log_pattern_matching = paginate_from_mongodb_aggregation(col=analysis_collection['log_pattern_matching'],
                                                             pipeline=log_pattern_matching_pipeline,
                                                             page=page,
                                                             page_size=page_size,
                                                             sort_by=sort_by,
                                                             sort_desc=sort_desc)
    return log_pattern_matching


# Monkey Section
@router.get("/monkey_section", response_model=schemas.MonkeyTest)
def get_data_of_monkey_section(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'start_timestamp',
    sort_desc: Optional[bool] = False
):
    """
    일반 몽키 테스트 섹션 데이터 조회(범위)
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        monkey_section_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                            testrun_id=testrun_id,
                                                            start_time=start_time,
                                                            end_time=end_time)
        monkey_section_pipeline[0]['$match']['analysis_type'] = 'monkey'
        additional_pipeline = [
            {'$project': {'id': {'$toString': '$_id'},
                          'start_timestamp': {'$dateToString': {'date': '$start_timestamp'}},
                          'end_timestamp': {'$dateToString': {'date': '$end_timestamp'}}}}]
        monkey_section_pipeline.extend(additional_pipeline)

        monkey_section = paginate_from_mongodb_aggregation(col='monkey_section',
                                                           pipeline=monkey_section_pipeline,
                                                           page=page,
                                                           page_size=page_size,
                                                           sort_by=sort_by,
                                                           sort_desc=sort_desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return monkey_section


# Monkey Smart Sense
@router.get("/monkey_smart_sense", response_model=schemas.MonkeySmartSense)
def get_data_of_monkey_smart_sense(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    일반 몽키 테스트 스마트 센스 키 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        monkey_smart_sense_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                                testrun_id=testrun_id,
                                                                start_time=start_time,
                                                                end_time=end_time)
        monkey_smart_sense_pipeline[0]['$match']['analysis_type'] = 'monkey'
        additional_pipeline = [{'$project': {'id': {'$toString': '$_id'},
                                             'timestamp': {'$dateToString': {'date': '$timestamp'}},
                                             'smart_sense_key': 1}}]
        monkey_smart_sense_pipeline.extend(additional_pipeline)

        monkey_section = paginate_from_mongodb_aggregation(col='monkey_smart_sense',
                                                           pipeline=monkey_smart_sense_pipeline,
                                                           page=page,
                                                           page_size=page_size,
                                                           sort_by=sort_by,
                                                           sort_desc=sort_desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return monkey_section


# Intelligent Monkey Section
@router.get("/intelligent_monkey_section", response_model=schemas.IntelligentMonkeyTest)
def get_data_of_intelligent_monkey_section(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'start_timestamp',
    sort_desc: Optional[bool] = False
):
    """
    인텔리전트 몽키 테스트 섹션 데이터 조회(범위)
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        monkey_section_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                            testrun_id=testrun_id,
                                                            start_time=start_time,
                                                            end_time=end_time)
        monkey_section_pipeline[0]['$match']['analysis_type'] = 'intelligent_monkey'
        additional_pipeline = [
            {'$project': {'_id': 0,
                          'section_id': '$section_id',
                          'start_timestamp': {'$dateToString': {'date': '$start_timestamp'}},
                          'end_timestamp': {'$dateToString': {'date': '$end_timestamp'}}}}]
        monkey_section_pipeline.extend(additional_pipeline)
        monkey_section = paginate_from_mongodb_aggregation(col='monkey_section',
                                                           pipeline=monkey_section_pipeline,
                                                           page=page,
                                                           page_size=page_size,
                                                           sort_by=sort_by,
                                                           sort_desc=sort_desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return monkey_section


# Intelligent Monkey Smart Sense
@router.get("/intelligent_monkey_smart_sense", response_model=schemas.IntelligentMonkeySmartSense)
def get_data_of_intelligent_monkey_smart_sense(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    인텔리전트 몽키 테스트 스마트 센스 키 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        monkey_smart_sense_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                                testrun_id=testrun_id,
                                                                start_time=start_time,
                                                                end_time=end_time)
        monkey_smart_sense_pipeline[0]['$match']['analysis_type'] = 'intelligent_monkey'
        additional_pipeline = [
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'smart_sense_key': 1,
                          'section_id': 1}}]
        monkey_smart_sense_pipeline.extend(additional_pipeline)

        monkey_section = paginate_from_mongodb_aggregation(col='monkey_smart_sense',
                                                           pipeline=monkey_smart_sense_pipeline,
                                                           page=page,
                                                           page_size=page_size,
                                                           sort_by=sort_by,
                                                           sort_desc=sort_desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return monkey_section


# Macro Block
@router.get("/macroblock", response_model=schemas.Macroblock)
def get_data_of_macro_block(
    start_time: str = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: str = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    화면 깨짐 데이터 조회
    """
    macroblock_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                    testrun_id=testrun_id,
                                                    start_time=start_time,
                                                    end_time=end_time)

    config = get_config_from_scenario_mongodb(scenario_id=scenario_id,
                                              testrun_id=testrun_id,
                                              target='macroblock')
    if config == {}:
        raise HTTPException(status_code=404, detail='Not Found Macroblock Configurataion')
    config_pipeline = [{'$match': {'user_config': config}}]
    macroblock_pipeline.extend(config_pipeline)

    additional_pipeline = [{'$project': {'_id': 0,
                                         'timestamp': {'$dateToString': {'date': '$timestamp'}},
                                         'duration': 1}}]
    macroblock_pipeline.extend(additional_pipeline)

    macroblock = paginate_from_mongodb_aggregation(col=analysis_collection['macroblock'],
                                                   pipeline=macroblock_pipeline,
                                                   page=page,
                                                   page_size=page_size,
                                                   sort_by=sort_by,
                                                   sort_desc=sort_desc)
    return macroblock


# Channel Change Time
@router.get("/channel_change_time", response_model=schemas.ChannelChangeTime)
def get_data_of_boot(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    page_size: Optional[int] = 10,
    page: Optional[int] = None,
    sort_by: Optional[str] = 'timestamp',
    sort_desc: Optional[bool] = False
):
    """
    채널 변경 시간 데이터 조회
    """
    try:
        if start_time is None and end_time is None:
            raise HTTPException(status_code=400, detail='Need at least one time parameter')

        channel_zapping_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                             testrun_id=testrun_id,
                                                             start_time=start_time,
                                                             end_time=end_time)

        config = get_config_from_scenario_mongodb(scenario_id=scenario_id,
                                                  testrun_id=testrun_id,
                                                  target='channel_change_time')
        if config == {}:
            raise HTTPException(status_code=404, detail='Not Found ChannelChangeTime Configurataion')
        target = config.get('targets', [])
        additional_pipeline = [{'$match': {'user_config.targets': target}}]
        channel_zapping_pipeline.extend(additional_pipeline)

        additional_pipeline = [
            {'$project': {'_id': 0,
                          'timestamp': {'$dateToString': {'date': '$timestamp'}},
                          'channel_name': 1,
                          'section_a': 1,
                          'section_b': 1,
                          'section_c': 1,
                          'measure_time': 1,
                          'targets': '$user_config.targets'}}]
        channel_zapping_pipeline.extend(additional_pipeline)

        channel_zapping = paginate_from_mongodb_aggregation(col=analysis_collection['channel_change_time'],
                                                            pipeline=channel_zapping_pipeline,
                                                            page=page,
                                                            page_size=page_size,
                                                            sort_by=sort_by,
                                                            sort_desc=sort_desc)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return channel_zapping


# Process Lifecycle
# @router.get("/process_lifecycle", response_model=schemas.ProcessLifecycle)
def get_data_of_process_lifecycle(
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
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
    start_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    end_time: Optional[str] = Query(None, description='ex)2009-02-13T23:31:30+00:00'),
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None
):
    """
    분석 결과 데이터 개요
    """
    try:
        basic_pipeline = make_basic_match_pipeline(scenario_id=scenario_id,
                                                   testrun_id=testrun_id,
                                                   start_time=start_time,
                                                   end_time=end_time)
        result = {}

        testrun_config = get_config_from_scenario_mongodb(scenario_id=scenario_id, testrun_id=testrun_id)
        for active_analysis, config in testrun_config.items():
            if config is None:
                continue
            pipeline = []
            additional_pipeline = []
            if active_analysis == 'log_level_finder':
                log_level_list = config.get('targets', [])
                additional_pipeline = [
                    {'$project': {'_id': 0, 'lines.log_level': 1}},
                    {'$unwind': {'path': '$lines'}},
                    {'$match': {'lines.log_level': {'$in': log_level_list}}},
                    {'$group': {'_id': '$lines.log_level', 'total': {'$sum': 1}}},
                    {'$group': {'_id': None, 'results': {'$push': {'target': '$_id', 'total': '$total'}}}},
                    {'$project': {'_id': 0, 'results': 1}}]
            elif active_analysis == 'freeze':
                duration = config.get('duration', 0)
                additional_pipeline = [
                    {'$match': {'user_config.duration': duration}},
                    {'$group': {'_id': '$freeze_type', 'total': {'$sum': 1}, 'color': {'$first': '$user_config.color'}}},
                    {'$group': {'_id': '$color', 'results': {
                        '$push': {'total': '$total', 'error_type': '$_id'}}}},
                    {'$project': {'_id': 0, 'color': '$_id', 'results': 1}}]
            elif active_analysis == 'resume':
                type = config.get('type', '')
                frame = config.get('frame', {})
                additional_pipeline = [
                    {'$match': {'user_config.type': type, 'user_config.frame': frame}},
                    {'$group': {'_id': '$user_config.type', 'total': {'$sum': 1},
                                'avg_time': {'$avg': '$measure_time'}, 'color': {'$first': '$user_config.color'}}},
                    {'$group': {'_id': '$color', 'results': {
                        '$push': {'target': '$_id', 'total': '$total', 'avg_time': '$avg_time'}}}},
                    {'$project': {'_id': 0, 'color': '$_id', 'results': 1}}]
            elif active_analysis == 'boot':
                frame = config.get('frame', {})
                additional_pipeline = [
                    {'$match': {'user_config.frame': frame}},
                    {'$group': {'_id': '$user_config.type', 'total': {'$sum': 1},
                                'avg_time': {'$avg': '$measure_time'}, 'color': {'$first': '$user_config.color'}}},
                    {'$group': {'_id': '$color', 'results': {
                        '$push': {'target': '$_id', 'total': '$total', 'avg_time': '$avg_time'}}}},
                    {'$project': {'_id': 0, 'color': '$_id', 'results': 1}}]
            elif active_analysis == 'log_pattern_matching':
                name = config.get('name', '')
                color = config.get('color', '')
                level = config.get('level', '')
                regular_expression = config.get('regular_expression', '')
                additional_pipeline = [
                    {'$match': {'matched_target': {'color': color, 'name': name, 'level': level,
                                                   'regular_expression': regular_expression}}},
                    {'$project': {'_id': 0, 'list': ['$matched_target.name',
                                                     '$matched_target.color'], 'color': '$user_config.color'}},
                    {'$group': {'_id': '$list', 'total': {'$sum': 1}, 'color': {'$first': '$color'}}},
                    {'$group': {'_id': '$color', 'results': {'$push': {'total': '$total',
                                                                       'log_pattern_name': {'$arrayElemAt': ['$_id', 0]},
                                                                       'color': {'$arrayElemAt': ['$_id', 1]}}}}},
                    {'$project': {'_id': 0, 'color': '$_id', 'results': 1}}]
            elif active_analysis == 'monkey_test':
                additional_pipeline = [
                    {'$match': {'analysis_type': 'monkey'}},
                    {'$project': {'id': {'$toString': '$_id'},
                                  'smart_sense': '$smart_sense_times',
                                  'duration_time': '$user_config.duration'}},
                    {'$group': {'_id': None, 'results': {'$push': '$$ROOT'}}}]
            elif active_analysis == 'intelligent_monkey_test':
                additional_pipeline = [
                    {'$match': {'analysis_type': 'intelligent_monkey'}},
                    {'$group': {'_id': ['$section_id', '$image_path'], 'smart_sense': {'$sum': '$smart_sense_times'}}},
                    {'$project': {'_id': 0,
                                  'smart_sense': '$smart_sense',
                                  'section_id': {'$arrayElemAt': ['$_id', 0]},
                                  'image_path': {'$arrayElemAt': ['$_id', 1]}}},
                    {'$sort': {'section_id': 1}},
                    {'$group': {'_id': None, 'results': {'$push': {'section_id': '$section_id',
                                                                   'smart_sense': '$smart_sense',
                                                                   'image_path': '$image_path'}}}}]
            elif active_analysis == 'macroblock':
                additional_pipeline = [
                    {'$match': {'user_config': config}},
                    {'$group': {'_id': 'testrun_id', 'duration': {'$avg': '$duration'}}}]
            elif active_analysis == 'channel_change_time':
                additional_pipeline = [
                    {'$project': {'_id': 0, 'measure_time': 1, 'targets': '$user_config.targets'}},
                    {'$unwind': {'path': '$targets'}},
                    {'$group': {'_id': '$targets',
                                'avg_time': {'$avg': '$measure_time'},
                                'total': {'$sum': 1}}},
                    {'$group': {'_id': None,
                                'results': {'$push': {'target': '$_id',
                                                      'avg_time': '$avg_time',
                                                      'total': '$total'}}}}]
            elif active_analysis == 'process_lifecycle_analysis':
                continue
            elif active_analysis == 'network_filter':
                continue
            elif active_analysis == 'loudness':
                additional_pipeline = [
                    {'$project': {'_id': 0, 'lines': 1}},
                    {'$unwind': {'path': '$lines'}},
                    {'$group': {'_id': None, 'lkfs': {'$avg': '$lines.I'}}},
                    {'$project': {'_id': 0, 'lkfs': 1}}]
            pipeline = basic_pipeline + additional_pipeline
            aggregation = aggregate_from_mongodb(col=analysis_collection[active_analysis], pipeline=pipeline)
            if len(aggregation) == 0:
                continue
            else:
                aggregation = aggregation[0]
            aggregation['color'] = config.get('color', '')
            result[active_analysis] = aggregation
        timestamp_pipeline = [{'$match': {'id': scenario_id}},
                              {'$project': {'_id': 0, 'testruns': 1}},
                              {'$unwind': {'path': '$testruns'}},
                              {'$match': {'testruns.id': testrun_id}},
                              {'$project': {'last_updated_timestamp': '$testruns.last_updated_timestamp'}}]
        last_updated_timestamp = aggregate_from_mongodb(col='scenario', pipeline=timestamp_pipeline)
        last_updated_timestamp = last_updated_timestamp[0].get('last_updated_timestamp', None)\
            if len(last_updated_timestamp) > 0 else None
        result['last_updated_timestamp'] = last_updated_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')\
            if (last_updated_timestamp is not None) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": result}


@router.post("/export")
async def export_result(
    export_in: schemas.ExportResult,
):
    try:
        now = datetime.today().strftime('%Y-%m-%dT%H%M%SF%f')
        export_type = {
            'file': ['videos', 'frames', 'monkey'],  # TODO
            'db': ['scenario', 'stb_log', 'stb_info', 'loudness', 'network_trace', 'terminal_log',
                   'monkey_smart_sense', 'monkey_section', 'an_color_reference', 'an_freeze',
                   'an_warm_boot', 'an_cold_boot', 'an_log_pattern', 'video_snapshot']
        }
        export_item = {key: [item for item in jsonable_encoder(export_in.items) if item in values]
                       for key, values in export_type.items()}
        scenario_id = export_in.scenario_id if export_in.scenario_id else RedisClient.hget('testrun', 'scenario_id')
        testrun_id = export_in.testrun_id if export_in.testrun_id else RedisClient.hget('testrun', 'id')

        tar_gz_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_gz_buffer, mode="w:gz") as tarf:
            for file_type in export_item['file']:
                path = f"{RedisClient.hget('testrun', 'workspace_path')}/{testrun_id}/raw/{file_type}"
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, path)
                        tarf.add(file_path, arcname=os.path.join(
                            'file', f'{testrun_id}', 'raw', file_type, relative_path))

            for collection_name in export_item['db']:
                param = {'id': scenario_id} if collection_name == 'scenario' \
                    else {'scenario_id': scenario_id, 'testrun_id': testrun_id}
                for document in load_from_mongodb(collection_name, param):
                    file_path = f"db/{collection_name}/{document['_id']}.json"
                    del document['_id']
                    data = json.dumps(document, indent=4, ensure_ascii=False, default=serialize_datetime)
                    info = tarfile.TarInfo(file_path)
                    info.size = len(data)
                    tarf.addfile(info, io.BytesIO(data.encode('utf-8')))

        tar_gz_buffer.seek(0)
        headers = {"Content-Disposition": f"attachment; filename=results_{now}.tar.gz"}
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return Response(content=tar_gz_buffer.read(), headers=headers, media_type="application/tar+gzip")


@router.post("/import", response_model=schemas.Msg)
async def import_result(file: UploadFile = File(...)) -> schemas.Msg:
    try:
        scenario_id = str(uuid.uuid4())
        tar_gz_data = await file.read()
        with tarfile.open(fileobj=io.BytesIO(tar_gz_data), mode="r:gz") as tarf:
            for tar_info in tarf:
                if tar_info.isfile():
                    file_data = tarf.extractfile(tar_info).read()
                    file_path = tar_info.name.split('/')
                    file_type = file_path[0]
                    file_name = file_path[-1]
                    file_path = '/'.join(file_path[1:-1])

                    if file_type == 'file':
                        workspace_path = RedisClient.hget('testrun', 'workspace_path')
                        real_path = f"{workspace_path}/{file_path}"
                        if not os.path.isdir(real_path):
                            os.makedirs(real_path, exist_ok=True)
                        with open(f'{real_path}/{file_name}', 'wb') as f:
                            f.write(file_data)

                    if file_type == 'db':
                        collection_name = os.path.dirname(f'{file_path}/{file_name}')
                        data = deserialize_datetime(convert_data_in(
                            scenario_id, collection_name, json.loads(file_data.decode("utf-8"))))
                        # data = deserialize_datetime(json.loads(file_data.decode("utf-8")))
                        insert_one_to_mongodb(col=collection_name, data=data)
    except Exception as e:
        logger.error(traceback.format_exc())
        # raise HTTPException(status_code=500, detail=traceback.format_exc())
    finally:
        pass
    return {'msg': f"Data from {file.filename} uploaded and restored to corresponding collections"}
