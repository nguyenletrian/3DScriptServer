from core.database import db


class BaseRepository:

    collection = None

    def get(self, item_id):
        return db.get(
            self.collection,
            item_id
        )

    def get_all(self):
        return db.get_all(
            self.collection
        )

    def insert(self, data):
        return db.insert(
            self.collection,
            data
        )

    def update(self, item_id, data):
        return db.update(
            self.collection,
            item_id,
            data
        )

    def delete(self, item_id):
        return db.delete(
            self.collection,
            item_id
        )
    
    def find_one(self, **conditions):
        items = self.get_all()
        for item in items:
            if all(
                item.get(key) == value
                for key, value in conditions.items()
            ):
                return item
        return None