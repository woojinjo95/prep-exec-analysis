import logging
import os
import time
import traceback
from datetime import datetime
from typing import Optional

from app import schemas
from app.api.utility import get_utc_datetime, set_redis_pub_msg
from app.crud.base import (aggregate_from_mongodb, load_by_id_from_mongodb,
                           update_by_id_to_mongodb, update_to_mongodb)
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{scenario_id}", response_model=schemas.MsgWithId)
def create_testrun(
    *,
    scenario_id: str,
) -> schemas.MsgWithId:
    """
    Create new testrun.
    """
    scenario = load_by_id_from_mongodb('scenario', scenario_id, {'_id': 1, 'testruns': 1})
    if not scenario:
        raise HTTPException(status_code=404, detail="The scenario with this id does not exist in the system.")

    try:
        workspace_path = RedisClient.hget('testrun', 'workspace_path')
        testrun_id = datetime.now().strftime("%Y-%m-%dT%H%M%SF%f")

        # 폴더 생성
        path = f'{workspace_path}/{testrun_id}'
        os.makedirs(f'{path}/raw')
        os.makedirs(f'{path}/analysis')

        # 시나리오 변경
        testruns = scenario.get('testruns', [])
        testruns.append({'id': testrun_id,
                         'is_active': True,
                         'raw': {'videos': []},
                         'analysis': {}})
        update_by_id_to_mongodb(col='scenario',
                                id=scenario_id,
                                data={'updated_at': get_utc_datetime(time.time()),
                                      'testruns': testruns})

        # 워크스페이스 변경
        RedisClient.hset('testrun', 'id', testrun_id)
        RedisClient.hset('testrun', 'scenario_id', scenario_id)

        # 워크스페이스 변경 메세지 전송
        RedisClient.publish('command',
                            set_redis_pub_msg(msg="workspace",
                                              data={"workspace_path": workspace_path,
                                                    "testrun_id": testrun_id,
                                                    "scenario_id": scenario_id}))

    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new testrun', 'id': testrun_id}


@router.delete("/{scenario_id}/{testrun_id}", response_model=schemas.Msg)
def delete_testrun(
    scenario_id: str,
    testrun_id: str,
) -> schemas.Msg:
    """
    Delete a testrun.
    """
    pipeline = [{'$match': {'id': scenario_id, 'testruns.id': testrun_id}},
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
                          data={"testruns.$.is_active": False})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Delete a scenario.'}


@router.get("", response_model=schemas.Testrun)
def read_testruns(
    scenario_id: Optional[str] = None,
) -> schemas.Testrun:
    """
    Retrieve testruns.
    """
    try:
        param = {}
        if scenario_id:
            param['id'] = scenario_id

        pipeline = [{"$match": param},
                    {"$unwind": "$testruns"},
                    {"$project": {"testrun_id": "$testruns.id",
                                  "is_active": "$testruns.is_active",
                                  "last_timestamp": "$testruns.analysis.last_timestamp",
                                  "targets": "$testruns.analysis.targets.type"}},
                    {'$match': {"is_active": True}},
                    {"$group": {"_id": {
                                "testrun_id": "$testrun_id",
                                "last_timestamp": "$last_timestamp",
                                "targets": "$targets"}}},
                    {"$project": {"_id": 0,
                                  "id": "$_id.testrun_id",
                                  "last_updated": "$_id.last_timestamp",
                                  "analysis_targets": "$_id.targets"}}]
        res = aggregate_from_mongodb('scenario', pipeline)

        items = []
        for x in res:
            x['analysis_targets'] = sorted(set(x.get('analysis_targets', [])))
            items.append(x)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {"items": items}
