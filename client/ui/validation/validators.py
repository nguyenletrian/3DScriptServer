import re


def validate_required(value):
    return value is not None and str(value).strip() != ""


def validate_username(value):
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", str(value)))


def validate_email(value):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(value)))


def validate_positive_int(value):
    try:
        return int(value) >= 0
    except (TypeError, ValueError):
        return False


VALIDATORS = {
    "username": validate_username,
    "email": validate_email,
    "positive_int": validate_positive_int,
}


def get_validator(name):
    return VALIDATORS.get(name)
