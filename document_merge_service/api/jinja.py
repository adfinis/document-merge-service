import imghdr

from babel.dates import format_date, format_datetime, format_time
from dateutil.parser import parse
from django.conf import settings
from django.utils.translation import to_locale
from docx.shared import Mm
from docxtpl import InlineImage, Listing
from jinja2 import Environment, contextfilter
from rest_framework.exceptions import ValidationError


def parse_string(value):
    return parse(str(value))


def dateformat(value, format="medium", locale=None):
    if value is None:
        return ""

    if locale is None:
        locale = to_locale(settings.LANGUAGE_CODE)

    parsed_value = parse_string(value)
    return format_date(parsed_value, format, locale=locale)


def datetimeformat(value, format="medium", locale=None):
    if value is None:
        return ""

    if locale is None:
        locale = to_locale(settings.LANGUAGE_CODE)

    parsed_value = parse_string(value)
    return format_datetime(parsed_value, format, locale=locale)


def timeformat(value, format="medium", locale=None):
    if value is None:
        return ""

    if locale is None:
        locale = to_locale(settings.LANGUAGE_CODE)

    parsed_value = parse_string(value)
    return format_time(parsed_value, format, locale=locale)


def emptystring(value):
    if value is None:
        return ""
    return value


def getwithdefault(value, default=""):
    if value is None:
        return default
    return value


def multiline(value):
    return Listing(value)


@contextfilter
def image(ctx, img_name, width=None, height=None):
    tpl = ctx["_tpl"]

    if img_name not in ctx:
        raise ValidationError(f'No file for image "{img_name}" provided!')

    img = ctx.get(img_name)

    if not img:
        # Fallback to no image
        return

    img.seek(0)  # needed in case image is referenced multiple times
    if imghdr.what(img) not in ["png", "jpg", "jpeg"]:
        raise ValidationError("Only png and jpg images are supported!")

    width = Mm(width) if width else None
    height = Mm(height) if height else None
    return InlineImage(tpl, img, width=width, height=height)


def get_jinja_env():
    jinja_env = Environment(extensions=settings.DOCXTEMPLATE_JINJA_EXTENSIONS)
    jinja_env.filters["date"] = dateformat
    jinja_env.filters["datetime"] = datetimeformat
    jinja_env.filters["time"] = timeformat
    jinja_env.filters["emptystring"] = emptystring
    jinja_env.filters["getwithdefault"] = getwithdefault
    jinja_env.filters["multiline"] = multiline
    jinja_env.filters["image"] = image
    return jinja_env
