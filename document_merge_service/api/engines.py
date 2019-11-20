import zipfile
from functools import singledispatch

from docx import Document
from docxtpl import DocxTemplate, Listing
from mailmerge import MailMerge
from rest_framework import exceptions

from . import models
from .jinja import get_jinja_env


class DocxValidator:
    def validate(self):
        try:
            Document(self.template)
        except (ValueError, zipfile.BadZipfile):
            raise exceptions.ParseError("not a valid docx file")

        self.template.seek(0)


@singledispatch
def apply_nested(data, fn):
    """Apply fn to every primitive value in nested data."""
    return fn(data)


@apply_nested.register(dict)
def _(data, fn):
    return {key: apply_nested(value, fn) for (key, value) in data.items()}


@apply_nested.register(list)
def _(data, fn):
    return [apply_nested(value, fn) for value in data]


class DocxTemplateEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def merge(self, data, buf):
        def transform(value):
            """Transform value for multiline support."""
            if value is None:
                return None
            return Listing(value)

        data = apply_nested(data, transform)

        doc = DocxTemplate(self.template)

        doc.render(data, get_jinja_env())
        doc.save(buf)
        return buf


class DocxMailmergeEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def merge(self, data, buf):
        with MailMerge(self.template) as document:
            document.merge(**data)
            document.write(buf)
            return buf


ENGINES = {
    models.Template.DOCX_TEMPLATE: DocxTemplateEngine,
    models.Template.DOCX_MAILMERGE: DocxMailmergeEngine,
}


def get_engine(engine, template):
    return ENGINES[engine](template)
