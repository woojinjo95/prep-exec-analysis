import logging
import os
import time
import traceback
import uuid
from datetime import datetime
from typing import Optional

from app import schemas
from app.api.utility import (get_multi_or_paginate_by_res, get_utc_datetime,
                             set_ilike, set_redis_pub_msg)
from app.crud.base import (aggregate_from_mongodb, get_mongodb_collection,
                           insert_one_to_mongodb, load_by_id_from_mongodb,
                           update_by_id_to_mongodb)
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/tag", response_model=schemas.ScenarioTag)
def read_scenario_tags() -> schemas.ScenarioTag:
    """
    Retrieve scenario tags.
    """
    try:
        pipeline = [
            {'$unwind': '$tags'},
            {'$group': {'_id': None, 'tags': {'$addToSet': '$tags'}}},
            {'$project': {'_id': 0, 'tags': 1}}
        ]
        mongo_res = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
        res = {} if len(mongo_res) == 0 else {'tags': sorted(mongo_res[0]['tags'])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': res}


@router.put("/tag/{tag}", response_model=schemas.Msg)
def update_scenario_tag(
    *,
    tag: str,
    tag_in: schemas.ScenarioTagUpdate,
) -> schemas.Msg:
    """
    Update a scenario tag.
    """
    try:
        col = get_mongodb_collection('scenario')
        col.update_many(
            {"tags": tag},
            {"$set": {"tags.$[elem]": tag_in.tag}},
            array_filters=[{"elem": tag}]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update a scenario tag.'}


@router.delete("/tag/{tag}", response_model=schemas.Msg)
def delete_scenario_tag(
    *,
    tag: str,
) -> schemas.Msg:
    """
    Delete a scenario tag.
    """
    try:
        col = get_mongodb_collection('scenario')
        col.update_many(
            {"tags": tag},
            {"$pull": {"tags": tag}}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Delete a scenario tag.'}


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
    try:
        # 워크스페이스 변경
        testrun_id = scenario.get('testrun', {}).get('id', 'null')
        RedisClient.hset('testrun', 'id', testrun_id)
        RedisClient.hset('testrun', 'scenario_id', scenario_id)

        # 워크스페이스 변경 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="workspace",
                                              data={"workspace_path": RedisClient.hget('testrun', 'workspace_path'),
                                                    "id": testrun_id,
                                                    "scenario_id": scenario_id}))

        # 로그 수집시작 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="stb_log",
                                              data={"control": "start"}))

        # 스트리밍 시작 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="streaming",
                                              data={"action": "start"}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
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
    try:
        update_by_id_to_mongodb(col='scenario',
                                id=scenario_id,
                                data={'is_active': scenario_in.is_active,
                                      'updated_at': get_utc_datetime(time.time()),
                                      'block_group': jsonable_encoder(scenario_in.block_group), })
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update a scenario.'}


@router.get("", response_model=schemas.ScenarioPage)
def read_scenarios(
    page: int = Query(None, ge=1),
    page_size: int = Query(None, ge=1, le=100),
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
            param['tags'] = {'$elemMatch': set_ilike(tag)}
        res = get_multi_or_paginate_by_res(col='scenario',
                                           page=page,
                                           page_size=page_size,
                                           sorting_keyword='name',
                                           param=param)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return res


@router.post("", response_model=schemas.MsgWithId)
def create_scenario(
    *,
    scenario_in: schemas.ScenarioCreate,
) -> schemas.MsgWithId:
    """
    Create new scenario.
    """
    try:
        scenario_id = str(uuid.uuid4())
        testrun_id = datetime.now().strftime("%Y-%m-%dT%H%M%SF%f")
        data = {'id': scenario_id,
                'is_active': scenario_in.is_active,
                'updated_at': get_utc_datetime(time.time()),
                'block_group': jsonable_encoder(scenario_in.block_group) if scenario_in.block_group else [],
                'name': scenario_in.name if scenario_in.name else str(time.time()),
                'tags': scenario_in.tags if scenario_in.tags else [],
                'testrun': {'id': testrun_id,
                            'raw': {'videos': []},
                            'analysis': {'videos': []}}}

        # 시나리오 등록
        insert_one_to_mongodb(col='scenario', data=data)

        # 폴더 생성
        path = f'/app/workspace/testruns/{testrun_id}'
        os.makedirs(f'{path}/raw')
        os.makedirs(f'{path}/analysis')

    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new scenario', 'id': scenario_id}
