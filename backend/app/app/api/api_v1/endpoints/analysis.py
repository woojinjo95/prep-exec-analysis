import logging
import traceback

from app import schemas
from app.api.utility import set_redis_pub_msg
from app.crud.base import delete_many_to_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=schemas.Msg)
async def start_analysis(
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
        analysis_in = jsonable_encoder(analysis_in)
        measurements = analysis_in['measurement']
        for measurement in measurements:
            collection = collection_dict.get(measurement, None)
            if collection:
                delete_many_to_mongodb(collection, {'scenario_id': analysis_in['scenario_id'],
                                                    'testrun_id': analysis_in['testrun_id']})

        RedisClient.publish('command', set_redis_pub_msg(msg="analysis",
                                                         data={"measurement": measurements}))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Start analysis: {measurements}'}
