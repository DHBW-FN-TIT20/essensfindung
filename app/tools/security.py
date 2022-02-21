import json
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import jose
from fastapi import Depends
from fastapi import Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from jose import JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.crud.user import get_user_by_mail
from db.database import get_db
from schemes import exceptions
from schemes.scheme_user import UserLogin
from tools.config import settings
from tools.hashing import Hasher
from tools.my_logging import logger


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "emailInput"
        )  # since outh works on username field we are considering email as username
        self.password = form.get("passwordInput")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.error = "Email is required"
        if not self.error:
            return True
        return False


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")  # changed to accept access token from httpOnly Cookie
        # print("access_token is", authorization)

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise exceptions.NotAuthorizedException(error_msg="No valid Token")
            else:
                return None
        return param


class InvalidTokens:
    def __init__(self):
        self.token_path = Path("./data/invalid_token.json")

    def is_invalid(self, token: str) -> bool:
        """Return true if the token is deactivated / invalid

        Args:
            token (str): Token to check

        Returns:
            bool: True if token is invalid
        """
        self.__clean_tokens__()
        tokens = self.__get_tokens__()
        if any(t.get(token) for t in tokens):
            return True
        return False

    def add_token(self, token: str) -> None:
        """If you add a token the user is forced to login again. Invalid the current JWS Token

        Args:
            token (str): Token to deactivade
        """
        self.token_path.touch(exist_ok=True)
        tokens = self.__get_tokens__()
        tokens.append({token: {"timestamp": datetime.now().timestamp()}})

        with self.token_path.open("w", encoding="utf-8") as file:
            json.dump(tokens, file)

    def __get_tokens__(self) -> List[Dict]:
        """Get the tokens in the buffer

        Returns:
            List[Dict[str]]: List of all Tokens as a dict
        """
        tokens = []
        if not self.token_path.exists():
            return tokens

        with self.token_path.open("r", encoding="utf-8") as file:
            try:
                tokens = json.load(file)
            except json.decoder.JSONDecodeError:
                pass

        return tokens

    def __clean_tokens__(self) -> int:
        """Remove all old Tokens that are safe expired"""
        old_tokens = self.__get_tokens__()
        cleaned_tokens = []
        for token in old_tokens:
            for key in token.keys():
                try:
                    jwt.decode(key, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                except jose.exceptions.ExpiredSignatureError:
                    logger.debug("Removed old Token from invalid DB")
                else:
                    cleaned_tokens.append(token)

        with self.token_path.open("w", encoding="utf-8") as file:
            json.dump(cleaned_tokens, file)

        return abs(len(old_tokens) - len(cleaned_tokens))


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")
invalid_tokens = InvalidTokens()


def authenticate_user(db_session: Session, username: str, password: str) -> Union[UserLogin, None]:
    """Validate the given username and password with the Database

    Args:
        db_session (Session): Session to the Database
        username (str): Email of the user
        password (str): Password to verify

    Returns:
        Union[UserLogin, None]: Return the User OR False
    """
    db_user = get_user_by_mail(db_session, username)
    if not db_user:
        return False
    if not Hasher.verify_password(password, db_user.hashed_password):
        return False
    return UserLogin.from_orm(db_user)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT with the given data and an Expires Delta

    Args:
        data (dict): Data to store in the Token
        expires_delta (Optional[timedelta], optional): Defaults to None.

    Returns:
        str: Created JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def invalid_access_token(token: str = Depends(oauth2_scheme)) -> str:
    """Add the token to local Database and if someone try to authenticate again with these token it will fail

    Args:
        token (str, optional): Token to be invalid. Defaults to Depends(oauth2_scheme).

    Returns:
        str: The removed Token
    """
    invalid_tokens.add_token(token=token)
    return token


async def get_current_user(db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserLogin:
    """Get the current user from a JWT

    Args:
        db_session (Session, optional): Session to the Database. Defaults to Depends(get_db).
        token (str, optional): JTW - Otherwise it takes it from /token. Defaults to Depends(oauth2_scheme).

    Raises:
        NotAuthorizedException: Exception if the the Token or the Data is invalid

    Returns:
        UserLogin: Logged in User from the Databse
    """
    credentials_exception = exceptions.NotAuthorizedException(error_msg="Not authorized")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception from JWTError
    user = get_user_by_mail(db_session, token_data.username)
    if user is None or invalid_tokens.is_invalid(token):
        raise credentials_exception
    return UserLogin.from_orm(user)
