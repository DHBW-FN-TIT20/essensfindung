""" Logic for Login and Registration Pages """
import fastapi
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/signin/", response_class=HTMLResponse)
def signin(request: Request):
    """Return the rendered template for the login page

    Args:
        request (Request): Requerd for Template
    """
    return templates.TemplateResponse("signin/signin.html", {"request": request})


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