import io
import json
import logging
import os
import re
import traceback
import zipfile
from datetime import datetime

from app import schemas
from app.api.utility import deserialize_datetime, serialize_datetime
from app.crud.base import insert_one_to_mongodb, load_from_mongodb
from app.db.redis_session import RedisClient
from fastapi import APIRouter, File, HTTPException, Response, UploadFile
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger(__name__)
router = APIRouter()


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


# @router.post("/export_result")
async def export_result(
    export_in: schemas.ExportResult,
):
    try:
        now = datetime.today().strftime('%Y-%m-%dT%H%M%SF%f')
        export_type = {
            'file': ['videos'],
            'redis': ['analysis_config'],
            'mongodb': ['scenario', 'stb_log']
        }
        export_item = {key: [item for item in jsonable_encoder(export_in.items) if item in values]
                       for key, values in export_type.items()}
        scenario_id = export_in.scenario_id if export_in.scenario_id else RedisClient.hget('testrun', 'scenario_id')
        testrun_id = export_in.testrun_id if export_in.testrun_id else RedisClient.hget('testrun', 'id')

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            # file
            for file_type in export_item['file']:
                path = f"{RedisClient.hget('testrun', 'workspace_path')}/{testrun_id}/raw/{file_type}"
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, path)
                        zipf.write(file_path, os.path.join(f'{testrun_id}', 'raw', file_type, relative_path))

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
                    if collection_name == 'scenario':
                        document['name'] = f"{document['name']}_{now}"
                    data = json.dumps(document, indent=4, ensure_ascii=False, default=serialize_datetime)
                    zipf.writestr(json_filename, data)

        zip_buffer.seek(0)
        headers = {"Content-Disposition": f"attachment; filename=results_{now}.zip"}
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return Response(content=zip_buffer.read(), headers=headers, media_type="application/zip")


# @router.post("/import_result", response_model=schemas.Msg)
async def import_result(file: UploadFile = File(...)) -> schemas.Msg:
    try:
        import_type = {
            'redis': ['analysis_config'],
            'mongodb': ['scenario', 'stb_log'],
        }
        zip_data = await file.read()
        with zipfile.ZipFile(io.BytesIO(zip_data), "r") as zipf:
            name_list = zipf.namelist()
            if any(item.startswith('analysis_config/') for item in name_list):
                pattern = 'analysis_config:*'
                keys_to_delete = list(RedisClient.keys(pattern))
                if keys_to_delete:
                    RedisClient.delete(*keys_to_delete)

            for filename in name_list:
                file_info = filename.split('/')
                _type = next((key for key, values in import_type.items() if file_info[0] in values), 'file')
                # file
                if _type == 'file':
                    workspace_path = RedisClient.hget('testrun', 'workspace_path')
                    path = f"{workspace_path}/{'/'.join(filename.split('/')[:-1])}"
                    if not os.path.isdir(path):
                        os.mkdir(path)
                    with open(f'{workspace_path}/{filename}', 'wb') as f:
                        f.write(file.file.read())

                if _type in ['redis', 'mongodb']:
                    file_data = zipf.read(filename).decode("utf-8")
                    # redis
                    if _type == 'redis':
                        for k, v in json.loads(file_data).items():
                            RedisClient.hset(f'{file_info[0]}:{file_info[1].split(".")[0]}', k, v)

                    # mongodb
                    if _type == 'mongodb':
                        collection_name = os.path.dirname(filename)
                        document = deserialize_datetime(json.loads(file_data))
                        insert_one_to_mongodb(collection_name, document)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f"Data from {file.filename} uploaded and restored to corresponding collections"}


@router.post("/validate_regex", response_model=schemas.RegexResult)
async def validate_regex(
    *,
    regex_str: schemas.Regex,
) -> schemas.RegexResult:
    """
    Validate regular expression
    """
    try:
        regex_str = regex_str.regex
        regex = re.compile(regex_str)
        if regex.groups > 0:
            if regex.groups != len(regex.groupindex):
                return {"is_valid": False,
                        "msg": f"{regex}",
                        "detail": f"there is no named group: number of groups: {regex.groups}, name_goups: {regex.groupindex.keys()}"}
        return {"is_valid": True, "msg": f"{regex}", "keys": list(regex.groupindex.keys())}
    except Exception as e:
        return {"is_valid": False, "msg": f"{e}"}
