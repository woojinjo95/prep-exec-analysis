import logging

from app import schemas
from app.db.redis_session import RedisClient
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()


# @router.get("/timezone", response_model=schemas.Timezone)
def read_timezone() -> schemas.Timezone:
    """
    타임존 확인
    """
    return {'timezone': RedisClient.hget('common', 'timezone')}


@router.get("/service_state", response_model=schemas.ServiceState)
def read_service_state() -> schemas.ServiceState:
    """
    Retrieve service_state.
    """
    return {'items': {'state': RedisClient.hget('common', 'service_state')}}


@router.get("/log_connection_status", response_model=schemas.LogConnectionStatus)
def read_log_connection_status() -> schemas.LogConnectionStatus:
    """
    Retrieve log_connection_status.
    """
    return {'items': {'status': RedisClient.hget('log_connection_status', 'is_connected')}}
