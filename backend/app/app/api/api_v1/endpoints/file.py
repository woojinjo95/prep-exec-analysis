import logging
import os

from app.core.config import settings
from app.crud.base import load_by_id_from_mongodb
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/download', response_class=FileResponse)
async def file_download(
    id: str = None,
    path: str = None,
) -> FileResponse:
    if id:
        file = load_by_id_from_mongodb(col='file', id=id)
        if not file:
            raise HTTPException(status_code=404, detail=f"The file does not exist in the system.")
        name = file.get('name', '')
        path = file.get('path', '')
    elif path:
        name = path.split("/")[-1] if "/" in path else ''
    return FileResponse(path=path, filename=name)


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
