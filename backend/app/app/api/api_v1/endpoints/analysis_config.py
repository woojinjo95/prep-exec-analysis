import json
import logging
import traceback

from app import schemas
from app.api.utility import parse_bytes_to_value
from app.db.redis_session import RedisClient
from app.schemas.enum import AnalysisTypeEnum
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.AnalysisConfigBase)
def read_analysis_config() -> schemas.AnalysisConfigBase:
    """
    Retrieve analysis_config.
    """
    try:
        analysis_config = {}
        for key in RedisClient.scan_iter(match="analysis_config:*"):
            analysis_config[key.split(':')[1]] = {k: parse_bytes_to_value(v)
                                                  for k, v in RedisClient.hgetall(key).items()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': analysis_config}


@router.put("", response_model=schemas.Msg)
def update_analysis_config(
    *,
    analysis_config_in: schemas.AnalysisConfig,
) -> schemas.Msg:
    """
    Update analysis_config.
    """
    try:
        for key, val in jsonable_encoder(analysis_config_in).items():
            if val is not None and key in AnalysisTypeEnum.list():
                for k, v in val.items():
                    RedisClient.hset(f'analysis_config:{key}', k, json.dumps(v))
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update analysis_config'}
