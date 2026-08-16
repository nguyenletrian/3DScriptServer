import importlib
from pathlib import Path


FEATURES_PATH = Path(__file__).resolve().parent.parent / "features"


def load_routers():
    for path in sorted(FEATURES_PATH.iterdir()):
        if not path.is_dir() or not (path / "router.py").exists():
            continue
        yield importlib.import_module(f"features.{path.name}.router").router
