"""Router for the Home of the Website"""
import enum

import fastapi
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from schemes import scheme_rest

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/findrestaurant", response_class=HTMLResponse)
async def findrestaurant(request: Request, rest_name: str, costs: float, cuisine: str):
    # api.Search_restaurant(...)
    restaurant = scheme_rest.Restaurant(
        place_id="PlaceID",
        name=rest_name,
        geometry=scheme_rest.Geometry(location=scheme_rest.LocationRest(lat="47.7007", lng="9.562", adr=cuisine)),
        maps_url="https://maps.google.com/?cid=10544281732087259755",
        rating=4.0,
        own_rating=costs,
        phone_number="07541",
        homepage="http://www.alpha-fn.de/",
    )
    return templates.TemplateResponse(
        "restaurant/restaurant_result.html", {"request": request, "restaurant": restaurant}
    )
