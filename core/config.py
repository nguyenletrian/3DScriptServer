from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
class Settings:
    APP_NAME = "ConnectVBS"
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    TEMPLATE_DIR = BASE_DIR / "core" / "templates"
    DATABASE_PATH = BASE_DIR / "database"


settings = Settings()