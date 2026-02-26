from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    full_name: str
    email: Optional[str]


class UserCreate(User):
    password: str


class TokenData(BaseModel):
    username: Optional[str] = None
    sub: Optional[str] = None
    id: Optional[int] = None
    exp: Optional[int] = None


class UserLogin(BaseModel):
    email: str
    password: str
