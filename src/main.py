# main.py

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Assuming these files and models exist in your project structure:
from todo.router import route as todo_router
from auth.router import route as auth_router
from todo.models import Base, TodoModel 


# --------------------
## ⚙️ Application Setup
# --------------------

app = FastAPI(title="To-Do Application", 
               description="A simple to-do application using FastAPI and Jinja2", 
               version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="../templates")


# --------------------
## 💾 Database Configuration
# --------------------

# Configure asynchronous database engine
enginer = create_async_engine("sqlite+aiosqlite:///./database/todolist.db", echo=True)

# Create a sessionmaker factory
new_session_maker = async_sessionmaker(bind=enginer, expire_on_commit=False)

# Dependency to provide a database session
async def get_session():
    """Provides a fresh asynchronous session for each request."""
    async with new_session_maker() as session:
        yield session

# --------------------
## 🚀 Database Initialization and Seeding
# --------------------

@app.post("/initdb", tags=["database"])
async def init_models():
    """Drops all tables, creates all tables, and seeds default data."""
    
    # 1. TRANSACTION FOR SCHEMA MANAGEMENT (DROP/CREATE)
    async with enginer.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    # 2. TRANSACTION FOR DATA MANIPULATION (SEEDING)
    async with new_session_maker() as session:
        default_todos = [
            TodoModel(
                title= "Complete project proposal",
                description="Write and submit the Q4 project proposal to the team",
                dateAdded= "2024-11-10",
                completed= False,
            ),
            TodoModel(
                title= "Buy groceries",
                description= "Bear, eggs, bread, and vegetables",
                dateAdded= "2024-11-12",
                completed= True,
            ),
        ]
        
        session.add_all(default_todos)
        await session.commit()
        
    return {"message": "Database initialized and seeded"}

# --------------------
## 🌐 Routing
# --------------------

@app.get("/", tags=["root"])
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "current_page": "home"}) 

app.include_router(todo_router)
app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn
    # Make sure to run this file with the correct module path if necessary
    uvicorn.run(app, host="localhost", port=8000)