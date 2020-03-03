import zipfile

from docx import Document
from docxtpl import DocxTemplate
from jinja2.exceptions import TemplateSyntaxError
from mailmerge import MailMerge
from rest_framework import exceptions

from . import models
from .jinja import get_jinja_env


class DocxValidator:
    def _validate_is_docx(self):
        try:
            Document(self.template)
        except (ValueError, zipfile.BadZipfile):
            raise exceptions.ParseError("not a valid docx file")
        finally:
            self.template.seek(0)

    def validate_template_syntax(self):  # pragma: no cover
        raise NotImplementedError(
            "validate_template_syntax must be implemented in engine class"
        )

    def validate(self):
        self._validate_is_docx()
        self.validate_template_syntax()


class DocxTemplateEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def validate_template_syntax(self):
        try:
            doc = DocxTemplate(self.template)
            doc.render({"foo": "bar"})
        except TemplateSyntaxError as exc:
            arg_str = ";".join(exc.args)
            raise exceptions.ValidationError(f"Syntax error in template: {arg_str}")

        finally:
            self.template.seek(0)

    def merge(self, data, buf):
        doc = DocxTemplate(self.template)

        doc.render(data, get_jinja_env())
        doc.save(buf)
        return buf


class DocxMailmergeEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def _has_placeholders(self, part):
        return bool(part.findall("//MergeField"))

    def validate_template_syntax(self):
        document = MailMerge(self.template)
        # syntax can't be invalid as it's validated by office
        # suites. However we need to have *some* placeholders
        has_placeholders = any(
            self._has_placeholders(part) for part in document.parts.values()
        )
        self.template.seek(0)
        if not has_placeholders:
            raise exceptions.ValidationError("Template has no merge fields")

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
