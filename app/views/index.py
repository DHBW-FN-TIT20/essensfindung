"""Router for the Home of the Website"""
from re import U

import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.database import get_db
from schemes import Allergies
from schemes import Cuisine
from schemes import scheme_filter
from schemes import scheme_rest

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Return the renderd template for the /index.html

    Args:
        request (Request): Requerd for Template
    """
    # request filter of user
    # service_res.get_assessments_from_user(db, user=get_logged_in_user.email)
    rest_filter = scheme_filter.FilterRest(
        cuisine=Cuisine.ASIAN,
        allergies=Allergies.LACTOSE,
        rating=4,
        costs=2,
        radius=15000,
        location=scheme_rest.LocationBase(lat="47.7007", lng="9.562"),
    )
    return templates.TemplateResponse("index.html", {"request": request, "rest_filter": rest_filter})
