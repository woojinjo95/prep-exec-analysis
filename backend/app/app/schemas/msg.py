from pydantic import BaseModel


class Msg(BaseModel):
    msg: str


class MsgWithId(BaseModel):
    msg: str
    id: int
