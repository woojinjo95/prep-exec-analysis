import logging
import uuid

from app import schemas
from app.crud.base import (delete_part_by_id_to_mongodb,
                           insert_by_id_to_mongodb_array,
                           load_by_id_from_mongodb, load_from_mongodb,
                           update_to_mongodb)
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.RemoconRead)
def read_remocon() -> schemas.RemoconRead:
    """
    리모컨 조회
    """
    return {'items': load_from_mongodb(col='remocon', sort_item="custom_keys.order")}


@router.post("/custom_key", response_model=schemas.MsgWithId)
def insert_custom_key(
    custom_key_in_base: schemas.RemoconCustomKeyCreateBase,
) -> schemas.MsgWithId:
    custom_key_in = schemas.RemoconCustomKeyCreate(
        id=str(uuid.uuid4()),
        order=0,
        name=custom_key_in_base.name,
        custom_code=custom_key_in_base.custom_code,
    )
    input_data = {
        'custom_keys': custom_key_in.dict()
    }
    insert_by_id_to_mongodb_array(col='remocon',
                                  id=custom_key_in_base.remocon_id,
                                  data=input_data)
    return {'msg': 'Create new custom_key', 'id': custom_key_in.id}


@router.put("/custom_key/{remocon_id}/{custom_key_id}", response_model=schemas.MsgWithId)
def update_custom_key(
    remocon_id: str,
    custom_key_id: str,
    custom_key_in: schemas.RemoconCustomKeyUpdate,
) -> schemas.MsgWithId:
    remocon = load_by_id_from_mongodb(col='remocon', id=remocon_id)
    if remocon is None:
        raise HTTPException(status_code=404, detail="Remocon not found")

    id_filter = {
        "id": remocon_id,
        "custom_keys.id": custom_key_id
    }

    update_data = {"custom_keys.$." + key: value for key,
                   value in custom_key_in.dict().items() if value is not None}

    update_to_mongodb(col='remocon',
                      param=id_filter,
                      data=update_data)
    return {'msg': 'Update custom_key', 'id': custom_key_id}


# @router.put("/custom_keys_order/{remocon_id}", response_model=schemas.MsgWithId)
def update_custom_keys_order(
    remocon_id: str,
    custom_key_in: schemas.RemoconCustomKeyUpdateMulti,
) -> schemas.MsgWithId:
    id_filter = {"id": remocon_id}
    for idx, custom_key_id in enumerate(custom_key_in.custom_key_ids, start=1):
        id_filter['custom_keys.id'] = custom_key_id
        update_to_mongodb(col='remocon',
                          param=id_filter,
                          data={"custom_keys.$.order": idx})
    return {'msg': 'Update custom_key order', 'id': remocon_id}


@router.delete("/custom_key/{remocon_id}", response_model=schemas.Msg)
def delete_custom_keys(
    remocon_id: str,
    custom_key_ids: schemas.RemoconCustomKeyUpdateMulti
) -> schemas.Msg:
    remocon = load_by_id_from_mongodb(col='remocon', id=remocon_id)
    if remocon is None:
        raise HTTPException(status_code=404, detail="Remocon not found")
    for custom_key_id in custom_key_ids.custom_key_ids:
        delete_part_by_id_to_mongodb(col='remocon',
                                     id=remocon_id,
                                     data={"custom_keys": {'id': custom_key_id}})
        logger.info(
            f"[Delete]remocon_id/custom_key : {remocon_id}/{custom_key_id}")
    return {'msg': 'custom_key Deletion Completed'}
