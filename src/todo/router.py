from fastapi import APIRouter, Request
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.encoders import jsonable_encoder
route = APIRouter(prefix="/todos", tags=["todos"])
data=[ {
      "id": 1,
      "title": "Complete project proposal",
      "description": "Write and submit the Q4 project proposal to the team",
      "dateAdded": "2024-11-10",
      "completed": False,
    },
    {
      "id": 2,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread, and vegetables",
      "dateAdded": "2024-11-12",
      "completed": True,
    },]
# 1. Start from the current file (router.py)
router_file_path = Path(__file__).resolve()

# 2. Get the project root directory by going up 3 levels:
#    router.py -> todo/ -> src/ -> project_folder/
project_root = router_file_path.parent.parent.parent 

# 3. Define the templates path
templates_dir = project_root / "templates"

# 4. Initialize Jinja2Templates
templates = Jinja2Templates(directory=str(templates_dir))
json_data=jsonable_encoder(data)

@route.get("/",response_class=HTMLResponse)
async def read_root(request: Request):
        return JSONResponse(content=json_data)