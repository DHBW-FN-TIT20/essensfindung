import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    last_login: datetime.datetime

    class Config:
        orm_mode = True
