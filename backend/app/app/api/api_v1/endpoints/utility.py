import io
import json
import logging
import os
import re
import traceback
import zipfile
from datetime import datetime

from app import schemas
from app.api.utility import (convert_data_in, deserialize_datetime,
                             serialize_datetime)
from app.crud.base import insert_many_to_mongodb, load_from_mongodb
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
            'file': ['videos', 'frames'],
            'db': ['scenario', 'stb_log', 'network_trace', 'terminal_log',
                   'an_color_reference', 'an_freeze', 'loudness', 'an_warm_boot',
                   'an_cold_boot', 'an_log_pattern', 'monkey_smart_sense', 'monkey_section', 'stb_info']
        }
        export_item = {key: [item for item in jsonable_encoder(export_in.items) if item in values]
                       for key, values in export_type.items()}
        scenario_id = export_in.scenario_id if export_in.scenario_id else RedisClient.hget('testrun', 'scenario_id')
        testrun_id = export_in.testrun_id if export_in.testrun_id else RedisClient.hget('testrun', 'id')

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for file_type in export_item['file']:
                path = f"{RedisClient.hget('testrun', 'workspace_path')}/{testrun_id}/raw/{file_type}"
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, path)
                        zipf.write(file_path, os.path.join('file', f'{testrun_id}', 'raw', file_type, relative_path))

            for collection_name in export_item['db']:
                param = {'id': scenario_id} if collection_name == 'scenario' \
                    else {'scenario_id': scenario_id, 'testrun_id': testrun_id}
                for document in load_from_mongodb(collection_name, param):
                    file_path = f"db/{collection_name}/{document['_id']}.json"
                    del document['_id']
                    data = json.dumps(document, indent=4, ensure_ascii=False, default=serialize_datetime)
                    zipf.writestr(file_path, data)

        zip_buffer.seek(0)
        headers = {"Content-Disposition": f"attachment; filename=results_{now}.zip"}
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return Response(content=zip_buffer.read(), headers=headers, media_type="application/zip")


# @router.post("/import_result", response_model=schemas.Msg)
async def import_result(file: UploadFile = File(...)) -> schemas.Msg:
    try:
        mongo_data = {}
        zip_data = await file.read()
        with zipfile.ZipFile(io.BytesIO(zip_data), "r") as zipf:
            for full_name in zipf.namelist():
                file_info = full_name.split('/')
                file_type = file_info[0]
                file_name = file_info[-1]
                file_path = '/'.join(file_info[1:-1])

                if file_type == 'file':
                    workspace_path = RedisClient.hget('testrun', 'workspace_path')
                    real_path = f"{workspace_path}/{file_path}"
                    if not os.path.isdir(real_path):
                        os.mkdir(real_path)
                    with open(f'{real_path}/{file_name}', 'wb') as f:
                        f.write(file.file.read())

                if file_type == 'db':
                    file_data = zipf.read(full_name).decode("utf-8")
                    collection_name = os.path.dirname(f'{file_path}/{file_name}')
                    data = convert_data_in(collection_name, deserialize_datetime(json.loads(file_data)))
                    if collection_name in mongo_data:
                        mongo_data[collection_name].append(data)
                    else:
                        mongo_data[collection_name] = [data]

        for collection_name, data in mongo_data.items():
            insert_many_to_mongodb(collection_name, jsonable_encoder(data))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {'msg': f"Data from {file.filename} uploaded and restored to corresponding collections"}


@router.post("/validate_regex", response_model=schemas.RegexResult)
def validate_regex(
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
