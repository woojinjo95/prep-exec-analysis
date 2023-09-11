import logging
import os
import traceback
from typing import Optional

from app import schemas
from app.api.utility import set_redis_pub_msg
from app.crud.base import aggregate_from_mongodb, load_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import FileResponse, Response

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/video_summary', response_model=schemas.VideoTimestamp)
def get_analysis_result_video_summary(
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
) -> schemas.VideoTimestamp:
    if scenario_id is None:
        scenario_id = RedisClient.hget('testrun', 'scenario_id')
    if testrun_id is None:
        testrun_id = RedisClient.hget('testrun', 'id')

    pipeline = [{'$match': {'id': scenario_id, 'testruns.id': testrun_id}},
                {'$unwind': "$testruns"},
                {'$match': {"testruns.id": testrun_id}},
                {'$unwind': "$testruns.raw.videos"},
                {'$project': {"_id": 0,
                              "path": "$testruns.raw.videos.path",
                              "start_time": "$testruns.raw.videos.start_time",
                              "end_time": "$testruns.raw.videos.end_time"}}]
    video = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not video:
        raise HTTPException(status_code=404, detail='Video data Not Found')

    video = video[0]  # TODO 0번째 요소에 대한 접근법은 추후에 수정해야 할 부분
    return {'items': {'path': video['path'],
                      'start_time': video['start_time'],
                      'end_time': video['end_time']}}


@router.get('/video_snapshot', response_model=schemas.VideoSnapshot)
def get_analysis_result_video_snapshot(
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
) -> schemas.VideoSnapshot:
    if scenario_id is None:
        scenario_id = RedisClient.hget('testrun', 'scenario_id')
    if testrun_id is None:
        testrun_id = RedisClient.hget('testrun', 'id')

    snapshots = load_from_mongodb('video_snapshot',
                                  {'scenario_id': scenario_id, 'testrun_id': testrun_id},
                                  {'_id': 0, 'path': 1, 'extension': 1, 'names': 1})
    if not snapshots:
        raise HTTPException(status_code=404, detail='video snapshot data Not Found')

    snapshot = snapshots[0]
    return {'items': [{'path': f'{snapshot.get("path", "")}/{snapshot_name}.{snapshot.get("extension", "")}',
                       'timestamp': snapshot_name}
                      for snapshot_name in snapshot.get('names', [])]}


@router.get('/video', response_class=FileResponse)
async def get_analysis_result_video(
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
) -> FileResponse:
    if scenario_id is None:
        scenario_id = RedisClient.hget('testrun', 'scenario_id')
    if testrun_id is None:
        testrun_id = RedisClient.hget('testrun', 'id')

    pipeline = [{'$match': {'id': scenario_id, 'testruns.id': testrun_id}},
                {'$unwind': "$testruns"},
                {'$match': {"testruns.id": testrun_id}},
                {'$unwind': "$testruns.raw.videos"},
                {'$project': {'_id': 0, "path": "$testruns.raw.videos.path"}}]
    video = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not video or video[0].get('path', None) is None:
        raise HTTPException(status_code=404, detail="Scenario data not found")

    try:
        video_file_path = video[0]['path']
        with open(video_file_path, "rb") as video:
            headers = {'Accept-Ranges': 'bytes'}
            return Response(video.read(), headers=headers, media_type="video/mp4")
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())


@router.get('/partial_video', response_class=FileResponse)
async def get_analysis_result_partial_video(
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    range: str = Header(None)
) -> FileResponse:
    if scenario_id is None:
        scenario_id = RedisClient.hget('testrun', 'scenario_id')
    if testrun_id is None:
        testrun_id = RedisClient.hget('testrun', 'id')

    pipeline = [{'$match': {'id': scenario_id, 'testruns.id': testrun_id}},
                {'$unwind': "$testruns"},
                {'$match': {"testruns.id": testrun_id}},
                {'$unwind': "$testruns.raw.videos"},
                {'$project': {'_id': 0, "path": "$testruns.raw.videos.path"}}]
    video = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not video or video[0].get('path', None) is None:
        raise HTTPException(status_code=404, detail="Scenario data not found")

    try:
        video_file_path = video[0]['path']

        if not range:
            return FileResponse(video_file_path)

        CHUNK_SIZE = 1024*1024*5  # TODO 운영하면서 조절
        start, end = range.replace("bytes=", "").split("-")
        start = int(start)
        end = int(end) if end else start + CHUNK_SIZE
        video_size = os.path.getsize(video_file_path)

        if start < 0:
            start = 0
        if end >= video_size:
            end = video_size - 1

        with open(video_file_path, "rb") as video_file:
            video_file.seek(start)
            content = video_file.read(end - start + 1)

        headers = {
            "Content-Range": f"bytes {start}-{end}/{video_size}",
            "Accept-Ranges": "bytes",
        }
        return Response(content, headers=headers, status_code=206, media_type="video/mp4")
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
