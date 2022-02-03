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

    #read terms of service and privacy policy from text files
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
        
    return templates.TemplateResponse("signin/register.html",{"request": request, "legal": legal})