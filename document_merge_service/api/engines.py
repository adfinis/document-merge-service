import zipfile

import jinja2
from django.conf import settings
from docx import Document
from docxtpl import DocxTemplate
from mailmerge import MailMerge
from rest_framework import exceptions

from . import models

# Custom filters
import jinja2
from datetime import datetime
def dateformat(value, format='%d.%m.%Y'):
    if value is None:
        return ""
    else:
        return datetime.strptime(value, "%Y-%m-%d").strftime(format)
def datetimeformat(value, in_format='%H:%M %Y-%m-%d', out_format='%H:%M %d.%m.%Y'):
    if value is None:
        return ""
    else:
        return datetime.strptime(value, in_format).strftime(out_format)
def emptystring(value):
    if value is None:
        return ""
    else:
        return value
jinja_env = jinja2.Environment()
jinja_env.filters['date'] = dateformat
jinja_env.filters['emptystring'] = emptystring
# /Custom filters

class DocxValidator:
    def validate(self):
        try:
            Document(self.template)
        except (ValueError, zipfile.BadZipfile):
            raise exceptions.ParseError("not a valid docx file")

        self.template.seek(0)


class DocxTemplateEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def merge(self, data, buf):
        doc = DocxTemplate(self.template)
        jinja_env = jinja2.Environment(
            extensions=settings.DOCXTEMPLATE_JINJA_EXTENSIONS
        )
        doc.render(data, jinja_env)
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
