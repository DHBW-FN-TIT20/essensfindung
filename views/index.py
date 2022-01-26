"""Router for the Home of the Website"""
from datetime import datetime
from schemes import scheme_filter, Cuisine, Allergies, scheme_rest

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
    #request filter of user
    rest_filter = scheme_filter.RestFilter(cuisine=Cuisine.ASIAN, allergies=Allergies.LACTOSE, rating=4, costs=2, radius=15000, location=scheme_rest.BaseLocation(lat="47.7007", lng="9.562"))
    return templates.TemplateResponse("index.html", {"request": request, "rest_filter": rest_filter})
