import io
import json
import logging
import os
import traceback
import zipfile
from datetime import datetime
from typing import Optional

from app import schemas
from app.core.config import settings
from app.crud.base import (delete_many_to_mongodb, insert_one_to_mongodb,
                           load_from_mongodb)
from app.db.redis_session import RedisClient
from fastapi import APIRouter, File, HTTPException, Query, Response, UploadFile

logger = logging.getLogger(__name__)
router = APIRouter()


# @router.get("/timezone", response_model=schemas.Timezone)
def read_timezone() -> schemas.Timezone:
    """
    타임존 확인
    """
    return {'timezone': RedisClient.hget('common', 'timezone')}


@router.get("/service_state", response_model=schemas.ServiceState)
def read_service_state() -> schemas.ServiceState:
    """
    Retrieve service_state.
    """
    return {'items': {'state': RedisClient.hget('common', 'service_state')}}


@router.get("/log_connection_status", response_model=schemas.LogConnectionStatus)
def read_log_connection_status() -> schemas.LogConnectionStatus:
    """
    Retrieve log_connection_status.
    """
    return {'items': {'status': RedisClient.hget('log_connection_status', 'is_connected')}}


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # TODO 타임존 복구 확인
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def add_directory_to_zip(directory_path, zipf, root_folder_name):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory_path)
            zipf.write(file_path, os.path.join(root_folder_name, relative_path))


@router.get("/export_result")
async def export_result(
    scenario_id: Optional[str] = None,
    testrun_id: Optional[str] = None,
    items: str = Query(None, description='ex) stb_log,videos'),
):
    try:
        if scenario_id is None:
            scenario_id = RedisClient.hget('testrun', 'scenario_id')
        if testrun_id is None:
            testrun_id = RedisClient.hget('testrun', 'id')
        export_type = {
            'file': ['videos', 'packet'],
            'redis': ['analysis_config'],
            'mongodb': ['scenario', 'stb_log'],
        }
        items = f'scenario,{items}' if items else 'scenario'
        export_item = {key: [item for item in items.split(',') if item in values]
                       for key, values in export_type.items()}

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            # file
            for file_type in export_item['file']:
                path = f"{RedisClient.hget('testrun', 'workspace_path').replace(settings.CONTAINER_PATH, settings.HOST_PATH)}/{testrun_id}/raw/{file_type}"
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, path)
                        zipf.write(file_path, os.path.join(testrun_id, 'raw', file_type, relative_path))

            # redis
            for redis_key in export_item['redis']:
                matching_keys = RedisClient.scan_iter(match=f"{redis_key}:*")
                for key in matching_keys:
                    json_filename = f'{redis_key}/{key.split(":")[1]}.json'
                    data = json.dumps(RedisClient.hgetall(key))
                    zipf.writestr(json_filename, data)

            # mongodb
            for collection_name in export_item['mongodb']:
                param = {'id': scenario_id} if collection_name == 'scenario' \
                    else {'scenario_id': scenario_id, 'testrun_id': testrun_id}
                for document in load_from_mongodb(collection_name, param):
                    json_filename = f"{collection_name}/{document['_id']}.json"
                    del document['_id']
                    data = json.dumps(document, indent=4, ensure_ascii=False, default=serialize_datetime)
                    zipf.writestr(json_filename, data)

        zip_buffer.seek(0)
        headers = {"Content-Disposition": f"attachment; filename=results_{datetime.today().strftime('%Y-%m-%dT%H%M%SF%f')}.zip"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return Response(content=zip_buffer.read(), headers=headers, media_type="application/zip")


@router.post("/import_result", response_model=schemas.Msg)
async def import_result(file: UploadFile = File(...)) -> schemas.Msg:
    try:
        zip_data = await file.read()
        with zipfile.ZipFile(io.BytesIO(zip_data), "r") as zipf:
            for filename in zipf.namelist():
                collection_name = os.path.dirname(filename)
                delete_many_to_mongodb(collection_name)

                file_data = zipf.read(filename).decode("utf-8")
                document = json.loads(file_data)
                insert_one_to_mongodb(collection_name, document)
    except Exception as e:
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f"Data from {file.filename} uploaded and restored to corresponding collections"}
