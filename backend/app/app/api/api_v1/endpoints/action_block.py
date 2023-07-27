import logging
import uuid
from typing import List

from app import schemas
from app.crud.base import (delete_by_id_to_mongodb, insert_to_mongodb,
                           load_by_id_from_mongodb, load_from_mongodb,
                           update_by_id_to_mongodb)
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.put("/{action_block_id}", response_model=schemas.MsgWithId)
def update_action_block(
    *,
    action_block_id: str,
    action_block_in: schemas.ActionBlockUpdate,
) -> schemas.MsgWithId:
    """
    Update a action_block.
    """
    action_block = load_by_id_from_mongodb(
        col='action_block', id=action_block_id)
    if not action_block:
        raise HTTPException(
            status_code=404, detail="The action_block with this id does not exist in the system.")
    update_by_id_to_mongodb(col='action_block',
                            id=action_block_id, data=action_block_in)
    return {'msg': 'Update a action_block', 'id': action_block_id}


@router.delete("/{action_block_id}", response_model=schemas.Msg)
def delete_action_block(
    action_block_id: str,
) -> schemas.Msg:
    """
    Delete a action_block.
    """
    action_block = load_by_id_from_mongodb(
        col='action_block', id=action_block_id)
    if not action_block:
        raise HTTPException(
            status_code=404, detail="The action_block with this id does not exist in the system.")
    delete_by_id_to_mongodb(col='action_block', id=action_block_id)
    return {'msg': 'Delete a action_block'}


@router.get("", response_model=List[schemas.ActionBlock])
def read_action_blocks() -> List[schemas.ActionBlock]:
    """
    Retrieve action_blocks.
    """
    return load_from_mongodb(col='action_block')


@router.post("", response_model=schemas.MsgWithId)
def create_action_block(
    *,
    action_block_in: schemas.ActionBlockCreateBase,
) -> schemas.MsgWithId:
    """
    Create new action_block.
    """
    action_block_in = schemas.ActionBlockCreate(
        type=action_block_in.type,
        value=action_block_in.value,
        delay_time=action_block_in.delay_time,
        sort_idx=0,  # TODO 그룹에 대한 블럭 총 갯수+1
        group_id=0,  # TODO 없을 경우 디폴트 값 지정
        id=str(uuid.uuid4()))
    insert_to_mongodb(col='action_block', data=action_block_in)
    return {'msg': 'Create new action_block', 'id': action_block_in.id}
