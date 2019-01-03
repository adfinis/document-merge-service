import io
import zipfile

from docx import Document
from docxtpl import DocxTemplate
from mailmerge import MailMerge
from rest_framework import exceptions

from . import models


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

    def merge(self, data):
        doc = DocxTemplate(self.template)
        doc.render(data)
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)

        return buf


class DocxMailmergeEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def merge(self, data):
        with MailMerge(self.template) as document:
            document.merge(**data)
            buf = io.BytesIO()
            document.write(buf)
            buf.seek(0)
            return buf


ENGINES = {
    models.Template.DOCX_TEMPLATE: DocxTemplateEngine,
    models.Template.DOCX_MAILMERGE: DocxMailmergeEngine,
}


def get_engine(engine, template):
    return ENGINES[engine](template)
