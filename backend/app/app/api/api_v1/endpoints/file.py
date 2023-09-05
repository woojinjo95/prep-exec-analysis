import logging
import os

from app.core.config import settings
from app.crud.base import load_by_id_from_mongodb
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/download/{file_id}', response_class=FileResponse)
async def file_download(
    file_id: str
) -> FileResponse:
    file = load_by_id_from_mongodb(col='file', id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail=f"The file does not exist in the system.")
    file_name = file.get('name', '')
    file_path = file.get('path', '')
    return FileResponse(path=file_path, filename=file_name)


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
