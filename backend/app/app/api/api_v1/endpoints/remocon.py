import json
import logging
import traceback
import uuid

from app import schemas
from app.api.utility import parse_bytes_to_value
from app.db.redis_session import RedisClient
from app.schemas.enum import RemoconEnum
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.RemoconRead)
def read_remocon() -> schemas.RemoconRead:
    """
    리모컨 조회
    """
    try:
        remocon_list = [{k: parse_bytes_to_value(v) for k, v in RedisClient.hgetall(key).items()}
                        for key in RedisClient.scan_iter(match='remocon:*')]
        remocon_list.sort(key=lambda remocon: remocon['sort_index'])
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': remocon_list}


@router.put("/{remocon_name}", response_model=schemas.Msg)
def update_remocon(
    remocon_name: RemoconEnum,
    remocon_in: schemas.RemoconUpdate,
) -> schemas.Msg:
    """
    리모컨 정보 덮어쓰기
    """
    try:
        remocon_name = remocon_name.value
        for key, val in jsonable_encoder(remocon_in).items():
            if val is not None:
                RedisClient.hset(f'remocon:{remocon_name}', key, json.dumps(val))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Update {remocon_name} remocon'}


@router.post("/custom_key", response_model=schemas.MsgWithId)
def insert_custom_key(
    custom_key_in_base: schemas.RemoconCustomKeyCreateBase,
) -> schemas.MsgWithId:
    """
    리모컨 커스텀 키 추가
    """
    try:
        custom_key_in = schemas.RemoconCustomKeyCreate(
            id=str(uuid.uuid4()),
            name=custom_key_in_base.name,
            custom_code=custom_key_in_base.custom_code,
        )
        input_data = {
            'custom_keys': custom_key_in.dict()
        }
        custom_keys = parse_bytes_to_value(RedisClient.hget('remocon:'+custom_key_in_base.remocon_name.value, 'custom_keys'))
        custom_keys.append(input_data['custom_keys'])
        RedisClient.hset('remocon:'+custom_key_in_base.remocon_name.value, 'custom_keys', str(custom_keys))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new custom_key', 'id': custom_key_in.id}


@router.delete("/custom_key/{remocon_name}", response_model=schemas.Msg)
def delete_custom_keys(
    remocon_name: RemoconEnum,
    custom_key_in: schemas.RemoconCustomKeyUpdateMulti
) -> schemas.Msg:
    remocon_name = remocon_name.value
    name = f'remocon:{remocon_name}'
    remocon = RedisClient.hgetall(name=name)
    if not remocon:
        raise HTTPException(
            status_code=404, detail=f"The remocon with this {remocon_name} does not exist in the system.")
    try:
        custom_keys = parse_bytes_to_value(remocon.get('custom_keys', []))
        updated_custom_keys = [item for item
                            in custom_keys if item["id"] not in custom_key_in.custom_key_ids]
        RedisClient.hset(name, 'custom_keys', json.dumps(updated_custom_keys))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'custom_key Deletion Completed'}


@router.put("/custom_key/{remocon_name}/{custom_key_id}", response_model=schemas.MsgWithId)
def update_custom_key(
    remocon_name: RemoconEnum,
    custom_key_id: str,
    custom_key_in: schemas.RemoconCustomKeyUpdate,
) -> schemas.MsgWithId:
    remocon_name = remocon_name.value
    name = f'remocon:{remocon_name}'
    remocon = RedisClient.hgetall(name=name)
    if not remocon:
        raise HTTPException(
            status_code=404, detail=f"The remocon with this {remocon_name} does not exist in the system.")
    try:
        custom_keys = parse_bytes_to_value(remocon.get('custom_keys', []))
        updated_custom_keys = [{key: val for key, val in jsonable_encoder(custom_key_in).items()}
                            if item["id"] == custom_key_id else item
                            for item in custom_keys]
        RedisClient.hset(name, 'custom_keys', json.dumps(updated_custom_keys))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update custom_key', 'id': custom_key_id}
