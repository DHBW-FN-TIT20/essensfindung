""" Contains all classes for the user """
import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base Class for all User

    Attributes:
        email (str): Email of the User

    """

    email: str


class UserCreate(UserBase):
    """
    Class to create an User.

    Attributes:
        password (str): Plaintext password
    """

    password: str


class User(UserBase):
    """
    User with mail an last_login

    Attributes:
        last_login (datetime.datetime): Timestamp of last login
    """

    last_login: datetime.datetime

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    """
    User if he try to login

    Attributes:
        hashed_password (str): Hashed user password
        last_login (Optional[datetime.datetime]): Defaults to None
    """

    hashed_password: str
    last_login: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True
