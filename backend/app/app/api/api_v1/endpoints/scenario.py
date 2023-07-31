import logging
import uuid

from app import schemas
from app.crud.base import (get_mongodb_collection, insert_one_to_mongodb,
                           load_from_mongodb)
from fastapi import APIRouter
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
        insert_one_to_mongodb(col='scenario', data={"block_group": [{
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
