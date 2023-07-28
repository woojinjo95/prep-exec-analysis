import logging
import uuid
from datetime import datetime

from app import schemas
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


def converted_data(data_str):
    try:
        converted_data = float(data_str)
        if converted_data.is_integer():
            return int(converted_data)
        return converted_data
    except ValueError:
        try:
            converted_data = str(data_str)
            return converted_data
        except ValueError:
            try:
                converted_data = bool(data_str)
                return converted_data
            except ValueError:
                return data_str


@router.put("", response_model=schemas.Msg)
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
def read_hardware_configuration():
    """
    Retrieve hardware_configuration.
    """
    hardware_configuration = RedisClient.hgetall(f'hardware_configuration')
    config = {field: converted_data(value)
              for field, value in hardware_configuration.items()}

    ip_limit_list = []
    matching_keys = RedisClient.scan_iter(
        match="hardware_configuration_ip_limit:*")
    for key in matching_keys:
        res = RedisClient.hgetall(key)
        ip_limit_list.append({
            'id': key.split(':')[1],
            'ip': res.get('ip', ''),
            'port': res.get('port', ''),
            'type': res.get('type', ''),
            'created_at': res.get('created_at', ''),
        })
    config['ip_limit'] = ip_limit_list
    return {'items': config}


@router.post("/ip_limit", response_model=schemas.MsgWithId)
def create_hardware_configuration_ip_limit(
    *,
    ip_limit_in: schemas.HardwareConfigurationIpLimitCreate,
) -> schemas.MsgWithId:
    """
    Create new hardware_configuration ip_limit.
    """
    id = str(uuid.uuid4())
    RedisClient.hset(f'hardware_configuration_ip_limit:{id}',
                     'created_at',
                     datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    for key, val in jsonable_encoder(ip_limit_in).items():
        RedisClient.hset(f'hardware_configuration_ip_limit:{id}', key, val)

    return {'msg': 'Create new hardware_configuration ip_limit', 'id': id}


@router.delete("/ip_limit/{id}", response_model=schemas.Msg)
def delete_hardware_configuration_ip_limit(
    id: str,
) -> schemas.Msg:
    """
    Delete a hardware_configuration ip_limit.
    """
    ip_limit = RedisClient.hget(name=f'hardware_configuration_ip_limit:{id}',
                                key='created_at')
    if not ip_limit:
        raise HTTPException(
            status_code=404, detail="The hardware_configuration ip_limit with this id does not exist in the system.")
    RedisClient.delete(f'hardware_configuration_ip_limit:{id}')
    return {'msg': 'Delete a hardware_configuration ip_limit.'}
