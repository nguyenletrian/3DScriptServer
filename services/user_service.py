import json


def load_users():
    with open("database/users.json", "r") as file:
        return json.load(file)


def save_users(users):
    with open("database/users.json", "w") as file:
        json.dump(users, file, indent=4)


def find_user(username):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return user
    return None