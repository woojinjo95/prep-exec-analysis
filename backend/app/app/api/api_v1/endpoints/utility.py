import logging

from app import schemas
from app.crud.base import aggregate_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/timezone", response_model=schemas.Timezone)
def read_timezone() -> schemas.Timezone:
    """
    타임존 확인
    """
    return {'timezone': RedisClient.hget('common', 'timezone')}


@router.get("/video")
def read_video_file() -> StreamingResponse:
    """
    비디오 파일 재생
    """
    scenario_id = RedisClient.hget('testrun', 'scenario_id')
    if scenario_id is None:
        raise HTTPException(status_code=404, detail="Scenario data not found")
    pipeline = [{'$match': {'id': scenario_id}},
                {'$project': {'_id': 0, 'videos': '$testrun.raw.videos'}},
                ]
    video_info = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not video_info:
        raise HTTPException(status_code=404, detail="Scenario data not found")
    video_info = video_info[0]['videos'][0]
    video_file_path = video_info.get('path', '')
    video_file_path = video_file_path.replace('./data', '/app')
    def video_file_open():
        with open(f"{video_file_path}", mode="rb") as video_file:
            yield from video_file
    return StreamingResponse(video_file_open(), media_type="video/mp4")