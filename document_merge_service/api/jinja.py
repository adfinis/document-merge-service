import magic
from babel.dates import format_date, format_datetime, format_time
from dateutil.parser import parse
from django.conf import settings
from django.utils.translation import to_locale
from docx.shared import Mm
from docxtpl import Listing
from jinja2 import pass_context
from jinja2.sandbox import SandboxedEnvironment
from PIL import Image
from rest_framework.exceptions import ValidationError

from document_merge_service.third_party.docxtpl import InlineImage


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


def create_image_filter(doc_instance):
    """
    Bins the 'doc' instance safely inside a Python closure.

    The template engine never sees the 'doc_instance' variable.
    """

    @pass_context
    def image(ctx, img_name, width=None, height=None, keep_aspect_ratio=False):
        if img_name not in ctx:
            raise ValidationError(f'No file for image "{img_name}" provided!')

        img = ctx.get(img_name)

        if not img:
            # Fallback to no image
            return

        img.seek(0)  # needed in case image is referenced multiple times
        if magic.from_buffer(img.read(), mime=True) not in ["image/png", "image/jpeg"]:
            raise ValidationError("Only png and jpg images are supported!")

        width = Mm(width) if width else None
        height = Mm(height) if height else None

        if width and height and keep_aspect_ratio:
            w, h = Image.open(img).size
            width, height = get_size_with_aspect_ratio(width, height, w / h)

        return InlineImage(doc_instance, img, width=width, height=height)

    return image


def get_jinja_filters(doc):
    return {
        "date": dateformat,
        "datetime": datetimeformat,
        "time": timeformat,
        "emptystring": emptystring,
        "getwithdefault": getwithdefault,
        "multiline": multiline,
        "image": create_image_filter(doc),
    }


def get_jinja_env(doc):
    jinja_env = SandboxedEnvironment(extensions=settings.DOCXTEMPLATE_JINJA_EXTENSIONS)
    jinja_env.filters.update(get_jinja_filters(doc))
    return jinja_env


def get_size_with_aspect_ratio(width, height, aspect_ratio):
    tpl_aspect_ratio = width / height

    if tpl_aspect_ratio >= aspect_ratio:
        width = height * aspect_ratio
    else:
        height = width / aspect_ratio

    return width, height
