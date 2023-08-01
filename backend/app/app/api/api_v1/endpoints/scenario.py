import logging

from app import schemas
from app.crud.base import load_from_mongodb, update_many_to_mongodb
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.Scenario)
def read_scenario() -> schemas.Scenario:
    """
    Retrieve scenario.
    """
    res = load_from_mongodb(col='scenario')
    return {'items': res[0] if res else {}}


@router.put("", response_model=schemas.Msg)
def update_scenario(
    *,
    scenario_in: schemas.ScenarioBase,
) -> schemas.Msg:
    """
    Update a scenario.
    """
    res = update_many_to_mongodb(col='scenario',
                                     data={'block_group': jsonable_encoder(scenario_in.block_group)})
    if res.matched_count == 0:
        raise HTTPException(
            status_code=406, detail="No items have been updated.")
    return {'msg': 'Update a scenario.'}
