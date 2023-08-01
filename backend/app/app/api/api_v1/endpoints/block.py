import logging
import uuid

from app import schemas
from app.crud.base import (delete_part_to_mongodb, get_mongodb_collection,
                           load_from_mongodb, load_one_from_mongodb,
                           update_many_to_mongodb, update_to_mongodb)
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=schemas.MsgWithId)
def create_block(
    *,
    block_in: schemas.BlockCreate,
) -> schemas.MsgWithId:
    """
    Create new block.
    """
    block_in = schemas.Block(id=str(uuid.uuid4()),
                             type=block_in.type,
                             value=block_in.value,
                             delay_time=block_in.delay_time)
    block_group = load_one_from_mongodb('scenario').get('block_group', [])

    if len(block_group) == 0:
        new_last_block_group = [{"id": str(uuid.uuid4()),
                                 "repeat_cnt": 1,
                                 "block": [jsonable_encoder(block_in)]}]
    else:
        last_block_group = block_group[-1]
        new_last_block_group = [item for item in block_group
                                if item != last_block_group]

        new_blocks = last_block_group.get('block', [])
        new_blocks.append(jsonable_encoder(block_in))
        new_last_block_group.append({"id": last_block_group.get('id', ''),
                                     "repeat_cnt": last_block_group.get('repeat_cnt', 0),
                                     "block": new_blocks})
    res = update_many_to_mongodb(col='scenario',
                                     data={'block_group': new_last_block_group})
    if res.matched_count == 0:
        raise HTTPException(
            status_code=406, detail="No items have been updated.")
    return {'msg': 'Create new block', 'id': block_in.id}


@router.delete("", response_model=schemas.Msg)
def delete_blocks(
    block_in: schemas.BlockDelete,
) -> schemas.Msg:
    """
    Delete blocks.
    """
    for block_id in block_in.block_ids:
        delete_part_to_mongodb(col='scenario',
                               param={'block_group': {
                                   '$elemMatch': {'block.id': block_id}}},
                               data={'block_group.$.block': {'id': block_id}})
    delete_part_to_mongodb(col='scenario',
                           param={'block_group.block': {'$size': 0}},
                           data={'block_group': {'block': {'$size': 0}}})
    return {'msg': 'Delete blocks.'}


@router.put("/{block_id}", response_model=schemas.MsgWithId)
def update_block(
    *,
    block_id: str,
    block_in: schemas.BlockUpdate,
) -> schemas.MsgWithId:
    """
    Update a block.
    """
    block = load_from_mongodb(col='scenario',
                              param={"block_group": {
                                  "$elemMatch": {"block.id": block_id}}},
                              proj={"_id": 1})
    if not block:
        raise HTTPException(
            status_code=404, detail="The block with this id does not exist in the system.")

    update_data = {f"block_group.$.block.$[elem].{key}": value
                   for key, value in block_in.dict().items() if value is not None}

    col = get_mongodb_collection('scenario')
    res = col.update_one({"block_group.block.id": block_id},
                         {'$set': update_data},
                         array_filters=[{"elem.id": block_id}],
                         upsert=False)
    if res.matched_count == 0:
        raise HTTPException(
            status_code=406, detail="No items have been updated.")
    return {'msg': 'Update a block', 'id': block_id}


router_detail = APIRouter()


@router_detail.put("/{block_group_id}", response_model=schemas.MsgWithId)
def update_block_group(
    *,
    block_group_id: str,
    block_group_in: schemas.BlockGroupUpdate,
) -> schemas.MsgWithId:
    """
    Update a block_group.
    """
    param = {"block_group.id": block_group_id}
    block_group = load_from_mongodb(col='scenario',
                                    param=param,
                                    proj={"_id": 1})
    if not block_group:
        raise HTTPException(
            status_code=404, detail="The block_group with this id does not exist in the system.")

    update_data = {f"block_group.$.{key}": value
                   for key, value in block_group_in.dict().items() if value is not None}
    res = update_to_mongodb(col='scenario',
                            param=param,
                            data=update_data)
    if res.matched_count == 0:
        raise HTTPException(
            status_code=406, detail="No items have been updated.")
    return {'msg': 'Update a block_group', 'id': block_group_id}