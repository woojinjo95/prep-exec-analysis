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
    remocon_name: str
    name: str
    custom_code: List[str]


class RemoconCustomKeyUpdate(BaseModel):
    id: str
    name: str
    custom_code: List[str]


class RemoconCustomKeyUpdateMulti(BaseModel):
    custom_key_ids: List[str]
