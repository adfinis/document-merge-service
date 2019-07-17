from babel.dates import format_date, format_datetime, format_time
from dateutil.parser import parse
from django.conf import settings
from django.utils.translation import to_locale
from jinja2 import Environment


def dateformat(value, format="medium", locale=None):
    if value is None:
        return ""

    if locale is None:
        locale = to_locale(settings.LANGUAGE_CODE)

    parsed_value = parse(value)
    return format_date(parsed_value, format, locale=locale)


def datetimeformat(value, format="medium", locale=None):
    if value is None:
        return ""

    if locale is None:
        locale = to_locale(settings.LANGUAGE_CODE)

    parsed_value = parse(value)
    return format_datetime(parsed_value, format, locale=locale)


def timeformat(value, format="medium", locale=None):
    if value is None:
        return ""

    if locale is None:
        locale = to_locale(settings.LANGUAGE_CODE)

    parsed_value = parse(value)
    return format_time(parsed_value, format, locale=locale)


def emptystring(value):
    if value is None:
        return ""
    return value


def get_jinja_env():
    jinja_env = Environment(extensions=settings.DOCXTEMPLATE_JINJA_EXTENSIONS)
    jinja_env.filters["date"] = dateformat
    jinja_env.filters["datetime"] = datetimeformat
    jinja_env.filters["time"] = timeformat
    jinja_env.filters["emptystring"] = emptystring
    return jinja_env
