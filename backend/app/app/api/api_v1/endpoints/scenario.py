import logging
import os
import time
import traceback
import uuid
from datetime import datetime

from app import schemas
from app.api.utility import get_multi_or_paginate_by_res
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
        RedisClient.hset('testrun', 'dir', scenario.get('testrun', {}).get('dir', 'null'))
        RedisClient.hset('testrun', 'scenario_id', scenario.get('id', 'null'))
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
        res = update_by_id_to_mongodb(col='scenario',
                                      id=scenario_id,
                                      data={'block_group': jsonable_encoder(scenario_in.block_group),
                                            "updated_at": time.time()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update a scenario.'}


@router.get("", response_model=schemas.ScenarioPage)
def read_scenarios(
    page: int = Query(None, ge=1, description="Page number"),
    page_size: int = Query(None, ge=1, le=100, description="Page size")
) -> schemas.ScenarioPage:
    """
    Retrieve scenarios.
    """
    return get_multi_or_paginate_by_res(col='scenario', page=page, page_size=page_size, sorting_keyword='name')


@router.post("", response_model=schemas.MsgWithId)
def create_scenario(
    *,
    scenario_in: schemas.ScenarioCreate,
) -> schemas.MsgWithId:
    """
    Create new scenario.
    """
    try:
        dir = datetime.now().strftime("%Y-%m-%dT%H%M%SF%f")
        scenario_in = schemas.ScenarioBase(
            id=str(uuid.uuid4()),
            updated_at=time.time(),
            block_group=[],
            name=scenario_in.name if scenario_in.name else time.time(),
            tags=scenario_in.tags if scenario_in.tags else [],
            testrun=schemas.Testrun(dir=dir,
                                    raw=schemas.TestrunRaw(videos=[]),
                                    analysis=schemas.TestrunAnalysis(videos=[])))
        # 시나리오 등록
        insert_one_to_mongodb(col='scenario', data=jsonable_encoder(scenario_in))

        # 워크스페이스 변경
        RedisClient.hset('testrun', 'dir', dir)
        RedisClient.hset('testrun', 'scenario_id', scenario_in.id)

        # 폴더 생성
        path = f'/app/workspace/testruns/{dir}'
        os.makedirs(f'{path}/raw')
        os.makedirs(f'{path}/analysis')
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new scenario', 'id': scenario_in.id}
