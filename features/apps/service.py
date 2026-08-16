from .repository import app_repository


def get_apps(): return app_repository.get_all()
def create_app(data): return app_repository.insert(data)
def update_app(app_id, data): return app_repository.update(app_id, data)
def delete_app(app_id): return app_repository.delete(app_id)
