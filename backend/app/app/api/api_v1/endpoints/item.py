import logging
from typing import List

from app import schemas
from app.crud.base import (delete_by_id_to_mongodb, insert_to_mongodb,
                           load_by_id_from_mongodb, load_from_mongodb,
                           update_by_id_to_mongodb)
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{item_id}", response_model=schemas.Item)
def read_item_by_id(
    item_id: str,
) -> schemas.Item:
    """
    Get a specific item by id.
    """
    item = load_by_id_from_mongodb(collection='item', id=item_id)
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
    item = load_by_id_from_mongodb(collection='item', id=item_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="The item with this id does not exist in the system.")
    update_by_id_to_mongodb(collection='item', id=item_id, data=item_in)
    return {'msg': 'Update a item', 'id': item_id}


@router.delete("/{item_id}", response_model=schemas.Msg)
def delete_item(
    item_id: str,
) -> schemas.Msg:
    """
    Delete a item.
    """
    item = load_by_id_from_mongodb(collection='item', id=item_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="The item with this id does not exist in the system.")
    delete_by_id_to_mongodb(collection='item', id=item_id)
    return {'msg': 'Delete a item.'}


@router.get("", response_model=List[schemas.Item])
def read_items() -> List[schemas.Item]:
    """
    Retrieve items.
    """
    res = load_from_mongodb(collection='item', param={})
    return res


@router.post("", response_model=schemas.MsgWithId)
def create_item(
    *,
    item_in: schemas.ItemCreate,
) -> schemas.MsgWithId:
    """
    Create new item.
    """
    id = insert_to_mongodb(collection='item', data=item_in)
    return {'msg': 'Create new item', 'id': id}
