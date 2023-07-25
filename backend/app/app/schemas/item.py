from app.schemas.base import PyObjectId
from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # TODO 컬럼명 커스텀

    class Config:
        json_encoders = {ObjectId: str}
