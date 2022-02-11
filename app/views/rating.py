import fastapi
from fastapi import Depends
from fastapi import status
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from schemes.scheme_rest import RestBewertungCreate
from schemes.scheme_rest import RestaurantBase
from db.database import get_db
from sqlalchemy.orm import Session
from tools.security import get_current_user
from schemes.scheme_user import User
from db.models.bewertung import Bewertung
from db.crud.bewertung import get_bewertung_from_user_to_rest, update_bewertung
from services import service_res
from copy import copy

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/rating", response_class=HTMLResponse)
def rating(
    request: Request,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rest_ratings = service_res.get_assessments_from_user(db_session=db_session, user=current_user)

    return templates.TemplateResponse(
        "rating/rating.html", {"request": request, "rest_ratings": rest_ratings}
    )


@router.get("/rating/edit", response_class=HTMLResponse)
def edit_rating(request: Request, place_id: str, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rest_ratings = service_res.get_assessments_from_user(db_session=db_session, user=current_user)
    rest_rating = [r for r in rest_ratings if r.place_id == place_id]
    return templates.TemplateResponse(
        "rating/rating_edit.html", {"request": request, "rest_rating": rest_rating[0]}
    )


@router.post("/rating/edit", response_class=RedirectResponse)
async def edit_rating(request: Request, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    form = await request.form()
    rating = form.get("rating_edit_rating_target")
    notes = form.get("rating_notes")
    name = form.get("rest_name")
    identifier = form.get("identifier")

    old_rating = get_bewertung_from_user_to_rest(db=db_session, user=current_user, rest=RestaurantBase(place_id=identifier, name=name))
    old_rating_scheme = RestBewertungCreate(name=name, comment=old_rating.kommentar, rating=old_rating.rating,
                                            person=current_user, restaurant=RestaurantBase(place_id=identifier, name=name))
    new_rating = copy(old_rating_scheme)
    new_rating.comment = notes
    new_rating.rating = rating

    service_res.update_assessment(db_session=db_session, old_assessment=old_rating_scheme, new_assessment=new_rating)
    return RedirectResponse("/rating/", status_code=status.HTTP_302_FOUND)

@router.get("/rating/delete", response_class=RedirectResponse)
def delete_rating(request: Request, place_id:str, rest_name:str, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service_res.delete_assessment(db_session=db_session, user=current_user, rest=RestaurantBase(place_id=place_id, name=rest_name))
    return RedirectResponse("/rating/", status_code=status.HTTP_302_FOUND)
