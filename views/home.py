"""Router for the Home of the Website"""
from datetime import datetime

import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/")
def index(request: Request):
    """Return the renderd template for the /index.html

    Args:
        request (Request): Requerd for Template
    """
    some_data_day = datetime.today().day
    return templates.TemplateResponse("home/index.html", {"request": request, "day": some_data_day})
