import logging

from app import schemas
from app.crud.base import load_from_mongodb, update_many_to_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.put("", response_model=schemas.Msg)
def update_analysis_config(
    *,
    analysis_config_in: schemas.AnalysisConfigUpdate,
) -> schemas.Msg:
    """
    Update a analysis_config.
    """
    return {'msg': 'Update a analysis_config'}


@router.get("", response_model=schemas.AnalysisConfigBase)
def read_analysis_config() -> schemas.AnalysisConfigBase:
    """
    Retrieve analysis_config.
    """
    res = load_from_mongodb(col='analysis_config')
    return {'items': res[0] if res else {}}
