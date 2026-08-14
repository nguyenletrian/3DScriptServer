from .repository import AppRepository

app_repository = AppRepository()
def get_apps():
    return app_repository.get_all()