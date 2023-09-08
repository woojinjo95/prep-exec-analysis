import logging
import os
import time
import traceback
import uuid
from datetime import datetime
from typing import Optional

from app import schemas
from app.api.utility import (get_utc_datetime,
                             paginate_from_mongodb_aggregation,
                             parse_bytes_to_value, set_ilike,
                             set_redis_pub_msg)
from app.crud.base import (count_from_mongodb, delete_part_to_mongodb,
                           insert_one_to_mongodb, load_by_id_from_mongodb,
                           update_by_id_to_mongodb)
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{scenario_id}", response_model=schemas.Scenario)
def read_scenario_by_id(
    scenario_id: str,
) -> schemas.Scenario:
    """
    Get a specific scenario by id.
    """
    scenario = load_by_id_from_mongodb(col='scenario', id=scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=404, detail="The scenario with this id does not exist in the system.")
    return {'items': scenario}


@router.put("/{scenario_id}", response_model=schemas.Msg)
def update_scenario(
    *,
    scenario_id: str,
    scenario_in: schemas.ScenarioUpdate,
) -> schemas.Msg:
    """
    Update a scenario.
    """
    scenario = load_by_id_from_mongodb(col='scenario', id=scenario_id, proj={'_id': 0, 'name': 1})
    if not scenario:
        raise HTTPException(status_code=404,
                            detail="The scenario with this id does not exist in the system.")

    if scenario['name'] != scenario_in.name\
            and count_from_mongodb(col='scenario', param={"name": scenario_in.name}) > 0:
        raise HTTPException(
            status_code=406, detail="The scenario name already exists in the system.")

    try:
        scenario_in.tags = list(set(scenario_in.tags)) if scenario_in.tags else []
        if scenario_in.tags:
            tags = RedisClient.hget('testrun', 'tags')
            tag_list = parse_bytes_to_value(tags) if tags else []
            RedisClient.hset('testrun', 'tags',
                             f'{list(set([tag for tag in scenario_in.tags if tag not in tag_list] + tag_list))}')

        update_by_id_to_mongodb(col='scenario',
                                id=scenario_id,
                                data={'updated_at': get_utc_datetime(time.time()),
                                      'is_active': scenario_in.is_active,
                                      'name': scenario_in.name,
                                      'tags': scenario_in.tags,
                                      'block_group': jsonable_encoder(scenario_in.block_group)})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update a scenario.'}


@router.delete("/{scenario_id}", response_model=schemas.Msg)
def delete_scenario(
    scenario_id: str,
) -> schemas.Msg:
    """
    Delete a scenario.
    """
    scenario = load_by_id_from_mongodb(col='scenario', id=scenario_id, proj={'_id': 0, 'name': 1})
    if not scenario:
        raise HTTPException(status_code=404,
                            detail="The scenario with this id does not exist in the system.")

    try:
        now = time.time()
        update_by_id_to_mongodb(col='scenario',
                                id=scenario_id,
                                data={'updated_at': get_utc_datetime(now),
                                      'is_active': False,
                                      'name': str(now)})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Delete a scenario.'}


@router.get("", response_model=schemas.ScenarioPage)
def read_scenarios(
    page: int = Query(None, ge=1),
    page_size: int = Query(None, ge=1, le=30),
    sort_by: Optional[str] = None,
    sort_desc: Optional[bool] = None,
    name: Optional[str] = None,
    tag: Optional[str] = None,
) -> schemas.ScenarioPage:
    """
    Retrieve scenarios.
    """
    try:
        param = {'is_active': True}
        if name:
            param['name'] = set_ilike(name)
        if tag:
            param['tags'] = tag

        pipeline = [{'$match': param},
                    {'$project': {'id': '$id',
                                  'name': '$name',
                                  'tags': '$tags',
                                  'updated_at': '$updated_at',
                                  "testrun_count": {"$size": {"$filter": {"input": "$testruns",
                                                                          "as": "testrun",
                                                                          "cond": {"$ifNull": ["$$testrun.last_updated_timestamp", False]}}}},
                                  'has_block': {'$cond': {'if': {'$eq': [{'$size': '$block_group'}, 0]},
                                                          'then': False,
                                                          'else': True}}
                                  }}]
        res = paginate_from_mongodb_aggregation(col='scenario',
                                                pipeline=pipeline,
                                                page=page,
                                                page_size=page_size,
                                                sort_by=sort_by if sort_by else 'updated_at',
                                                sort_desc=sort_desc if sort_desc is not None else True)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return res


@router.post("", response_model=schemas.ScenarioCreateResult)
def create_scenario(
    *,
    scenario_in: schemas.ScenarioCreate,
) -> schemas.ScenarioCreateResult:
    """
    Create new scenario.
    """
    scenario_in.name = scenario_in.name if scenario_in.name else str(time.time())
    if count_from_mongodb(col='scenario', param={"name": scenario_in.name}) > 0:
        raise HTTPException(
            status_code=406, detail="The scenario name already exists in the system.")

    try:
        scenario_in.tags = list(set(scenario_in.tags)) if scenario_in.tags else []
        if scenario_in.tags:
            tags = RedisClient.hget('testrun', 'tags')
            tag_list = parse_bytes_to_value(tags) if tags else []
            RedisClient.hset('testrun', 'tags',
                             f'{list(set([tag for tag in scenario_in.tags if tag not in tag_list] + tag_list))}')

        workspace_path = RedisClient.hget('testrun', 'workspace_path')
        scenario_id = str(uuid.uuid4())
        testrun_id = datetime.now().strftime("%Y-%m-%dT%H%M%SF%f")
        block_groups = jsonable_encoder(scenario_in.block_group) if scenario_in.block_group else []
        block_group_data = [
            {
                **block_group,
                "id": str(uuid.uuid4()),
                "block": [
                    {**block, "id": str(uuid.uuid4())}
                    for block in block_group.get('block', [])
                ]
            }
            for block_group in block_groups
        ]

        # 폴더 생성
        path = f"{workspace_path}/{testrun_id}"
        os.makedirs(f'{path}/raw')
        os.makedirs(f'{path}/analysis')

        # 시나리오 등록
        insert_one_to_mongodb(col='scenario', data={'id': scenario_id,
                                                    'updated_at': get_utc_datetime(time.time()),
                                                    'is_active': scenario_in.is_active,
                                                    'name': scenario_in.name,
                                                    'tags': scenario_in.tags,
                                                    'block_group': block_group_data,
                                                    'testruns': [{'id': testrun_id,
                                                                  'raw': {'videos': []},
                                                                  'analysis': {}}]})

        # 워크스페이스 변경
        RedisClient.hset('testrun', 'id', testrun_id)
        RedisClient.hset('testrun', 'scenario_id', scenario_id)

        # 워크스페이스 변경 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="workspace",
                                              data={"workspace_path": workspace_path,
                                                    "testrun_id": testrun_id,
                                                    "scenario_id": scenario_id}))

    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new scenario', 'id': scenario_id, 'testrun_id': testrun_id}


router_detail = APIRouter()


@router_detail.post("", response_model=schemas.ScenarioCreateResult)
def copy_scenario(
    *,
    scenario_in: schemas.CopyScenarioCreate,
) -> schemas.ScenarioCreateResult:
    """
    Copy scenario.
    """
    scenario = load_by_id_from_mongodb(col='scenario', id=scenario_in.src_scenario_id,
                                       proj={'_id': 0, 'testruns': 1})
    if not scenario:
        raise HTTPException(status_code=404,
                            detail="The scenario with this id does not exist in the system.")

    if count_from_mongodb(col='scenario', param={"name": scenario_in.name}) > 0:
        raise HTTPException(
            status_code=406, detail="The scenario name already exists in the system.")

    try:
        scenario_in.tags = list(set(scenario_in.tags)) if scenario_in.tags else []
        if scenario_in.tags:
            tags = RedisClient.hget('testrun', 'tags')
            tag_list = parse_bytes_to_value(tags) if tags else []
            RedisClient.hset('testrun', 'tags',
                             f'{list(set([tag for tag in scenario_in.tags if tag not in tag_list] + tag_list))}')

        workspace_path = RedisClient.hget('testrun', 'workspace_path')
        scenario_id = str(uuid.uuid4())
        block_groups = jsonable_encoder(scenario_in.block_group) if scenario_in.block_group else []
        block_group_data = [
            {
                **block_group,
                "id": str(uuid.uuid4()),
                "block": [
                    {**block, "id": str(uuid.uuid4())}
                    for block in block_group.get('block', [])
                ]
            }
            for block_group in block_groups
        ]

        src_testrun_id = RedisClient.hget('testrun', 'id')
        src_testrun = next((item for item in scenario.get('testruns', [])
                            if item['id'] == src_testrun_id), None)

        # 기존 시나리오에 testrun이 있을 경우
        if src_testrun:
            testrun_id = src_testrun_id
            testruns = [src_testrun]
            delete_part_to_mongodb(col='scenario',
                                   param={'id': scenario_in.src_scenario_id},
                                   data={"testruns": {"id": src_testrun_id}})
        else:
            testrun_id = datetime.now().strftime("%Y-%m-%dT%H%M%SF%f")
            testruns = [{'id': testrun_id,
                        'raw': {'videos': []},
                         'analysis': {}}]

            # 폴더 생성
            path = f'{workspace_path}/{testrun_id}'
            os.makedirs(f'{path}/raw')
            os.makedirs(f'{path}/analysis')

        # 시나리오 복제
        insert_one_to_mongodb(col='scenario', data={'id': scenario_id,
                                                    'updated_at': get_utc_datetime(time.time()),
                                                    'is_active': True,
                                                    'name': scenario_in.name,
                                                    'tags': scenario_in.tags,
                                                    'block_group': block_group_data,
                                                    'testruns': testruns})

        # 워크스페이스 변경
        RedisClient.hset('testrun', 'id', testrun_id)
        RedisClient.hset('testrun', 'scenario_id', scenario_id)

        # 워크스페이스 변경 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="workspace",
                                              data={"workspace_path": workspace_path,
                                                    "testrun_id": testrun_id,
                                                    "scenario_id": scenario_id}))

    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Copy scenario', 'id': scenario_id, 'testrun_id': testrun_id}
