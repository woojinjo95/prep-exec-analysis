import logging
import uuid
from typing import List

from app import schemas
from app.crud.base import (delete_by_id_to_mongodb, insert_to_mongodb,
                           load_by_id_from_mongodb, load_from_mongodb,
                           update_by_id_to_mongodb, update_by_multi_filter_in_mongodb,
                           insert_by_id_to_mongodb, get_mongodb_collection)
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=List[schemas.Remocon])
def read_remocon() -> List[schemas.Remocon]:
    """
    리모컨 조회
    """
    return load_from_mongodb(collection='remocon', param={}, sort_item="custom_keys.order")


@router.post("/custom_key/{remocon_id}", response_model=schemas.MsgWithId)
def insert_custom_key(
    remocon_id: str,
    custom_key_in: schemas.RemoconCustomKeyCreate,
) -> schemas.MsgWithId:
    custom_key_in.id = str(uuid.uuid4())
    custom_key_in.order = len(load_by_id_from_mongodb(collection='remocon', id=remocon_id).get('custom_keys', [])) + 1
    input_data = {
        'custom_keys': custom_key_in.dict()
    }
    insert_by_id_to_mongodb(collection='remocon', id=remocon_id, data=input_data)
    return {'msg': 'Create new custom_key', 'id': remocon_id}
    # TODO: response_model 필요


@router.put("/custom_key/{remocon_id}/{custom_key_id}", response_model=schemas.MsgWithId)
def update_custom_key(
    remocon_id: str,
    custom_key_id: str,
    custom_key_in: schemas.RemoconCustomKeyUpdate,
) -> schemas.MsgWithId:
    remocon = load_by_id_from_mongodb(collection='remocon', id=remocon_id)
    if remocon is None:
        raise HTTPException(status_code=404, detail="Remocon not found")

    id_filter = {
        "id": remocon_id,
        "custom_keys.id": custom_key_id
    }
    update_data = {}
    for key, value in custom_key_in.dict().items():
        if value is not None:
            update_data["custom_keys.$." + key] = value
    
    update_result = update_by_multi_filter_in_mongodb(collection='remocon', param=id_filter, data=update_data)
    return {'msg': 'Update custom_key', 'id': remocon_id}
    # TODO: response_model 필요


@router.put("/custom_keys_order", response_model=schemas.MsgWithId)
def update_custom_key(
    remocon_id: str,
    custom_key_ids: List[str]
) -> schemas.MsgWithId:
    id_filter = {"id": remocon_id}
    for idx, custom_key_id in enumerate(custom_key_ids, start=1):
        id_filter['custom_keys.id'] = custom_key_id
        update_by_multi_filter_in_mongodb(collection='remocon', param=id_filter, data={"custom_keys.$.order": idx})
    return {'msg': 'Update custom_key order', 'id': remocon_id}
