import logging
import os
import traceback
from uuid import uuid4

from app import schemas
from app.api.utility import classify_file_type
from app.core.config import settings
from app.crud.base import insert_one_to_mongodb, load_from_mongodb
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()


# @router.post("/upload", response_model=schemas.MsgWithId)
async def file_upload(
    file: UploadFile = File(...)
) -> schemas.MsgWithId:
    if file is None:
        raise HTTPException(status_code=400, detail="No upload file")
    try:
        file_uuid = str(uuid4())
        file_dir = classify_file_type(file.filename)
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        with open(os.path.join(file_dir, file_uuid), 'wb') as f:
            f.write(file.file.read())
        insert_one_to_mongodb(col='file',
                              data={'id': file_uuid, "name": file.filename, "path": file_dir})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'{file.filename} uploaded successfully',
            'id': file_uuid}


# @router.get('/download/{file_id}', response_class=FileResponse)
async def file_download(
    file_id: str
) -> FileResponse:
    file_info = load_from_mongodb(col='file', param={'id': file_id})
    if file_info == []:
        raise HTTPException(status_code=400, detail="No file")
    try:
        file_name = file_info[0]['name']
        file_dir = classify_file_type(file_name)
        file_dir = os.path.join(file_dir, file_id)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
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
