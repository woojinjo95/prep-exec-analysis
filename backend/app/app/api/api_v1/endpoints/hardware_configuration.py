import logging
import traceback

from app import schemas
from app.api.utility import parse_bytes_to_value, set_redis_pub_msg
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.HardwareConfigurationBase)
def read_hardware_configuration() -> schemas.HardwareConfigurationBase:
    """
    Retrieve hardware_configuration.
    """
    try:
        hardware_configuration = RedisClient.hgetall(f'hardware_configuration')
        config = {field: parse_bytes_to_value(value)
                  for field, value in hardware_configuration.items()}
        stb_conn = RedisClient.hgetall('stb_connection')
        config['stb_connection'] = {field: parse_bytes_to_value(value)
                                    for field, value in stb_conn.items()} if stb_conn else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': config}


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
        for key, val in conn_info.items():
            if val is not None:
                RedisClient.hset('stb_connection', key, str(val))
        RedisClient.publish('command', set_redis_pub_msg(msg="config",
                                                         data={"mode": conn_info.get('mode', None),
                                                               "host": conn_info.get('host', None),
                                                               "port": conn_info.get('port', None),
                                                               "username": conn_info.get('username', None),
                                                               "password": conn_info.get('password', None)}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Update {stb_connection_in.mode.value} stb_connection.'}


@router.delete("/stb_connection", response_model=schemas.Msg)
def delete_stb_connection() -> schemas.Msg:
    """
    Delete stb_connection.
    """
    stb_connection = RedisClient.hgetall('stb_connection')
    if not stb_connection:
        raise HTTPException(
            status_code=404, detail="The stb_connection does not exist in the system.")
    try:
        RedisClient.delete('stb_connection')
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Delete stb_connection.'}
