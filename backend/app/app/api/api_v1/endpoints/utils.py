import io
import json
import logging
import os
import traceback
import zipfile

from app import schemas
from app.crud.base import (delete_many_to_mongodb, insert_one_to_mongodb,
                           load_from_mongodb)
from fastapi import APIRouter, File, HTTPException, Response, UploadFile

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/export_result")
async def export_result():
    collection_names_list = ['terminal_log', 'stb_log']

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for collection_name in collection_names_list:
            for document in load_from_mongodb(collection_name):
                json_filename = f"{collection_name}/{document['_id']}.json"

                del document['_id']
                json_data = json.dumps(document, indent=4, ensure_ascii=False)

                zipf.writestr(json_filename, json_data)

    zip_buffer.seek(0)
    headers = {"Content-Disposition": f"attachment; filename=results.zip"}
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
