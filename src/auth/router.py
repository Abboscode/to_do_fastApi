from fastapi import APIRouter, Request
from .constants import PATH_TO_AUTH_TEMPLATES
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
route = APIRouter(prefix="/auth", tags=["auth"])
tempalates = Jinja2Templates(directory=str(PATH_TO_AUTH_TEMPLATES))
#sign in page
@route.get("/auth",response_class=HTMLResponse)
async def read_auth(request: Request):
        return tempalates.TemplateResponse("auth.html",{"request":request})