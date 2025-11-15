from fastapi import APIRouter, Depends,Request
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from  .models import TodoModel

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
json_data = []


#get all todos from database

# Configure asynchronous database engine
enginer = create_async_engine("sqlite+aiosqlite:///./database/todolist.db", echo=True)

# Create a sessionmaker factory
new_session_maker = async_sessionmaker(bind=enginer, expire_on_commit=False)
async def get_session():
    """Provides a fresh asynchronous session for each request."""
    async with new_session_maker() as session:
        yield session
      


@route.get("/todos")
async def read_todos(
    # Inject the session dependency
    session: AsyncSession = Depends(get_session)
):
    """Fetches and returns all To-Do items as JSON."""
  
    # 1. Fetch the ORM objects
    stmt = select(TodoModel)
    result = await session.scalars(stmt)
    todos_list = result.all() 
    
    # 2. Use jsonable_encoder to convert the list of ORM objects 
    #    into JSON-compatible dictionaries.
    json_data = jsonable_encoder(todos_list)
    
    # 3. Return the JSON-compatible data
    return json_data

@route.post("/add",response_class=HTMLResponse)
async def add_tddo(request: Request):
        return JSONResponse(content={"message":"Todo created successfully"})

      
@route.get("/todos/{todo_id}",response_class=HTMLResponse)
async def read_todo(request: Request,todo_id:int):
        for todo in data:
            if todo["id"]==todo_id:
                return JSONResponse(content=jsonable_encoder(todo))
        return JSONResponse(content={"message":"Todo not found"},status_code=404)