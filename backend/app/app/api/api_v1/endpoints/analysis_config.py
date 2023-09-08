import json
import logging
import traceback
from typing import Optional

from app import schemas
from app.crud.base import aggregate_from_mongodb, update_to_mongodb
from app.db.redis_session import RedisClient
from app.schemas.enum import AnalysisTypeEnum
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.AnalysisConfigBase)
def read_analysis_config(
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
) -> schemas.AnalysisConfigBase:
    """
    Retrieve analysis_config.
    """
    try:
        analysis_config = {}
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        pipeline = [{"$match": {'id': scenario_id}},
                    {"$unwind": "$testruns"},
                    {"$project": {"testrun_id": "$testruns.id",
                                  "config": "$testruns.analysis.config"}},
                    {"$match": {"testrun_id": testrun_id}},
                    {"$project": {"_id": 0, "config": "$config"}}]
        res = aggregate_from_mongodb('scenario', pipeline)
        if res:
            analysis_config = res[0].get('config', {})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': analysis_config}


@router.put("/{scenario_id}/{testrun_id}", response_model=schemas.Msg)
def update_analysis_config(
    scenario_id: str,
    testrun_id: str,
    analysis_config_in: schemas.AnalysisConfig,
) -> schemas.Msg:
    """
    Update analysis_config.
    """
    pipeline = [{'$match': {'id': scenario_id}},
                {'$unwind': "$testruns"},
                {'$match': {"testruns.id": testrun_id}},
                {'$project': {'_id': 1}}]
    testrun = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not testrun:
        raise HTTPException(status_code=404,
                            detail="The testrun with this id does not exist in the system.")
    try:
        update_to_mongodb(col="scenario",
                          param={"id": scenario_id,
                                 "testruns.id": testrun_id},
                          data={"testruns.$.analysis.config": jsonable_encoder(analysis_config_in)})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update analysis_config'}


@router.delete("/{scenario_id}/{testrun_id}/{analysis_type}", response_model=schemas.Msg)
def delete_analysis_config(
    scenario_id: str,
    testrun_id: str,
    analysis_type: AnalysisTypeEnum,
) -> schemas.Msg:
    """
    Delete analysis_config.
    """
    pipeline = [{"$match": {'id': scenario_id}},
                {"$unwind": "$testruns"},
                {"$project": {"testrun_id": "$testruns.id",
                              "config": "$testruns.analysis.config"}},
                {"$match": {"testrun_id": testrun_id}},
                {"$project": {"_id": 0, "config": "$config"}}]
    testrun = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not testrun:
        raise HTTPException(status_code=404,
                            detail="The testrun with this id does not exist in the system.")
    try:
        analysis_type = analysis_type.value
        config = testrun[0].get('config', {})
        if analysis_type in config:
            del config[analysis_type]

        update_to_mongodb(col="scenario",
                          param={"id": scenario_id,
                                 "testruns.id": testrun_id},
                          data={"testruns.$.analysis.config": config})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Delete {analysis_type} analysis_config'}
