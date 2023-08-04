from typing import Optional, List
from pydantic import BaseModel
from app.schemas.enum import RemoconEnum

class Remocon(BaseModel):
    class remocon_code(BaseModel):
        name: str
        code_name: str
        pronto_code: str
        coordinate: List[int]
        hotkey: List[str]

    class custom_key(BaseModel):
        id: Optional[str] = None
        name: str
        custom_code: List[str]
        order: int

    name: RemoconEnum
    image_path: str
    remocon_codes: List[remocon_code]
    custom_keys: List[custom_key]


class RemoconUpdate(BaseModel):
    name: Optional[str]
    image_path: Optional[str]
    remocon_codes: Optional[List] = []
    custom_keys: Optional[List] = []


class RemoconRead(BaseModel):
    items: List[Remocon]


class RemoconCustomKeyCreate(BaseModel):
    id: Optional[str]
    name: str
    custom_code: List[str]
    order: int


class RemoconCustomKeyCreateBase(BaseModel):
    remocon_name: RemoconEnum
    name: str
    custom_code: List[str]


class RemoconCustomKeyUpdate(BaseModel):
    id: str
    name: str
    custom_code: List[str]


class RemoconCustomKeyUpdateMulti(BaseModel):
    custom_key_ids: List[str]
