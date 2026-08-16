def format_thousands(value):
    if value in (None, ""):
        return value
    try:
        number = float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return value
    return f"{int(number):,}" if number.is_integer() else f"{number:,}"


def parse_number(value):
    if value in (None, ""):
        return value
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return value


FORMATTERS = {
    "thousands": format_thousands,
    "number": parse_number,
}


def get_formatter(name):
    return FORMATTERS.get(name)
