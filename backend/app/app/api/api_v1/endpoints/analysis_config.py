import logging
import uuid

from app import schemas
from app.crud.base import load_one_from_mongodb, update_many_to_mongodb
from app.schemas.enum import AnalysisTypeEnum
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


def set_uuid(val):
    frames = val.get('frames', [])
    for frame in frames:
        frame['id'] = str(uuid.uuid4())
        for roi in frame['rois']:
            roi['id'] = str(uuid.uuid4())
    if frames:
        val['frames'] = frames
    return val


@router.get("", response_model=schemas.AnalysisConfigBase)
def read_analysis_config() -> schemas.AnalysisConfigBase:
    """
    Retrieve analysis_config.
    """
    return {'items': load_one_from_mongodb(col='analysis_config')}


@router.put("", response_model=schemas.Msg)
def update_analysis_config(
    *,
    analysis_config_in: schemas.AnalysisConfig,
) -> schemas.Msg:
    """
    Update analysis_config.
    """
    for key, val in jsonable_encoder(analysis_config_in).items():
        if val is not None and key in AnalysisTypeEnum.list():
            update_many_to_mongodb(col='analysis_config',
                                   data={key: val})
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
    res = update_many_to_mongodb(col='analysis_config',
                                 data={analysis_type: None})
    if res.matched_count == 0:
        raise HTTPException(
            status_code=406, detail="No items have been updated.")
    return {'msg': f'Delete {analysis_type} analysis_config'}
