""" Logic for Login and Registration Pages """
import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()

@router.get("/signin/")
def signin(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
    """
    return templates.TemplateResponse("signin/signin.html", {"request": request})


@router.get("/register/")
def register(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
    """
    return templates.TemplateResponse("signin/register.html", {"request": request})