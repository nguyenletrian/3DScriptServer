import importlib
import pkgutil

import features


def load_routers():
    for item in pkgutil.iter_modules(features.__path__):
        try:
            router = importlib.import_module(f"features.{item.name}.router").router
        except (ModuleNotFoundError, AttributeError):
            continue
        yield router
