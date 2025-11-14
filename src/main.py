from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from todo.router import route as todo_router
from auth.router import route as auth_router


app = FastAPI(title="To-Do Application", description="A simple to-do application using FastAPI and Jinja2", version="1.0.0")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Jinja2 templates
templates= Jinja2Templates(directory="../templates")




@app.get("/",tags=["root"])
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request":request,"current_page":"home"}) 


app.include_router(todo_router)
app.include_router(auth_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)