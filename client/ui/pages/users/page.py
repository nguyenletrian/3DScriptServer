from ...builders.page_builder import PageBuilder


PAGE_CONFIG = {
    "title": "Users",
    "data": {
        "loader": "load",
    },
    "list": {
        "columns": [
            {"name": "id", "label": "ID"},
            {"name": "username", "label": "Username"},
            {"name": "role", "label": "Role"},
        ],
    },
}


class UsersPage(PageBuilder):

    def __init__(self):
        super().__init__(PAGE_CONFIG)
