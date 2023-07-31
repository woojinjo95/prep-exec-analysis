import logging
import uuid

from app import schemas
from app.api.utility import get_multi_or_paginate_by_res
from app.crud.base import (delete_by_id_to_mongodb, insert_one_to_mongodb,
                           load_by_id_from_mongodb, update_by_id_to_mongodb)
from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{item_id}", response_model=schemas.Item)
def read_item_by_id(
    item_id: str,
) -> schemas.Item:
    """
    Get a specific item by id.
    """
    item = load_by_id_from_mongodb(col='item', id=item_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="The item with this id does not exist in the system.")
    return item


@router.put("/{item_id}", response_model=schemas.MsgWithId)
def update_item(
    *,
    item_id: str,
    item_in: schemas.ItemUpdate,
) -> schemas.MsgWithId:
    """
    Update a item.
    """
    item = load_by_id_from_mongodb(col='item', id=item_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="The item with this id does not exist in the system.")
    update_by_id_to_mongodb(col='item', id=item_id, data=item_in)
    return {'msg': 'Update a item', 'id': item_id}


@router.delete("/{item_id}", response_model=schemas.Msg)
def delete_item(
    item_id: str,
) -> schemas.Msg:
    """
    Delete a item.
    """
    item = load_by_id_from_mongodb(col='item', id=item_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="The item with this id does not exist in the system.")
    delete_by_id_to_mongodb(col='item', id=item_id)
    return {'msg': 'Delete a item.'}


@router.get("", response_model=schemas.ItemPage)
def read_items(page: int = Query(None, ge=1, description="Page number"),
               page_size: int = Query(None, ge=1, le=100, description="Page size")) -> schemas.ItemPage:
    """
    Retrieve items.
    """
    return get_multi_or_paginate_by_res(col='item', page=page, page_size=page_size)


@router.post("", response_model=schemas.MsgWithId)
def create_item(
    *,
    item_in: schemas.ItemBase,
) -> schemas.MsgWithId:
    """
    Create new item.
    """
    item_in = schemas.ItemCreate(name=item_in.name, id=str(uuid.uuid4()))
    insert_one_to_mongodb(col='item', data=item_in)
    return {'msg': 'Create new item', 'id': item_in.id}
