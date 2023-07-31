import logging
import uuid

from app import schemas
from app.api.utility import get_multi_or_paginate_by_res
from app.crud.base import (delete_by_id_to_mongodb, insert_to_mongodb,
                           load_by_id_from_mongodb, update_by_id_to_mongodb)
from fastapi import APIRouter, HTTPException, File, UploadFile

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/files_upload", response_model=schemas.Msg)
def files_upload(
    files: list[UploadFile]
) -> schemas.Msg:
    return {'msg': ''}