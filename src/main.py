from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from todo.router import router as todo_router
app = FastAPI(title="To-Do Application", description="A simple to-do application using FastAPI and Jinja2", version="1.0.0")
templates= Jinja2Templates(directory="templates")
data=[{"id":1,"task":"Do laundry"},{"id":2,"task":"Read a book"},{"id":3,"task":"Write code"},{"id":4,"task":"Go for a walk"},{"id":5,"task":"Cook dinner"}]

@app.get("/",tags=["root"])
async def read_root(request: Request):
    return ({"message": "Welcome to the To-Do Application!"})

app.include_router(todo_router.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)