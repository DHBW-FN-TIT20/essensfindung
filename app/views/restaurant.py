"""Router for the Home of the Website"""
import fastapi
from db.database import get_db
from fastapi import Depends
from fastapi.responses import HTMLResponse
from schemes import Allergies
from schemes import Cuisine
from schemes import scheme_filter
from schemes import scheme_rest
from schemes.scheme_user import UserBase
from services import service_res
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from typing import Union
from typing import List

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/findrestaurant", response_class=HTMLResponse)
async def findrestaurant(
    request: Request,
    cuisine: str,
    rating: int,
    costs: float,
    radius: int,
    lat: str,
    lng: str,
    allergies: Union[Allergies, None]=None,
    db_session: Session = Depends(get_db)
):
    #cuisine:str zum Cuisine-Array machen
    rest_filter = scheme_filter.FilterRest(
        cuisine=cuisine,
        allergies=allergies,
        rating=rating,
        costs=costs,
        radius=radius * 1000,
        location=scheme_rest.LocationBase(lat=lat, lng=lng),
    )
    mock_user = UserBase(email="example@gmx.de")
    # api.Search_restaurant(...)
    restaurant = service_res.search_for_restaurant(db_session=db_session, user=mock_user, user_f=rest_filter)
    # restaurant = scheme_rest.Restaurant(
    #     place_id="PlaceID",
    #     name="Alpha",
    #     geometry=scheme_rest.Geometry(location=scheme_rest.LocationRest(lat="47.7007", lng="9.562", adr=cuisine)),
    #     maps_url="https://maps.google.com/?cid=10544281732087259755",
    #     rating=4.0,
    #     own_rating=costs,
    #     phone_number="07541",
    #     homepage="http://www.alpha-fn.de/",
    # )
    return templates.TemplateResponse(
        "restaurant/restaurant_result.html", {"request": request, "restaurant": restaurant}
    )
