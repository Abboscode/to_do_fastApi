from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends,Request
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from  .models import TodoModel
from datetime import datetime as Data
from .schemas import TodoCreate

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
      
SessionDep=Annotated[AsyncSession,Depends(get_session)]

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

@route.post("/add")
async def add_tddo(data:TodoCreate,session: AsyncSession = Depends(get_session)):
        
         
        new_todo=TodoModel(
            title=data.title,
            dateAdded=Data.now().strftime("%Y-%m-%d %H:%M:%S"),
            description=data.description,
            completed=data.completed
        )
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)

        return new_todo

      



@route.delete("/delete/{todo_id}")
async def delete_todo(todo_id:int,session:SessionDep)-> JSONResponse:
        # 1. Construct the DELETE statement
        # We use sqlalchemy.delete() with .where()
        stmt=delete(TodoModel).where(TodoModel.id==todo_id)
       # 2. Execute the statement
       # session.execute() returns a Result object
        result=await session.execute(stmt)
        
    
    # 3. Commit the transaction to apply the changes
        await session.commit()
        delete_todo=result.rowcount

        if delete_todo==0:
            # If no rows were deleted, the todo item was not found
        # Raising an HTTPException is the standard FastAPI way for errors
            raise HTTPException(
            status_code=404, 
            detail=f"Todo with ID {todo_id} not found"
        )
        
    # 5. If successful (rows_deleted > 0), return a success message
        return JSONResponse(
        content={"message": f"Todo with ID {todo_id} successfully deleted"},
        status_code=200
    )