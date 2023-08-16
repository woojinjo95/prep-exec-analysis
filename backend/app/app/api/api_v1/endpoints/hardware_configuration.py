import json
import logging
import traceback
import uuid

from app import schemas
from app.api.utility import parse_bytes_to_value
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


# @router.put("", response_model=schemas.Msg)
def update_hardware_configuration(
    *,
    hardware_configuration_in: schemas.HardwareConfigurationUpdate,
) -> schemas.Msg:
    """
    Update a hardware_configuration.
    """
    for key, val in jsonable_encoder(hardware_configuration_in).items():
        if val is not None:
            RedisClient.hset('hardware_configuration', key, str(val))
    return {'msg': 'Update a hardware_configuration'}


@router.get("", response_model=schemas.HardwareConfigurationBase)
def read_hardware_configuration() -> schemas.HardwareConfigurationBase:
    """
    Retrieve hardware_configuration.
    """
    try:
        hardware_configuration = RedisClient.hgetall(f'hardware_configuration')
        config = {field: parse_bytes_to_value(value)
                  for field, value in hardware_configuration.items()}
        stb_conn = RedisClient.hget(f'hardware_configuration',
                                    'stb_connection')
        config['stb_connection'] = json.loads(stb_conn) if stb_conn else None

        ip_limit_list = []
        matching_keys = RedisClient.scan_iter(
            match="hardware_configuration_ip_limit:*")
        for key in matching_keys:
            res = RedisClient.hgetall(key)
            ip_limit_list.append({
                'id': key.split(':')[1],
                'ip': res.get('ip', ''),
                'port': res.get('port', ''),
                'protocol': res.get('protocol', ''),
            })
        config['ip_limit'] = sorted(ip_limit_list, key=lambda x: x['ip']) if ip_limit_list else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': config}


# @router.post("/ip_limit", response_model=schemas.MsgWithId)
def create_hardware_configuration_ip_limit(
    *,
    ip_limit_in: schemas.HardwareConfigurationIpLimitCreate,
) -> schemas.MsgWithId:
    """
    Create new hardware_configuration ip_limit.
    """
    id = str(uuid.uuid4())
    for key, val in jsonable_encoder(ip_limit_in).items():
        RedisClient.hset(f'hardware_configuration_ip_limit:{id}', key, val)
    return {'msg': 'Create new hardware_configuration ip_limit', 'id': id}


# @router.put("/ip_limit/{id}", response_model=schemas.MsgWithId)
def update_hardware_configuration_ip_limit(
    *,
    id: str,
    ip_limit_in: schemas.HardwareConfigurationIpLimitCreate,
) -> schemas.MsgWithId:
    """
    Update a hardware_configuration ip_limit.
    """
    name = f'hardware_configuration_ip_limit:{id}'
    ip_limit = RedisClient.hgetall(name=name)
    if not ip_limit:
        raise HTTPException(
            status_code=404, detail="The hardware_configuration ip_limit with this id does not exist in the system.")

    for key, val in jsonable_encoder(ip_limit_in).items():
        RedisClient.hset(name, key, val)
    return {'msg': 'Update a hardware_configuration ip_limit.', 'id': id}


# @router.delete("/ip_limit/{id}", response_model=schemas.Msg)
def delete_hardware_configuration_ip_limit(
    id: str,
) -> schemas.Msg:
    """
    Delete a hardware_configuration ip_limit.
    """
    name = f'hardware_configuration_ip_limit:{id}'
    ip_limit = RedisClient.hgetall(name=name)
    if not ip_limit:
        raise HTTPException(
            status_code=404, detail="The hardware_configuration ip_limit with this id does not exist in the system.")

    RedisClient.delete(name)
    return {'msg': 'Delete a hardware_configuration ip_limit.'}


# @router.post("/stb_connection", response_model=schemas.Msg)
def create_stb_connection(
    *,
    stb_connection_in: schemas.StbConnection,
) -> schemas.Msg:
    """
    Create new stb_connection.
    """
    RedisClient.hset('hardware_configuration',
                     'stb_connection', json.dumps({k: v for k, v
                                                   in jsonable_encoder(stb_connection_in).items()
                                                   if v is not None}))
    return {'msg': f'Create new {stb_connection_in.type} stb_connection'}


@router.put("/stb_connection", response_model=schemas.Msg)
def update_stb_connection(
    *,
    stb_connection_in: schemas.StbConnection,
) -> schemas.Msg:
    """
    Update stb_connection.
    """
    try:
        conn_info = jsonable_encoder(stb_connection_in)
        RedisClient.hset('hardware_configuration',
                         'stb_connection', json.dumps({k: v for k, v
                                                      in conn_info.items()
                                                      if v is not None}))
        RedisClient.publish('command', json.dumps({
            "msg": "config",
            "data": {
                "mode": conn_info.get('type', None),
                "host": conn_info.get('ip', None),
                "port": conn_info.get('port', None),
                "username": conn_info.get('username', None),
                "password": conn_info.get('password', None),
            }
        }))
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Update {stb_connection_in.type.value} stb_connection.'}


@router.delete("/stb_connection", response_model=schemas.Msg)
def delete_stb_connection() -> schemas.Msg:
    """
    Delete stb_connection.
    """
    stb_connection = RedisClient.hget('hardware_configuration',
                                      'stb_connection')
    if not stb_connection:
        raise HTTPException(
            status_code=404, detail="The hardware_configuration with this stb_connection does not exist in the system.")

    RedisClient.hdel('hardware_configuration', 'stb_connection')
    return {'msg': 'Delete stb_connection.'}
