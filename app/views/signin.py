""" Logic for Login and Registration Pages """
from datetime import timedelta

import fastapi
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.database import get_db
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/signin/", response_class=HTMLResponse)
def signin(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
    """
    return templates.TemplateResponse("signin/signin.html", {"request": request})


@router.post("/signin/", response_class=HTMLResponse)
async def login(request: Request, db_session: Session = Depends(get_db)):
    form = security.LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("signin/signin.html", form.__dict__)
            await login_for_access_token(response=response, form_data=form, db_session=db_session)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("signin/signin.html", form.__dict__)
    return templates.TemplateResponse("signin/signin.html", form.__dict__)


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
            privstring = "".join(privfile.readlines())
        with open("static/text/tos.txt", "r", encoding="utf-8") as tosfile:
            tosstring = "".join(tosfile.readlines())

    except Exception as e:
        print(e)

    legal = {"tos": tosstring, "privacy": privstring}

    return templates.TemplateResponse("signin/register.html", {"request": request, "legal": legal})


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
