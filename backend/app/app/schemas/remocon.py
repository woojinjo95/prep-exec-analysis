import uuid

from typing import Optional
from pydantic import BaseModel


class Remocon(BaseModel):
    class remocon_code(BaseModel):
        name: str
        hotkey: str
        code: str
        location: list[dict]
    
    class custom_key(BaseModel):
        id: Optional[str] = None
        name: str
        custom_code: str
        order: int

    id: Optional[str] = None
    name: str
    image_path: str
    image_resolution: dict
    remocon_codes: list[remocon_code]
    custom_keys: list[custom_key]

    class Config:
        orm_mode = True


class RemoconCustomKeyCreate(BaseModel):
    id: Optional[str]
    name: Optional[str]
    custom_code: str
    order: Optional[int]


class RemoconCustomKeyUpdate(BaseModel):
    name: Optional[str]
    custom_code: Optional[str]
