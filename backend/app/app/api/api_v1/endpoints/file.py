import logging
import os

from uuid import uuid4
from app import schemas
from app.crud.base import insert_to_mongodb, load_from_mongodb
from app.core.config import settings
from app.api.utility import classify_file_type
from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=schemas.MsgWithId)
async def file_upload(
    file: UploadFile = File(...)
) -> schemas.MsgWithId:
    if file is None:
        raise HTTPException(status_code=400, detail="No upload file")
    
    file_uuid = str(uuid4())
    insert_to_mongodb(col='files', data={'file_id':file_uuid, "file_name":file.filename})

    file_dir = classify_file_type(file.filename)
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    with open(os.path.join(file_dir, file_uuid), 'wb') as f:
        f.write(file.file.read())
    
    return {'msg': f'{file.filename} uploaded successfully',
            'id': file_uuid}


@router.get('/download/{file_uuid}', response_class=FileResponse)
async def file_download(
    file_uuid: str
) -> FileResponse:
    file_info = load_from_mongodb(col='file', param={'file_id': {'$eq': file_uuid}})
    if file_info == []:
        raise HTTPException(status_code=400, detail="No file")
    file_name = file_info[0]['file_name']
    file_dir = classify_file_type(file_name)
    file_dir = os.path.join(file_dir, file_info[0]['file_id'])
    return FileResponse(path=file_dir, filename=file_name)


@router.get('/system_file/{file_name}', response_class=FileResponse)
async def system_file_download(
    file_name: str,
) -> FileResponse:
    file_dir = os.path.join(settings.FILES_PATH, 'system', file_name)
    if not os.path.isfile(path=file_dir):
        raise HTTPException(status_code=400, detail="No file")
    return FileResponse(path=file_dir, filename=file_name)
