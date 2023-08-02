from typing import Optional
from pydantic import BaseModel


class Remocon(BaseModel):
    class remocon_code(BaseModel):
        name: str
        hotkey: list[str]
        pronto_code: str
        coordinate: list[int]

    class custom_key(BaseModel):
        id: Optional[str] = None
        name: str
        custom_code: list[str]
        order: int

    id: Optional[str] = None
    name: str
    image_path: str
    image_resolution: list
    remocon_codes: list[remocon_code]
    custom_keys: list[custom_key]


class RemoconUpdate(BaseModel):
    name: Optional[str]
    image_path: Optional[str]
    image_resolution: Optional[list]
    remocon_codes: Optional[list]
    custom_keys: Optional[list]


class RemoconRead(BaseModel):
    items: list[Remocon]


class RemoconCustomKeyCreate(BaseModel):
    id: Optional[str]
    name: str
    custom_code: list[str]
    order: int


class RemoconCustomKeyCreateBase(BaseModel):
    name: str
    custom_code: list[str]
    remocon_id: str


class RemoconCustomKeyUpdate(BaseModel):
    name: Optional[str]
    custom_code: Optional[list[str]]


class RemoconCustomKeyUpdateMulti(BaseModel):
    custom_key_ids: list[str]
