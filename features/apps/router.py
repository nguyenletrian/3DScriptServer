from core.crud import crud_router
from .config import CONFIG

router = crud_router(CONFIG)
