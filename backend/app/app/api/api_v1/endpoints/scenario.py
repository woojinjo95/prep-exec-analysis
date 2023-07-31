import logging
import uuid

from app import schemas
from app.crud.base import (get_mongodb_collection, insert_to_mongodb,
                           load_from_mongodb)
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


@router.post("/block", response_model=schemas.MsgWithId)
def create_block(
    *,
    block_in: schemas.BlockCreate,
) -> schemas.MsgWithId:
    """
    Create new block.
    """
    block_id = str(uuid.uuid4())
    block_in = schemas.Block(id=block_id,
                             type=block_in.type,
                             value=block_in.value,
                             delay_time=block_in.delay_time)
    col = get_mongodb_collection('scenario')
    obj = col.find_one()
    if obj is None:
        insert_to_mongodb(col='scenario', data={"block_group": [{
            "id": str(uuid.uuid4()),
            "repeat_cnt": 1,
            "block": [jsonable_encoder(block_in)]
        }]})
    else:
        block_group = obj.get('block_group', [{}])[0]
        blocks = block_group.get('block', [])
        blocks.append(jsonable_encoder(block_in))
        new_block_group = {
            "block_group": [{
                "id": block_group.get('id', ''),
                "repeat_cnt": block_group.get('repeat_cnt', 0),
                "block": blocks
            }]
        }
        col = get_mongodb_collection('scenario')
        col.update_many({}, {'$set': new_block_group})
    return {'msg': 'Create new block', 'id': block_id}


@router.put("/block/{block_group_id}/{block_id}", response_model=schemas.MsgWithId)
def update_block(
    *,
    block_group_id: str,
    block_id: str,
    block_in: schemas.BlockUpdate,
) -> schemas.MsgWithId:
    """
    Update a block.
    """
    block = load_from_mongodb(col='scenario',
                              param={
                                  "block_group": {
                                      "$elemMatch": {
                                          "id": block_group_id,
                                          "block.id": block_id
                                      }
                                  }
                              },
                              proj={"_id": 1})
    if not block:
        raise HTTPException(
            status_code=404, detail="The block with this id does not exist in the system.")

    update_data = {f"block_group.$.block.$[elem].{key}": value
                   for key, value in block_in.dict().items() if value is not None}

    col = get_mongodb_collection('scenario')
    col.update_one({"block_group.id": block_group_id, "block_group.block.id": block_id},
                   {'$set': update_data},
                   array_filters=[{"elem.id": block_id}],
                   upsert=False)

    return {'msg': 'Update a block', 'id': block_id}
