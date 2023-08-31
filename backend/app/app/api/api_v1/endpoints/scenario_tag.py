import logging
import traceback

from app import schemas
from app.api.utility import parse_bytes_to_value
from app.crud.base import get_mongodb_collection
from app.db.redis_session import RedisClient
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.ScenarioTag)
def read_scenario_tags() -> schemas.ScenarioTag:
    """
    Retrieve scenario tags.
    """
    try:
        tags = RedisClient.hget('testrun', 'tags')
        res = {'tags': sorted(parse_bytes_to_value(tags)) if tags else []}
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'items': res}


@router.post("", response_model=schemas.Msg)
def create_tag(
    *,
    tag_in: schemas.ScenarioTagUpdate,
) -> schemas.Msg:
    """
    Create new tag.
    """
    tags = RedisClient.hget('testrun', 'tags')
    tag_list = parse_bytes_to_value(tags) if tags else []
    if tag_in.tag in tag_list:
        raise HTTPException(status_code=406, detail="The scenario tag already exists in the system.")
    try:
        tag_list.append(tag_in.tag)
        RedisClient.hset('testrun', 'tags', str(tag_list))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Create new tag'}


@router.put("/{tag}", response_model=schemas.Msg)
def update_scenario_tag(
    *,
    tag: str,
    tag_in: schemas.ScenarioTagUpdate,
) -> schemas.Msg:
    """
    Update a scenario tag.
    """
    tags = RedisClient.hget('testrun', 'tags')
    tag_list = parse_bytes_to_value(tags) if tags else []
    if tag != tag_in.tag and tag_in.tag in tag_list:
        raise HTTPException(
            status_code=406, detail="The scenario tag already exists in the system.")
    try:
        # 태그 수정
        tag_list.append(tag_in.tag)
        RedisClient.hset('testrun', 'tags', str(tag_list))

        # 시나리오에 할당 된 태그 전부 수정
        col = get_mongodb_collection('scenario')
        col.update_many({"tags": tag},
                        {"$set": {"tags.$[elem]": tag_in.tag}},
                        array_filters=[{"elem": tag}])
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Update a scenario tag.'}


@router.delete("/{tag}", response_model=schemas.Msg)
def delete_scenario_tag(
    *,
    tag: str,
) -> schemas.Msg:
    """
    Delete a scenario tag.
    """
    try:
        # 태그 삭제
        tags = RedisClient.hget('testrun', 'tags')
        tag_list = parse_bytes_to_value(tags) if tags else []
        tag_list.remove(tag)
        RedisClient.hset('testrun', 'tags', str(tag_list))

        # 시나리오에 할당 된 태그 전부 삭제
        col = get_mongodb_collection('scenario')
        col.update_many({"tags": tag},
                        {"$pull": {"tags": tag}})
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': 'Delete a scenario tag.'}
