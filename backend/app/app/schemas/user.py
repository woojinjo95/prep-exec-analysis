from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    user_id: str
    password: str


class UserUpdate(BaseModel):
    password: Optional[str]


class User(UserBase):
    id: int
