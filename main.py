from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from features.users.router import router as users_router
from features.auth.router import router as auth_router
from features.dashboard.router import router as dashboard_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="my_super_secret_key"
)

templates = Jinja2Templates(
    directory="templates"
)


app.include_router(
    users_router
)

app.include_router(
    auth_router
)

app.include_router(
    dashboard_router
)



@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/health")
def health():
    return {
        "status": "ok"
    }