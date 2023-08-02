import logging
import uuid

from app import schemas
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


def converted_data(data_str):
    try:
        res = float(data_str)
        if res.is_integer():
            return int(res)
        return res
    except ValueError:
        try:
            res = str(data_str)
            return res
        except ValueError:
            try:
                res = bool(data_str)
                return res
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
def read_hardware_configuration() -> schemas.HardwareConfigurationBase:
    """
    Retrieve hardware_configuration.
    """
    hardware_configuration = RedisClient.hgetall(f'hardware_configuration')
    config = {field: converted_data(value)
              for field, value in hardware_configuration.items()}
    adb = RedisClient.hgetall(name='stb_connection:adb')
    ssh = RedisClient.hgetall(name='stb_connection:ssh')
    config['adb_connection'] = adb if adb else None
    config['ssh_connection'] = ssh if ssh else None

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
        })
    config['ip_limit'] = sorted(ip_limit_list, key=lambda x: x['ip'])
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
                                key='ip')
    if not ip_limit:
        raise HTTPException(
            status_code=404, detail="The hardware_configuration ip_limit with this id does not exist in the system.")
    RedisClient.delete(f'hardware_configuration_ip_limit:{id}')
    return {'msg': 'Delete a hardware_configuration ip_limit.'}


@router.post("/stb_connection", response_model=schemas.Msg)
def create_stb_connection(
    *,
    stb_connection_in: schemas.StbConnectionCreate,
) -> schemas.Msg:
    """
    Create new stb_connection.
    """
    connection_type = stb_connection_in.connection_type
    for key, val in jsonable_encoder(stb_connection_in).items():
        if val is not None and key != 'connection_type':
            RedisClient.hset(f'stb_connection:{connection_type}', key, val)
    return {'msg': f'Create new {connection_type} stb_connection'}


@router.delete("/stb_connection/{connection_type}", response_model=schemas.Msg)
def delete_stb_connection(
    connection_type: str,
) -> schemas.Msg:
    """
    Delete a stb_connection.
    """
    stb_connection = RedisClient.hgetall(
        name=f'stb_connection:{connection_type}')
    if not stb_connection:
        raise HTTPException(
            status_code=404, detail="The stb_connection with this connection_type does not exist in the system.")
    RedisClient.delete(f'stb_connection:{connection_type}')
    return {'msg': f'Delete {connection_type} stb_connection.'}
