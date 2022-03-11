"""Router and logic for the rating of the Website"""
from copy import copy
from typing import Optional

import fastapi
from fastapi import Depends
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.crud.restBewertung import get_bewertung_from_user_to_rest
from db.crud.recipeBewertung import get_bewertung_from_user_to_recipe
from db.database import get_db
from schemes.scheme_rest import RestaurantBase
from schemes.scheme_recipe import RecipeBase
from schemes.scheme_rest import RestBewertungCreate
from schemes.scheme_recipe import RecipeBewertungCreate
from schemes.scheme_user import User
from services import service_res
from services import service_rec
from tools.security import get_current_user

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/rating", response_class=HTMLResponse)
def rating(request: Request, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all ratings of user

    Args:
        request (Request): the http request
        db_session (Session, optional): the db session. Defaults to Depends(get_db).
        current_user (User, optional): the current user. Defaults to Depends(get_current_user).

    Returns:
        TemplateResponse: the http response
    """
    res_ratings = service_res.get_assessments_from_user(db_session=db_session, user=current_user)
    rec_ratings = service_rec.get_assessments_from_user(db_session=db_session, user=current_user)

    return templates.TemplateResponse("rating/rating.html", {"request": request, "res_ratings": res_ratings, "rec_ratings": rec_ratings})


@router.get("/rating/edit", response_class=HTMLResponse)
def edit_rating(
    request: Request,
    id: str,
    type: str,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return the rendered template for displaying rating that matches place_id for editing

    Args:
        request (Request): Request for template
        id (str): identifier for either a restaurant or a recipe
        db_session (Session, optional): current db_session. Defaults to Depends(get_db).
        current_user (User, optional): current logged in user. Defaults to Depends(get_current_user).

    Returns:
        HTMLResponse: rendered template
        HTTPRedicrect: redirect to error page if type is invalid
    """
    if type == "Restaurant":
        rest_ratings = service_res.get_assessments_from_user(db_session=db_session, user=current_user)
        rest_rating = [r for r in rest_ratings if r.place_id == id]
        return templates.TemplateResponse("rating/rating_edit.html", {"request": request, "type": "Restaurant", "rating": rest_rating[0]})
    elif type == "Recipe":
        rec_ratings = service_rec.get_assessments_from_user(db_session=db_session, user=current_user)
        rec_rating = [r for r in rec_ratings if r.id == id]
        return templates.TemplateResponse("rating/rating_edit.html", {"request": request, "type": "Recipe", "rating": rec_rating[0]})
    else:
        response = RedirectResponse(url="/error?msg=Invalid type of rating", status_code=status.HTTP_302_FOUND)
        return response


@router.post("/rating/edit", response_class=RedirectResponse)
async def edit_rating_post(
    request: Request, db_session: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Save rating of user

    Args:
        request (Request): the http request
        db_session (Session, optional): the db session. Defaults to Depends(get_db).
        current_user (User, optional): the current user. Defaults to Depends(get_current_user).

    Returns:
        RedirectResponse: redirect to .../rating/
    """
    form = await request.form()
    rating_type = form.get("type")
    rating = form.get("rating_edit_rating_target")
    notes = form.get("rating_notes")
    name = form.get("rest_name")
    identifier = form.get("identifier")

    if rating_type == "Restaurant":
        old_rating = get_bewertung_from_user_to_rest(
            db=db_session, user=current_user, rest=RestaurantBase(place_id=identifier, name=name)
        )
        old_rating_scheme = RestBewertungCreate(
            name=name,
            comment=old_rating.kommentar,
            rating=old_rating.rating,
            person=current_user,
            restaurant=RestaurantBase(place_id=identifier, name=name),
        )
        new_rating = copy(old_rating_scheme)
        new_rating.comment = notes
        new_rating.rating = rating

        service_res.update_assessment(db_session=db_session, old_assessment=old_rating_scheme, new_assessment=new_rating)

    elif rating_type == "Recipe": 
        old_rating = get_bewertung_from_user_to_recipe(
            db=db_session, user=current_user, recipe=RecipeBase(id=identifier)
        )
        old_rating_scheme = RecipeBewertungCreate(
            name=name,
            comment=old_rating.kommentar,
            rating=old_rating.rating,
            person=current_user,
            recipe=RecipeBase(id=identifier),
        )
        new_rating = copy(old_rating_scheme)
        new_rating.comment = notes
        new_rating.rating = rating

        service_rec.update_assessment(db_session=db_session, old_assessment=old_rating_scheme, new_assessment=new_rating)

    return RedirectResponse("/rating/", status_code=status.HTTP_302_FOUND)


@router.get("/rating/delete", response_class=RedirectResponse)
def delete_rating(
    request: Request,
    type: str,
    id: str,
    rest_name: Optional[str] = None,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete user rating

    Args:
        request (Request): the http request
        id (str): the recipe id or restaurant place_id
        rest_name (str): the restaurant name
        db_session (Session, optional): the db session. Defaults to Depends(get_db).
        current_user (User, optional): the current user. Defaults to Depends(get_current_user).

    Returns:
        RedirectResponse: redirect to /rating/
    """
    if type == "Restaurant":
        service_res.delete_assessment(
            db_session=db_session, user=current_user, rest=RestaurantBase(place_id=id, name=rest_name)
        )
    elif type == "Recipe":
        service_rec.delete_assessment(
            db_session=db_session, user=current_user, recipe=RecipeBase(id=id)
        )
    return RedirectResponse("/rating/", status_code=status.HTTP_302_FOUND)
