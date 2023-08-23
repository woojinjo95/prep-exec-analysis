import logging
import os
import traceback
from typing import Optional
from uuid import uuid4

from app import schemas
from app.api.utility import classify_file_type
from app.core.config import settings
from app.crud.base import (aggregate_from_mongodb, insert_one_to_mongodb,
                           load_from_mongodb)
from app.db.redis_session import RedisClient
from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=schemas.MsgWithId)
async def file_upload(
    file: UploadFile = File(...)
) -> schemas.MsgWithId:
    if file is None:
        raise HTTPException(status_code=400, detail="No upload file")
    file_uuid = str(uuid4())
    insert_one_to_mongodb(col='file', data={'file_id': file_uuid, "file_name": file.filename})

    file_dir = classify_file_type(file.filename)
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    with open(os.path.join(file_dir, file_uuid), 'wb') as f:
        f.write(file.file.read())
    return {'msg': f'{file.filename} uploaded successfully',
            'id': file_uuid}


@router.get('/download/{file_id}', response_class=FileResponse)
async def file_download(
    file_id: str
) -> FileResponse:
    file_info = load_from_mongodb(col='file', param={'file_id': file_id})
    if file_info == []:
        raise HTTPException(status_code=400, detail="No file")
    file_name = file_info[0]['file_name']
    file_dir = classify_file_type(file_name)
    file_dir = os.path.join(file_dir, file_id)
    return FileResponse(path=file_dir, filename=file_name)


@router.get('/system_file/{file_name}', response_class=FileResponse)
async def system_file_download(
    file_name: str,
) -> FileResponse:
    """
    시스템 파일 다운로드
    """
    file_dir = os.path.join(settings.FILES_PATH, 'system', file_name)
    if not os.path.isfile(path=file_dir):
        raise HTTPException(status_code=400, detail="No file")
    return FileResponse(path=file_dir, filename=file_name)


@router.get('/partial_video', response_class=FileResponse)
async def partial_video_download(
    scenario_id: Optional[str] = None,
    range: str = Header(None)
) -> FileResponse:
    """
    워크스페이스 비디오 파일 특정 범위 다운로드
    """
    if scenario_id is None:
        scenario_id = RedisClient.hget('testrun', 'scenario_id')
    pipeline = [{'$match': {'id': scenario_id}},
                {'$project': {'_id': 0, 'videos': '$testrun.raw.videos'}}]
    video_info = aggregate_from_mongodb(col='scenario', pipeline=pipeline)
    if not video_info:
        raise HTTPException(status_code=404, detail="Scenario data not found")

    try:
        video_info = video_info[0].get('videos', [{}])[0]
        video_file_path = video_info.get('path', '')
        video_file_path = video_file_path.replace('./data', '/app')

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
        raise HTTPException(status_code=500, detail=traceback.format_exc())

