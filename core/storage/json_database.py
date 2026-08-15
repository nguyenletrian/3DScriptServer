import json


class JsonDatabase:

    def __init__(self, database_path):
        self.database_path = database_path

    def _get_path(self, collection):
        return (
            self.database_path
            / f"{collection}.json"
        )

    def _load(self, collection):

        path = self._get_path(collection)

        if not path.exists():
            return []

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def _save(self, collection, data):

        path = self._get_path(collection)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    def get(self, collection, item_id):

        data = self._load(collection)

        for item in data:

            if item["id"] == item_id:
                return item

        return None

    def get_all(self, collection):

        return self._load(collection)

    def insert(self, collection, data):

        items = self._load(collection)

        if items:
            data["id"] = max(
                item["id"]
                for item in items
            ) + 1
        else:
            data["id"] = 1

        items.append(data)

        self._save(
            collection,
            items
        )

        return data

    def update(
        self,
        collection,
        item_id,
        data
    ):

        items = self._load(collection)

        for item in items:

            if item["id"] == item_id:

                item.update(data)

                self._save(
                    collection,
                    items
                )

                return item

        return None

    def delete(
        self,
        collection,
        item_id
    ):

        items = self._load(collection)

        for item in items:

            if item["id"] == item_id:

                items.remove(item)

                self._save(
                    collection,
                    items
                )

                return True

        return False