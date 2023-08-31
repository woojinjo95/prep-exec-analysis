import json
import logging
import os
import traceback
from uuid import uuid4

from app import schemas
from app.api.utility import parse_bytes_to_value
from app.core.config import settings
from app.crud.base import insert_one_to_mongodb, load_from_mongodb
from app.db.redis_session import RedisClient
from app.schemas.enum import AnalysisTypeEnum
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.AnalysisConfigBase)
def read_analysis_config() -> schemas.AnalysisConfigBase:
    """
    Retrieve analysis_config.
    """
    try:
        analysis_config = {}
        for key in RedisClient.scan_iter(match="analysis_config:*"):
            analysis_config[key.split(':')[1]] = {k: parse_bytes_to_value(v)
                                                  for k, v in RedisClient.hgetall(key).items()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': analysis_config}


@router.put("", response_model=schemas.Msg)
def update_analysis_config(
    *,
    analysis_config_in: schemas.AnalysisConfig,
) -> schemas.Msg:
    """
    Update analysis_config.
    """
    try:
        for key, val in jsonable_encoder(analysis_config_in).items():
            if val is not None and key in AnalysisTypeEnum.list():
                for k, v in val.items():
                    RedisClient.hset(f'analysis_config:{key}', k, json.dumps(v))
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update analysis_config'}


@router.delete("/{analysis_type}", response_model=schemas.Msg)
def delete_analysis_config(
    *,
    analysis_type: AnalysisTypeEnum,
) -> schemas.Msg:
    """
    Delete analysis_config.
    """
    analysis_type = analysis_type.value
    name = f'analysis_config:{analysis_type}'
    if not RedisClient.hgetall(name=name):
        raise HTTPException(
            status_code=404, detail=f"The analysis_config with this {analysis_type} does not exist in the system.")
    try:
        RedisClient.delete(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f'Delete {analysis_type} analysis_config'}


@router.post("/frame", response_model=schemas.FrameImage)
async def upload_frame(
    file: UploadFile = File(...)
) -> schemas.FrameImage:
    """
    Upload frame.
    """
    if file is None:
        raise HTTPException(status_code=400, detail="No upload file")
    try:
        file_uuid = str(uuid4())
        filename, file_extension = file.filename.split(".")
        workspace_path = f"{RedisClient.hget('testrun','workspace_path')}/{RedisClient.hget('testrun','id')}/raw/frame"
        insert_one_to_mongodb(col='file', data={'id': file_uuid, "name": filename,
                              "path": workspace_path, "extension": file_extension})
        if not os.path.isdir(workspace_path):
            os.mkdir(workspace_path)
        with open(os.path.join(workspace_path, f'{file_uuid}.{file_extension}'), 'wb') as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'id': file_uuid, 'path': f"{workspace_path}/{file_uuid}.{file_extension}"}


@router.get('/frame/{frame_id}', response_class=FileResponse)
async def download_frame(
    frame_id: str
) -> FileResponse:
    """
    Download frame.
    """
    file = load_from_mongodb(col='file', param={'id': frame_id})
    if not file:
        raise HTTPException(status_code=404, detail=f"The frame does not exist in the system.")
    try:
        file_name = file[0]['name']
        file_extension = file[0]['extension']
        workspace_path = f"{RedisClient.hget('testrun','workspace_path')}/{RedisClient.hget('testrun','id')}/raw/frame/{frame_id}.{file_extension}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return FileResponse(path=workspace_path, filename=f'{file_name}.{file_extension}')
