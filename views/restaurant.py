"""Router for the Home of the Website"""
import enum
from datetime import datetime

import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.database import get_db
from schemes import scheme_rest
from services import service_res

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/findrestaurant")
async def findrestaurant(request: Request, rest_name: str, costs: float, cuisine: str, db: Session = Depends(get_db)):
    # api.Search_restaurant(...)
    # service_res.get_assessments_from_user(db, user=Us)
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
