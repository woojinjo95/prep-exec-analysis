import logging
import traceback

from app import schemas
from app.api.utility import get_config_from_scenario_mongodb, set_redis_pub_msg
from app.crud.base import delete_part_to_mongodb
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
        analysis_in = jsonable_encoder(analysis_in)
        new_measurements = set(analysis_in['measurement'])
        testrun_config = get_config_from_scenario_mongodb(
            analysis_in['scenario_id'], analysis_in['testrun_id']).get('config', {})
        old_measurements = set([key for key, value in testrun_config.items() if value is not None])

        for _type in list(old_measurements - new_measurements):
            delete_part_to_mongodb(col="scenario",
                                   param={"id": analysis_in['scenario_id'],
                                          "testruns.id": analysis_in['testrun_id']},
                                   data={"testruns.$.measure_targets": {'type': _type}})

        RedisClient.publish('command', set_redis_pub_msg(msg="start_analysis"))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Start analysis: {analysis_in["measurement"]}'}
