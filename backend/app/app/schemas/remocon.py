from typing import Optional, List
from pydantic import BaseModel


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

    id: Optional[str] = None
    name: str
    image_path: str
    image_resolution: List
    remocon_codes: List[remocon_code]
    custom_keys: List[custom_key]


class RemoconUpdate(BaseModel):
    name: Optional[str]
    image_path: Optional[str]
    image_resolution: Optional[List] = []
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
    name: str
    custom_code: List[str]
    remocon_id: str


class RemoconCustomKeyUpdate(BaseModel):
    name: Optional[str]
    custom_code: Optional[List[str]]


class RemoconCustomKeyUpdateMulti(BaseModel):
    custom_key_ids: List[str]
