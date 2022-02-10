import fastapi
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()

