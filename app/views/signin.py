"""Router and Logic for Login and Registration Pages"""
from datetime import timedelta
from typing import Optional

import fastapi
from fastapi import Depends
from fastapi import Response
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.crud.user import create_user
from db.crud.user import delete_user
from db.database import get_db
from schemes import exceptions
from schemes.scheme_user import User
from schemes.scheme_user import UserCreate
from schemes.scheme_user import UserLogin
from tools import security
from tools.config import settings
from tools.my_logging import logger
from tools.security import get_current_user
from tools.security import oauth2_scheme

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.post("/token", response_model=security.Token)
async def login_for_access_token(
    response: Response, db_session: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """Generate token for user

    Args:
        response (Response): the http response
        db_session (Session, optional): the db session. Defaults to Depends(get_db).
        form_data (OAuth2PasswordRequestForm, optional): the data of the login form. Defaults to Depends().

    Raises:
        exceptions.NotAuthorizedException: wrong login exception

    Returns:
        access_token: access token for user
    """
    user = security.authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise exceptions.NotAuthorizedException(error_msg="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/signin/", response_class=HTMLResponse)
def signin(request: Request, error: Optional[str] = ""):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
        error (Optional[str], optional): the error message. Defaults to "".

    Returns:
        TemplateResponse: the http response
    """
    return templates.TemplateResponse("signin/signin.html", {"request": request, "error": error})


@router.post("/signin/", response_class=RedirectResponse)
async def login(request: Request, url: Optional[str] = None, db_session: Session = Depends(get_db)):
    """Login Form to login the user and redirect if valid

    Args:
        request (Request): the http request
        url (Optional[str], optional): url for redirect. Defaults to None.
        db_session (Session, optional): the db session. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: redirect to /signin/ or /signin/... or /main/
    """
    if not url:
        url = "/main"
    form = security.LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            url = url.replace("%26", "&")
            response = RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
            await login_for_access_token(response=response, form_data=form, db_session=db_session)
            return response
        except exceptions.NotAuthorizedException:
            url = url.replace("&", "%26")
            form.__dict__.update(msg="")
            form.error = "Incorrect Email or Password"
            return RedirectResponse(
                url=f"/signin/?error=Wrong Email or Password&url={url}", status_code=status.HTTP_302_FOUND
            )
    return RedirectResponse(url="/signin/", status_code=status.HTTP_302_FOUND)


@router.get("/signout/", response_class=RedirectResponse)
async def signout(token: str = Depends(oauth2_scheme)):
    """Logout the user and redirect to the main page

    Args:
        token (str, optional): the authentification token. Defaults to Depends(oauth2_scheme).

    Returns:
        RedirectResponse: redirect to /main/
    """
    await security.invalid_access_token(token=token)
    return RedirectResponse(url="/main", status_code=status.HTTP_302_FOUND)


@router.get("/register/", response_class=HTMLResponse)
def register(request: Request):
    """Return the rendered template for the register page

    Args:
        request (Request): Requerd for Template

    Returns:
        TemplateResponse: the http response
    """

    # read terms of service and privacy policy from text files
    tosstring = "Terms of Service is Missing"
    privstring = "Privacy Policy is Missing"

    try:
        with open("static/text/privacy.txt", "r", encoding="utf-8") as privfile:
            privstring = privfile.read()
        with open("static/text/tos.txt", "r", encoding="utf-8") as tosfile:
            tosstring = tosfile.read()

    except Exception as e:
        print(e)

    legal = {"tos": tosstring, "privacy": privstring}

    data = {"request": request, "legal": legal}
    return templates.TemplateResponse("signin/register.html", data)


@router.post("/register/", response_class=RedirectResponse)
async def register_post(request: Request, db_session: Session = Depends(get_db)):
    """Register Form to register the user and redirect if valid

    Args:
        request (Request): the http request
        db_session (Session, optional): the db session. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: redirect to /accresp/?success=...
    """
    form = await request.form()
    email = form.get("emailInput")
    password = form.get("passwordInput")

    try:
        user = UserCreate(email=email, password=password)
        create_user(db=db_session, person=user)
        return RedirectResponse("/accresp/?success=True", status_code=status.HTTP_302_FOUND)
    except exceptions.DuplicateEntry:
        logger.warning("User %s already exist in the Database", email)
        return RedirectResponse(
            "/accresp/?success=False&msg=User mit der email gibt es bereits", status_code=status.HTTP_302_FOUND
        )
    except exceptions.DatabaseException:
        return RedirectResponse(
            "/accresp/?success=False&msg=Probleme mit der Datenbank", status_code=status.HTTP_302_FOUND
        )


@router.get("/accresp/", response_class=HTMLResponse)
def account_response(request: Request, msg: Optional[str] = "", success: Optional[str] = ""):
    """Return a response page for account creation, either positive or negative

    Args:
        request (Request): the http request
        msg (Optional[str], optional): the error msg. Defaults to "".
        success (Optional[str], optional): the succes boolean. Defaults to "".

    Returns:
        TemplateResponse: the http response
    """
    data = {"request": request, "msg": msg, "success": success}
    return templates.TemplateResponse("signin/accresponse.html", data)


@router.get("/recover/", response_class=HTMLResponse)
def recover(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template

    Returns:
        TemplateResponse: the http response
    """
    return templates.TemplateResponse("signin/recover.html", {"request": request})


@router.get("/pwreset/", response_class=HTMLResponse)
def pwreset(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template

    Returns:
        TemplateResponse: the http response
    """
    return templates.TemplateResponse("signin/pwreset.html", {"request": request})


@router.get("/pwchange/", response_class=HTMLResponse)
def pwchange(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template

    Returns:
        TemplateResponse: the http response
    """
    return templates.TemplateResponse("signin/pwchange.html", {"request": request})


@router.post("/delete/", status_code=200, response_model=User)
def delete_singined_user(
    request: Request, current_user: UserLogin = Depends(get_current_user), db_session: Session = Depends(get_db)
) -> User:
    """Delete the current logged in user

    Args:
        request (Request): The Request
        current_user (UserLogin, optional): Current logged in User. Defaults to Depends(get_current_user).
        db_session (Session, optional): Session to the Database. Defaults to Depends(get_db).

    Returns:
        RedirectResponse: Redirect to the landingpage
    """
    user = User(email=current_user.email, last_login=current_user.last_login)
    delete_user(db=db_session, user=user)
    return user
