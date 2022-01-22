"""Router for the Home of the Website"""
from datetime import datetime
import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()

@router.get("/findrestaurant/")
async def findrestaurant(request: Request, test1: int):
    neu=test1+1
    return templates.TemplateResponse("home/search.html", {"request": request, "neu": neu})