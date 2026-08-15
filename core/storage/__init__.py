from core.config import settings

from .json_database import JsonDatabase


db = JsonDatabase(
    settings.DATABASE_PATH
)