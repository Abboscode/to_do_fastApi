from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
router = APIRouter()

templates= Jinja2Templates(directory="templates")
data=[{"id":1,"task":"Do laundry"},{"id":2,"task":"Read a book"},{"id":3,"task":"Write code"},{"id":4,"task":"Go for a walk"},{"id":5,"task":"Cook dinner"}]

@router.get("/",response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("todo.html", {"request":request ,"todos":data})