from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from core.config import settings
from core.feature_loader import load_routers

app = FastAPI(title=settings.APP_NAME)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
templates = Jinja2Templates(directory="templates")

for router in load_routers(): app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request): return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
def health(): return {"status": "ok"}
