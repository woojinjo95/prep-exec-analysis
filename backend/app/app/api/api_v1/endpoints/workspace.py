import logging

from app import schemas
from app.crud.base import load_from_mongodb, aggregate_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/video")
def read_video_file(
    scenario_id: str
):
# ) -> StreamingResponse:
    """
    비디오 파일 재생
    """
    pipeline = [{'$match': {'id': scenario_id}},
                {'$project': {'_id': 0, 'videos': '$testrun.raw.videos'}},
                ]
    video_info = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not video_info:
        raise HTTPException(status_code=404, detail="Scenario data not found")
    video_info = video_info[0]['videos'][0]
    video_file_path = video_info.get('path', '')
    video_file_path = video_file_path.replace('./data', '/app')
    def iterfile():
        with open(f"{video_file_path}", mode="rb") as video_file:
            yield from video_file
    return StreamingResponse(iterfile(), media_type="video/mp4")
