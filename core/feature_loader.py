import importlib
import importlib.util
import pkgutil

import features


def load_routers():
    for item in pkgutil.iter_modules(features.__path__):
        module_name = f"features.{item.name}.router"
        if importlib.util.find_spec(module_name) is None:
            continue
        yield importlib.import_module(module_name).router
