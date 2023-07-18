from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str = None
    refresh_token:  Optional[str] = None


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None


class LoginInfo(BaseModel):
    user_id: str
    password: str


class AccessToken(BaseModel):
    access_token: str
