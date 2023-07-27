import logging
import uuid
from typing import List

from app import schemas
from app.crud.base import (delete_by_id_to_mongodb, insert_to_mongodb,
                           load_by_id_from_mongodb, load_from_mongodb,
                           update_by_id_to_mongodb, update_by_multi_filter_in_mongodb)
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("")
def create_basic_remocon(
    remocon_in: schemas.Remocon
):
    """
    신규 리모컨 등록 (임시).
    """
    # remocon_in.id = str(uuid.uuid4())
    res = insert_to_mongodb(collection='remocon', data=remocon_in)
    # return {'msg': 'Create new item', 'id': remocon_in.id}


@router.get("", response_model=List[schemas.Remocon])
def read_remocon() -> List[schemas.Remocon]:
    """
    리모컨 조회
    """
    return load_from_mongodb(collection='remocon', param={})


@router.put("/custom_key/{remocon_id}/{custom_key_id}")
def update_custom_key(
    remocon_id: str,
    custom_key_id: str,
    custom_key_in: schemas.RemoconCustomKeyUpdate,
):
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
    return update_result.upserted_id
