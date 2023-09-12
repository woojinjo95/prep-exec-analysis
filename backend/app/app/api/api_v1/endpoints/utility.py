import logging
import re

from app import schemas
from app.db.redis_session import RedisClient
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()


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


@router.post("/validate_regex", response_model=schemas.RegexResult)
def validate_regex(
    *,
    regex_str: schemas.Regex,
) -> schemas.RegexResult:
    """
    Validate regular expression
    """
    try:
        regex_str = regex_str.regex
        regex = re.compile(regex_str)
        if regex.groups > 0:
            if regex.groups != len(regex.groupindex):
                return {"is_valid": False,
                        "msg": f"{regex}",
                        "detail": f"there is no named group: number of groups: {regex.groups}, name_goups: {regex.groupindex.keys()}"}
        return {"is_valid": True, "msg": f"{regex}", "keys": list(regex.groupindex.keys())}
    except Exception as e:
        return {"is_valid": False, "msg": f"{e}"}
