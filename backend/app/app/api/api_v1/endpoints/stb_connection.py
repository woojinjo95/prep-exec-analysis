import logging
import uuid

from app import schemas
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.StbConnectionBase)
def read_stb_connection() -> schemas.StbConnectionBase:
    """
    Retrieve stb_connection.
    """
    stb_conn_list = []
    matching_keys = RedisClient.scan_iter(match="stb_connection:*")
    for key in matching_keys:
        res = RedisClient.hgetall(key)
        stb_conn_list.append({
            'id': key.split(':')[1],
            'connection_type': res.get('connection_type', 'ssh'),
            'ip': res.get('ip', ''),
            'port': res.get('port', ''),
            'username': res.get('username', None),
            'password': res.get('password', None),
        })
    return {'items': sorted(stb_conn_list, key=lambda x: x['ip'])}


@router.post("", response_model=schemas.MsgWithId)
def create_stb_connection(
    *,
    stb_connection_in: schemas.StbConnectionCreate,
) -> schemas.MsgWithId:
    """
    Create new stb_connection.
    """
    id = str(uuid.uuid4())
    for key, val in jsonable_encoder(stb_connection_in).items():
        if val is not None:
            RedisClient.hset(f'stb_connection:{id}', key, val)
    return {'msg': 'Create new stb_connection', 'id': id}


@router.delete("/{id}", response_model=schemas.Msg)
def delete_stb_connection(
    id: str,
) -> schemas.Msg:
    """
    Delete a stb_connection.
    """
    stb_connection = RedisClient.hget(name=f'stb_connection:{id}', key='ip')
    if not stb_connection:
        raise HTTPException(
            status_code=404, detail="The stb_connection with this id does not exist in the system.")
    RedisClient.delete(f'stb_connection:{id}')
    return {'msg': 'Delete a stb_connection.'}
