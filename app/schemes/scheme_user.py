import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    last_login: datetime.datetime

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    hashed_password: str
    last_login: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True
