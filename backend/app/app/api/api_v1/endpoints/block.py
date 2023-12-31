import logging
import time
import traceback
import uuid

from app import schemas
from app.api.utility import get_utc_datetime
from app.crud.base import (delete_part_to_mongodb, get_mongodb_collection,
                           load_by_id_from_mongodb, load_from_mongodb,
                           update_by_id_to_mongodb, update_to_mongodb)
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/run_block", response_model=schemas.RunBlock)
def read_run_block() -> schemas.RunBlock:
    """
    Retrieve run block id.
    """
    return {'items': {'id': RedisClient.hget('testrun', 'run_block')}}


@router.post("/{scenario_id}", response_model=schemas.MsgWithId)
def create_block(
    *,
    scenario_id: str,
    block_in: schemas.BlockCreate,
) -> schemas.MsgWithId:
    """
    Create new block.
    """
    scenario = load_by_id_from_mongodb('scenario', scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="The scenario with this id does not exist in the system.")
    try:
        block_id = str(uuid.uuid4())
        block_in = jsonable_encoder(block_in)
        block_in['id'] = block_id
        block_group = scenario.get('block_group', [])

        if len(block_group) == 0:
            new_last_block_group = [{"id": str(uuid.uuid4()),
                                    "repeat_cnt": 1,
                                     "block": [block_in]}]
        else:
            last_block_group = block_group[-1]
            new_last_block_group = [item for item in block_group
                                    if item != last_block_group]

            new_blocks = last_block_group.get('block', [])
            new_blocks.append(block_in)
            new_last_block_group.append({"id": last_block_group.get('id', ''),
                                        "repeat_cnt": last_block_group.get('repeat_cnt', 0),
                                         "block": new_blocks})
        update_by_id_to_mongodb(col='scenario',
                                id=scenario_id,
                                data={'updated_at': get_utc_datetime(time.time()),
                                      'block_group': new_last_block_group})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new block', 'id': block_id}


@router.delete("/{scenario_id}", response_model=schemas.Msg)
def delete_blocks(
    scenario_id: str,
    block_in: schemas.BlockDelete,
) -> schemas.Msg:
    """
    Delete blocks.
    """
    scenario = load_by_id_from_mongodb('scenario', scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="The scenario with this id does not exist in the system.")
    try:
        for block_id in block_in.block_ids:
            delete_part_to_mongodb(col='scenario',
                                   param={'id': scenario_id,
                                          'block_group': {'$elemMatch': {'block.id': block_id}}},
                                   data={'block_group.$.block': {'id': block_id}})
        delete_part_to_mongodb(col='scenario',
                               param={'id': scenario_id,
                                      'block_group.block': {'$size': 0}},
                               data={'block_group': {'block': {'$size': 0}}})
        update_by_id_to_mongodb(col='scenario', id=scenario_id, data={"updated_at": get_utc_datetime(time.time())})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Delete blocks.'}


@router.put("/{scenario_id}/{block_id}", response_model=schemas.MsgWithId)
def update_block(
    *,
    scenario_id: str,
    block_id: str,
    block_in: schemas.BlockUpdate,
) -> schemas.MsgWithId:
    """
    Update a block.
    """
    block = load_from_mongodb(col='scenario',
                              param={"id": scenario_id,
                                     "block_group": {"$elemMatch": {"block.id": block_id}}},
                              proj={"_id": 1})
    if not block:
        raise HTTPException(
            status_code=404, detail="The block with this id does not exist in the system.")

    try:
        update_data = {f"block_group.$.block.$[elem].{key}": value
                       for key, value in jsonable_encoder(block_in).items() if value is not None}

        col = get_mongodb_collection('scenario')
        col.update_one({"id": scenario_id, "block_group.block.id": block_id},
                       {'$set': update_data},
                       array_filters=[{"elem.id": block_id}],
                       upsert=False)
        update_by_id_to_mongodb(col='scenario', id=scenario_id, data={"updated_at": get_utc_datetime(time.time())})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update a block', 'id': block_id}


router_detail = APIRouter()


@router_detail.post("/{scenario_id}", response_model=schemas.Msg)
def bulk_create_blocks(
    *,
    scenario_id: str,
    blocks_in: schemas.BlockBulkCreate,
) -> schemas.Msg:
    """
    Bulk Create blocks.
    """
    scenario = load_by_id_from_mongodb('scenario', scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="The scenario with this id does not exist in the system.")
    try:
        block_in = [{'id': str(uuid.uuid4()), **x} for x in jsonable_encoder(blocks_in.blocks)]
        block_group = scenario.get('block_group', [])

        if len(block_group) == 0:
            new_last_block_group = [{"id": str(uuid.uuid4()),
                                    "repeat_cnt": 1,
                                     "block": block_in}]
        else:
            last_block_group = block_group[-1]
            new_last_block_group = [item for item in block_group
                                    if item != last_block_group]

            new_blocks = last_block_group.get('block', [])
            new_last_block_group.append({"id": last_block_group.get('id', ''),
                                        "repeat_cnt": last_block_group.get('repeat_cnt', 0),
                                         "block": new_blocks+block_in})
        update_by_id_to_mongodb(col='scenario',
                                id=scenario_id,
                                data={'updated_at': get_utc_datetime(time.time()),
                                      'block_group': new_last_block_group})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Bulk Create blocks'}


block_group_router = APIRouter()


@block_group_router.put("/{scenario_id}/{block_group_id}", response_model=schemas.MsgWithId)
def update_block_group(
    *,
    scenario_id: str,
    block_group_id: str,
    block_group_in: schemas.BlockGroupUpdate,
) -> schemas.MsgWithId:
    """
    Update a block_group.
    """
    param = {"id": scenario_id, "block_group.id": block_group_id}
    block_group = load_from_mongodb(col='scenario',
                                    param=param,
                                    proj={"_id": 1})
    if not block_group:
        raise HTTPException(
            status_code=404, detail="The block_group with this id does not exist in the system.")
    try:
        update_data = {f"block_group.$.{key}": value
                       for key, value in jsonable_encoder(block_group_in).items() if value is not None}
        update_data['updated_at'] = get_utc_datetime(time.time())
        update_to_mongodb(col='scenario',
                          param=param,
                          data=update_data)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update a block_group', 'id': block_group_id}
