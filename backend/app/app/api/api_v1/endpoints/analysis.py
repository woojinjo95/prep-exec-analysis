import json
import logging
import traceback
from typing import Optional

from app import schemas
from app.api.utility import parse_bytes_to_value, set_redis_pub_msg
from app.crud.base import aggregate_from_mongodb, update_to_mongodb
from app.db.redis_session import RedisClient
from app.schemas.enum import AnalysisTypeEnum
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=schemas.Msg)
def start_analysis(
    *,
    analysis_in: schemas.Analysis,
) -> schemas.Msg:
    try:
        collection_dict = {
            "freeze": "an_freeze",
            "resume": "an_warm_boot",
            "boot": "an_cold_boot",
            "log_pattern_matching": "an_log_pattern"
        }

        # 초기화
        for measurement in analysis_in.measurement:
            collection = collection_dict.get(measurement, None)
            if collection:
                pass

        RedisClient.publish('command', set_redis_pub_msg(msg="analysis",
                                                         data={"measurement": analysis_in.measurement}))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Start analysis: {analysis_in.measurement}'}
