""" Logic for Login and Registration Pages """
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
from db.database import get_db
from schemes import exceptions
from schemes.scheme_user import UserCreate
from tools import security
from tools.config import settings

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.post("/token", response_model=security.Token)
async def login_for_access_token(
    response: Response, db_session: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
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
    """
    return templates.TemplateResponse("signin/signin.html", {"request": request, "error": error})


@router.post("/signin/", response_class=RedirectResponse)
async def login(request: Request, url: Optional[str] = None, db_session: Session = Depends(get_db)):
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


@router.get("/register/", response_class=HTMLResponse)
def register(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
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
    form = await request.form()
    email = form.get("emailInput")
    password = form.get("passwordInput")

    try:
        user = UserCreate(email=email, password=password)
        create_user(db=db_session, person=user)
        return RedirectResponse("/accresp/?success=True", status_code=status.HTTP_302_FOUND)
    except exceptions.DuplicateEntry:
        return RedirectResponse(
            "/accresp/?success=False&msg=User mit der email gibt es bereits", status_code=status.HTTP_302_FOUND
        )
    except exceptions.DatabaseException:
        return RedirectResponse(
            "/accresp/?success=False&msg=Probleme mit der Datenbank", status_code=status.HTTP_302_FOUND
        )


@router.get("/accresp/", response_class=HTMLResponse)
def account_response(request: Request, msg: Optional[str] = "", success: Optional[str] = ""):
    """Return a response page for account creation, either positive or negative"""
    data = {"request": request, "msg": msg, "success": success}
    return templates.TemplateResponse("signin/accresponse.html", data)



@router.get("/recover/", response_class=HTMLResponse)
def recover(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
    """
    return templates.TemplateResponse("signin/recover.html", {"request": request})


@router.get("/pwreset/", response_class=HTMLResponse)
def pwreset(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
    """
    return templates.TemplateResponse("signin/pwreset.html", {"request": request})


@router.get("/pwchange/", response_class=HTMLResponse)
def pwchange(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
    """
    return templates.TemplateResponse("signin/pwchange.html", {"request": request})
