import datetime as dt
import json
import logging
import math
import os
import time
import traceback
from ast import literal_eval
from datetime import datetime

from app import schemas
from app.core.config import settings
from app.crud.base import (aggregate_from_mongodb, load_from_mongodb,
                           load_paginate_from_mongodb)
from app.db.redis_session import RedisClient
from dateutil.parser import isoparse
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()
analysis_collection = {
    "log_level_finder": "stb_log",
    "freeze": "an_freeze",
    "resume": "an_warm_boot",
    "boot": "an_cold_boot",
    "log_pattern_matching": "an_log_pattern",
    "loudness": "loudness",
    "cpu": "stb_info",
    "memory": "stb_info",
    "event_log": "event_log",
    "color_reference": "an_color_reference",
    "monkey_test": "monkey_section",
    "intelligent_monkey_test": "monkey_section"
}


def convert_pageset(page_param, res):
    page = page_param['page']
    page_size = page_param['page_size']
    total = page_param['total']
    pages = math.ceil(total / page_size)

    return {
        "total": total,
        "pages": pages,
        "prev": None if page == 1 or page > pages else page - 1,
        "next": None if page >= pages else page + 1,
        "items": res
    }


def paginate_from_mongodb(col, page, page_size=None, param={}, sorting_keyword=None, is_descending=False, proj=None):
    page_size = page_size if page_size else 30
    res = load_paginate_from_mongodb(
        col=col, page=page, page_size=page_size, param=param, proj=proj, sort_item=None
        if sorting_keyword is None else [(sorting_keyword, -1 if is_descending else 1)])
    page_param = {
        'page': page,
        'page_size': page_size,
        'total': res.get('total', 1)
    }
    return convert_pageset(page_param, list(res.get('items', [])))


def get_multi_or_paginate_by_res(col, page, page_size=10, sorting_keyword=None, is_descending=None, proj=None, param={}):
    if page:
        res_dict = paginate_from_mongodb(col=col,
                                         page=page,
                                         page_size=page_size,
                                         param=param,
                                         sorting_keyword=sorting_keyword,
                                         is_descending=is_descending,
                                         proj=proj)
    else:
        res = load_from_mongodb(col=col, param=param, proj=proj)
        res_dict = {
            "total": len(res),
            "pages": None,
            "prev": None,
            "next": None,
            "items": res
        }
    return res_dict


def classify_file_type(file_name):
    file_exp = file_name.split('.')[-1]
    if file_exp in ['jpg', 'png', 'jpeg', 'gif']:
        file_dir = os.path.join(settings.FILES_PATH, 'images')
    elif file_exp in ['mp4', 'avi']:
        file_dir = os.path.join(settings.FILES_PATH, 'videos')
    else:
        file_dir = os.path.join(settings.FILES_PATH, 'etc')
    return file_dir


def parse_bytes_to_value(value: bytes) -> any:
    decoded = value.decode() if isinstance(value, bytes) else value
    try:
        value = literal_eval(decoded)
    except:
        value = decoded
    return value


def set_redis_pub_msg(msg: str, data: dict = {}, service: str = 'backend', level: str = 'info'):
    return json.dumps({
        "service": service,
        "level": level,
        "time": time.time(),
        "msg": msg,
        "data": data
    })


def get_utc_datetime(timestamp: float, remove_float_point: bool = False) -> datetime:
    dt_obj = datetime.utcfromtimestamp(timestamp)
    if remove_float_point:
        dt_obj = dt_obj.replace(microsecond=0)
    return dt_obj


def convert_iso_format(input_str: str):
    if 'Z' in input_str:
        input_str = input_str.replace('Z', '+00:00')
    return datetime.fromisoformat(input_str)


def set_ilike(param):
    item = param.replace("(", "\\(").replace(")", "\\)")
    return {'$regex': item, '$options': 'i'}


def paginate_from_mongodb_aggregation(col: str, pipeline: list, sort_by: str, page: int, page_size: int = 10, sort_desc: bool = False):
    if sort_by is not None:
        sorting_pipeline = [{'$sort': {sort_by: -1 if sort_desc else 1}}]
        pipeline.extend(sorting_pipeline)
    if page:
        skip_num = (page - 1) * page_size
        paging_pipeline = [{'$facet': {'page_info': [{'$count': 'total'}],
                                       'items': [{'$skip': skip_num},
                                                 {'$limit': page_size}]}},
                           {'$project': {'total': {'$arrayElemAt': ['$page_info.total', 0]},
                                         'pages': {'$ceil': {'$divide': [{'$arrayElemAt': ['$page_info.total', 0]}, page_size]}},
                                         'items': 1}},
                           {'$addFields': {'prev': {'$cond': [{'$eq': [page, 1]}, None, {'$subtract': [page, 1]}]},
                                           'next': {'$cond': [{'$gt': ['$pages', page]}, {'$add': [page, 1]}, None]}}}]
        pipeline.extend(paging_pipeline)
    result = aggregate_from_mongodb(col=col, pipeline=pipeline)
    if page:
        return result[0]
    else:
        return {'total': len(result), 'pages': None, 'prev': None, 'next': None, 'items': result}


def deserialize_datetime(json_obj):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            json_obj[key] = deserialize_datetime(value)
    elif isinstance(json_obj, list):
        for i in range(len(json_obj)):
            json_obj[i] = deserialize_datetime(json_obj[i])
    elif isinstance(json_obj, str):
        try:
            return isoparse(json_obj)
        except (TypeError, ValueError):
            pass
    return json_obj


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        utc_timezone = dt.timezone.utc
        utc_datetime = obj.replace(tzinfo=utc_timezone)
        return utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def get_config_from_scenario_mongodb(scenario_id: str, testrun_id: str):
    pipeline = [{"$match": {'id': scenario_id}},
                {"$unwind": "$testruns"},
                {"$project": {"testrun_id": "$testruns.id",
                              "config": f"$testruns.analysis.config"}},
                {"$match": {"testrun_id": testrun_id}},
                {"$project": {"_id": 0, "config": 1}}]
    res = aggregate_from_mongodb('scenario', pipeline)
    return res[0] if len(res) > 0 else {}


def convert_data_in(scenario_id, collection_name, document):
    data = {}
    try:
        if collection_name == 'scenario':
            data = schemas.ImportScenario(
                id=scenario_id,
                updated_at=document.get('updated_at', None),
                is_active=document.get('is_active', None),
                name=f"{document.get('name')}_{datetime.today().strftime('%Y-%m-%dT%H%M%SF%f')}",
                tags=document.get('tags', None),
                block_group=document.get('block_group', None),
                testruns=document.get('testruns', None),
            )
        elif collection_name == 'event_log':
            data = schemas.ImportEventLog(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                lines=document.get('lines', None),
            )
        elif collection_name == 'loudness':
            data = schemas.ImportLoudness(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                lines=document.get('lines', None),
            )
        elif collection_name == 'monkey_section':
            data = schemas.ImportMonkeySection(
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                timestamp=document.get('timestamp', None),
                start_timestamp=document.get('start_timestamp', None),
                end_timestamp=document.get('end_timestamp', None),
                analysis_type=document.get('analysis_type', None),
                section_id=document.get('section_id', None),
                image_path=document.get('image_path', None),
                smart_sense_times=document.get('smart_sense_times', None),
                user_config=document.get('user_config', None),
            )
        elif collection_name == 'monkey_smart_sense':
            data = schemas.ImportMonkeySmartSense(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),  # timestamp 확인
                analysis_type=document.get('analysis_type', None),
                section_id=document.get('section_id', None),
                smart_sense_key=document.get('smart_sense_key', None),
                user_config=document.get('user_config', None),
            )
        elif collection_name == 'network_trace':
            data = schemas.ImportNetworkTrace(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                lines=document.get('lines', None),
            )
        elif collection_name == 'shell_log':
            data = schemas.ImportShellLog(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                mode=document.get('mode', None),
                lines=document.get('lines', None),
            )
        elif collection_name == 'stb_info':
            data = schemas.ImportStbInfo(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                cpu_usage=document.get('cpu_usage', None),
                total=document.get('total', None),
                user=document.get('user', None),
                kernel=document.get('kernel', None),
                iowait=document.get('iowait', None),
                irq=document.get('irq', None),
                softirq=document.get('softirq', None),
                memory_usage=document.get('memory_usage', None),
                total_ram=document.get('total_ram', None),
                free_ram=document.get('free_ram', None),
                used_ram=document.get('used_ram', None),
                lost_ram=document.get('lost_ram', None),
            )
        elif collection_name == 'stb_log':
            data = schemas.ImportStbLog(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                lines=document.get('lines', None),
            )
        elif collection_name == 'video_snapshot':
            data = schemas.ImportVideoSnapshot(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                video_path=document.get('video_path', None),
                path=document.get('path', None),
                extension=document.get('extension', None),
                names=document.get('names', None),
            )
        elif collection_name == 'an_cold_boot':
            data = schemas.ImportAnColdBoot(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                measure_time=document.get('measure_time', None),
                user_config=document.get('user_config', None),
            )
        elif collection_name == 'an_color_reference':
            data = schemas.ImportAnColorReference(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                color_reference=document.get('color_reference', None),
                user_config=document.get('user_config', None),
            )
        elif collection_name == 'an_freeze':
            data = schemas.ImportAnFreeze(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                freeze_type=document.get('freeze_type', None),
                duration=document.get('duration', None),
                user_config=document.get('user_config', None),
            )
        elif collection_name == 'an_log_pattern':
            data = schemas.ImportAnLogPattern(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                module=document.get('module', None),
                log_level=document.get('log_level', None),
                process_name=document.get('process_name', None),
                pid=document.get('pid', None),
                tid=document.get('tid', None),
                message=document.get('message', None),
                matched_target=document.get('matched_target', None),
                user_config=document.get('user_config', None),
            )
        elif collection_name == 'an_warm_boot':
            data = schemas.ImportAnWarmBoot(
                timestamp=document.get('timestamp', None),
                scenario_id=scenario_id,
                testrun_id=document.get('testrun_id', None),
                measure_time=document.get('measure_time', None),
                user_config=document.get('user_config', None),
            )
        else:
            raise HTTPException(status_code=404, detail='This is undefined collection_name')
    except Exception as e:
        logging.info(traceback.format_exc())
        # raise HTTPException(status_code=422, detail=traceback.format_exc())
    finally:
        pass
    return jsonable_encoder(data)


def make_basic_match_pipeline(scenario_id: str = None, testrun_id: str = None, start_time: str = None, end_time: str = None):
    time_range = {}
    if start_time:
        time_range['$gte'] = convert_iso_format(start_time)
    if end_time:
        time_range['$lte'] = convert_iso_format(end_time)
    if testrun_id is None:
        testrun_id = RedisClient.hget('testrun', 'id')
    if scenario_id is None:
        scenario_id = RedisClient.hget('testrun', 'scenario_id')

    return [{'$match': {'timestamp': time_range,
                        'scenario_id': scenario_id,
                        'testrun_id': testrun_id}}]
