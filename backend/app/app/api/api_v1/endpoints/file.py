import logging
import os

from app import schemas
from app.core.config import settings
from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=schemas.Msg)
async def file_upload(
    file: UploadFile = File(...)
) -> schemas.Msg:
    if file is None:
        raise HTTPException(status_code=400, detail="No upload file")
    
    file_exp = file.filename.split('.')[-1]
    if file_exp in ['jpg', 'png', 'jpeg', 'gif']:
        file_dir = os.path.join(settings.FILES_PATH, 'images')
    elif file_exp in ['mp4', 'avi']:
        file_dir = os.path.join(settings.FILES_PATH, 'videos')
    else:
        file_dir = os.path.join(settings.FILES_PATH, 'etc')
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    with open(os.path.join(file_dir, file.filename), 'wb') as f:
        f.write(file.file.read())
    
    return {'msg': f'{file.filename} uploaded successfully'}


@router.get('/download', response_class=FileResponse)
async def file_download(
    file_name: str
) -> FileResponse:
    file_exp = file_name.split('.')[-1]
    if file_exp in ['jpg', 'jpeg', 'png', 'gif']:
        file_dir = os.path.join(settings.FILES_PATH, 'images', file_name)
    elif file_exp in ['mp4', 'avi']:
        file_dir = os.path.join(settings.FILES_PATH, 'videos', file_name)
    else:
        file_dir = os.path.join(settings.FILES_PATH, 'etc', file_name)
    
    if not os.path.isfile(path=file_dir):
        raise HTTPException(status_code=400, detail="No file")
    
    return FileResponse(path=file_dir, filename=file_name)