import requests

http = requests.Session()
_current_user = None


def set_user(user):
    global _current_user
    _current_user = user


def get_user():
    return _current_user


def clear_user():
    global _current_user
    _current_user = None


def get_http_session():
    return http