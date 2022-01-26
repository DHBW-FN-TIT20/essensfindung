"""Router for the Home of the Website"""
from datetime import datetime
from schemes import scheme_rest
import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()

@router.get("/findrestaurant")
async def findrestaurant(request: Request, rest_name: str, costs : float):
    #api.Search_restaurant(...)
    restaurant = scheme_rest.Restaurant(place_id="PlaceID", name=rest_name, geometry=scheme_rest.Geometry(location=scheme_rest.ResLocation(lat="47.7007", lng="9.562", adr="Restaurantstraße 5")),
    maps_url="https://maps.google.com/?cid=10544281732087259755", rating=4.0, own_rating=3, phone_number="07541", homepage="http://www.alpha-fn.de/")
    return templates.TemplateResponse("restaurant/restaurant_result.html", {"request": request, "restaurant": restaurant})