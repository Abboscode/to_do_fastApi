from fastapi import APIRouter, Request
from .constants import PATH_TO_AUTH_TEMPLATES
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
route = APIRouter(prefix="/auth", tags=["auth"])
tempalates = Jinja2Templates(directory=str(PATH_TO_AUTH_TEMPLATES))
#sign in page
@route.get("/signIn",response_class=HTMLResponse)
async def read_auth(request: Request):
        return tempalates.TemplateResponse("auth.html",{"request":request,"current_page":"signIn"})@route.get("/signIn",response_class=HTMLResponse)

@route.get("/signOut",response_class=HTMLResponse)
async def read_auth(request: Request):
        return tempalates.TemplateResponse("auth.html",{"request":request,"current_page":"signOut"})