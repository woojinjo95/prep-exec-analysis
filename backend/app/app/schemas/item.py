from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str


class ItemCreate(ItemBase):
    id: str


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: str


class ItemPage(BaseModel):
    total: Optional[int]
    pages: Optional[int]
    prev: Optional[int]
    next: Optional[int]
    items: List[Item]
