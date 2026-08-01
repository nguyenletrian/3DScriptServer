from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from routers import users
from routers import auth

app = FastAPI()

templates = Jinja2Templates(directory="templates")


app.include_router(users.router)
app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )