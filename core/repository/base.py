from core.storage import db


class BaseRepository:
    def __init__(self, collection): self.collection = collection
    def get(self, item_id): return db.get(self.collection, item_id)
    def get_all(self): return db.get_all(self.collection)
    def insert(self, data): return db.insert(self.collection, data)
    def update(self, item_id, data): return db.update(self.collection, item_id, data)
    def delete(self, item_id): return db.delete(self.collection, item_id)
    def find_one(self, **conditions): return next((item for item in self.get_all() if all(item.get(k) == v for k, v in conditions.items())), None)
