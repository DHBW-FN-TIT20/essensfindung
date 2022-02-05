"""Router for the Home of the Website"""
import fastapi
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

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
    rest_filter = scheme_filter.FilterRest(
        cuisines=[Cuisine.ASIAN],
        allergies=[Allergies.LACTOSE],
        rating=4,
        costs=2,
        radius=15000,
        location=scheme_rest.LocationBase(lat="47.7007", lng="9.562"),
    )
    return templates.TemplateResponse("index.html", {"request": request, "rest_filter": rest_filter})


@router.get("/landing/", response_class=HTMLResponse)
def index(request: Request):
    """Return landing page for new users"""

    return templates.TemplateResponse("landing.html", {"request": request})
