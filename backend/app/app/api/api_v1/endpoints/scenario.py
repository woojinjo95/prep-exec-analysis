import logging
import time
import uuid

from app import schemas
from app.api.utility import get_multi_or_paginate_by_res
from app.crud.base import (insert_one_to_mongodb, load_by_id_from_mongodb,
                           update_by_id_to_mongodb)
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
    res = update_by_id_to_mongodb(col='scenario',
                                  id=scenario_id,
                                  data={'block_group': jsonable_encoder(scenario_in.block_group),
                                        "updated_at": time.time()})
    if res.matched_count == 0:
        raise HTTPException(
            status_code=406, detail="No items have been updated.")
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
    scenario_in = schemas.ScenarioBase(
        id=str(uuid.uuid4()),
        name=time.time(),
        updated_at=time.time(),
        tags=[],
        block_group=[],
    )
    insert_one_to_mongodb(col='scenario', data=jsonable_encoder(scenario_in))
    return {'msg': 'Create new scenario', 'id': scenario_in.id}
