from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from core.config import settings
from features.users.router import router as users_router
from features.auth.router import router as auth_router
from features.dashboard.router import router as dashboard_router
from features.apps.router import router as apps_router

app = FastAPI(title=settings.APP_NAME)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
templates = Jinja2Templates(directory="templates")

for router in (users_router, auth_router, dashboard_router, apps_router): app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request): return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
def health(): return {"status": "ok"}
