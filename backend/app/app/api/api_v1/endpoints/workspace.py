import logging

from app import schemas
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/video")
def read_video_file() -> StreamingResponse:
    """
    비디오 파일 재생
    """
    # TODO: 비디오 파일에 대한 정보는 어디에..
    video_file_name = 'temp_video_file.mp4'
    video_file_path = RedisClient.hget("common", "testrun_path")

    def iterfile():
        with open(f"{video_file_path}/{video_file_name}", mode="rb") as video_file:
            yield from video_file
    return StreamingResponse(iterfile(), media_type="video/mp4")
