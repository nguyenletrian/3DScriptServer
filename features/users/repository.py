from core.repository import BaseRepository


class UserRepository(BaseRepository):

    collection = "users"

    def find_by_username(self, username):

        users = self.get_all()

        for user in users:

            if user["username"] == username:
                return user

        return None


user_repository = UserRepository()