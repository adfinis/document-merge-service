from datetime import datetime

from django.conf import settings
from jinja2 import Environment


def dateformat(value, format="%d.%m.%Y"):
    if value is None:
        return ""
    else:
        return datetime.strptime(value, "%Y-%m-%d").strftime(format)


def datetimeformat(value, in_format="%Y-%m-%d %H:%M", out_format="%H:%M %d.%m.%Y"):
    if value is None:
        return ""
    else:
        return datetime.strptime(value, in_format).strftime(out_format)


def emptystring(value):
    if value is None:
        return ""
    else:
        return value


def get_jinja_env():
    jinja_env = Environment(extensions=settings.DOCXTEMPLATE_JINJA_EXTENSIONS)
    jinja_env.filters["date"] = dateformat
    jinja_env.filters["datetime"] = datetimeformat
    jinja_env.filters["emptystring"] = emptystring
    return jinja_env
