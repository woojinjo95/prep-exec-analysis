import logging
import os
import time
import traceback
from datetime import datetime

from app import schemas
from app.api.utility import get_utc_datetime, set_redis_pub_msg
from app.crud.base import load_by_id_from_mongodb, update_by_id_to_mongodb
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
        testrun_id = datetime.now().strftime("%Y-%m-%dT%H%M%SF%f")

        # 폴더 생성
        path = f'/app/workspace/testruns/{testrun_id}'
        os.makedirs(f'{path}/raw')
        os.makedirs(f'{path}/analysis')

        # 시나리오 변경
        testruns = scenario.get('testruns', [])
        testruns.append({'id': testrun_id,
                         'raw': {'videos': []},
                         'analysis': {'videos': []}})
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
                                              data={"workspace_path": RedisClient.hget('testrun', 'workspace_path'),
                                                    "testrun_id": testrun_id,
                                                    "scenario_id": scenario_id}))

    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new testrun', 'id': testrun_id}
