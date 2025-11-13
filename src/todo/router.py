from fastapi import APIRouter, Request
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
route = APIRouter(prefix="/todos", tags=["todos"])

# 1. Start from the current file (router.py)
router_file_path = Path(__file__).resolve()

# 2. Get the project root directory by going up 3 levels:
#    router.py -> todo/ -> src/ -> project_folder/
project_root = router_file_path.parent.parent.parent 

# 3. Define the templates path
templates_dir = project_root / "templates"

# 4. Initialize Jinja2Templates
templates = Jinja2Templates(directory=str(templates_dir))
data=[{"id":1,"task":"Do laundry"},{"id":2,"task":"Read a book"},{"id":3,"task":"Write code"},{"id":4,"task":"Go for a walk"},{"id":5,"task":"Cook dinner"}]

@route.get("/",response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("todo.html", {"request":request ,"todos":data})