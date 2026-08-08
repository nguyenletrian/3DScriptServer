from fastapi.templating import Jinja2Templates
from core.config import settings

templates = Jinja2Templates(
    directory=settings.TEMPLATE_DIR
)