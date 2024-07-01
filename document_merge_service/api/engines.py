import io
import re
import zipfile
from collections.abc import Mapping

import openpyxl
import xltpl.writerx as writerx
from docx import Document
from docxtpl import DocxTemplate
from jinja2.exceptions import TemplateSyntaxError
from mailmerge import MailMerge
from rest_framework import exceptions

from document_merge_service.api.data import django_file

from . import models
from .jinja import get_jinja_env, get_jinja_filters


class _MagicPlaceholder(str, Mapping):  # type: ignore
    def __new__(cls, parent=None, name=None):
        self = str.__new__(cls, name if name else "")
        self._parent = parent
        self._reports = parent._reports if parent else set()

        if self != "":
            self._reports.add(self)
        return self

    @property
    def reports(self):
        return list(self._reports)

    def __iter__(self):
        return (x for x in [_MagicPlaceholder(parent=self, name=f"{self}[]")])

    def __getitem__(self, idx):
        assert isinstance(idx, str)
        return _MagicPlaceholder(parent=self, name=f"{self}.{idx}".strip("."))

    def __getattr__(self, attr):
        return _MagicPlaceholder(parent=self, name=f"{self}.{attr}".strip("."))

    def __len__(self):
        return 2

    def __radd__(self, other):
        return str(self) + str(other)


class DocxValidator:
    def _validate_is_docx(self):
        try:
            Document(self.template)
        except (ValueError, zipfile.BadZipfile):
            raise exceptions.ParseError("not a valid docx file")
        finally:
            self.template.seek(0)

    def validate_template_syntax(self, available_placeholders=None):  # pragma: no cover
        raise NotImplementedError(
            "validate_template_syntax must be implemented in engine class"
        )

    def validate(self, available_placeholders=None, sample_data=None):
        self._validate_is_docx()
        self.validate_template_syntax(available_placeholders, sample_data)

    def validate_available_placeholders(
        self, used_placeholders, available_placeholders
    ):
        # We don't validate available_placeholders if it's not given
        if not available_placeholders:
            return

        available_placeholders = self._normalize_available_placeholders(
            available_placeholders
        )

        referenced_unavailable = "; ".join(
            sorted(set(used_placeholders) - set(available_placeholders))
        )
        if referenced_unavailable:
            raise exceptions.ValidationError(
                f"Template uses unavailable placeholders: {referenced_unavailable}"
            )

    def _normalize_available_placeholders(self, placeholders):
        available_placeholders = set(placeholders)
        # add all prefixes of placeholders, so users don't
        # have to add "foo" if they have "foo.bar" in the list
        for ph in placeholders:
            prefix = ""
            for word in ph.split("."):
                prefix = f"{prefix}.{word}" if prefix else word
                if prefix.endswith("[]"):
                    available_placeholders.add(prefix[:-2])
                available_placeholders.add(prefix)
        return available_placeholders


class DocxTemplateEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def _extract_image_placeholders(self, doc):
        """Extract placeholders using the image filter.

        This method extracts all placeholder names that use the image filter so
        we can add a dummy image to the sample data for validation. We
        explicitly need to parse headers and footers as well as the actual
        document body.
        """

        body_xml = doc.get_xml()
        body_xml = doc.patch_xml(body_xml)

        xmls = [body_xml]

        for _, part in [
            *doc.get_headers_footers(doc.HEADER_URI),
            *doc.get_headers_footers(doc.FOOTER_URI),
        ]:
            part_xml = doc.get_part_xml(part)
            part_xml = doc.patch_xml(part_xml)
            xmls.append(part_xml)

        images = set()

        for xml in xmls:
            image_match = re.match(r".*{{\s?(\S*)\s?\|\s?image\(.*", xml)
            matches = image_match.groups() if image_match else []
            images.update(matches)

        return images

    def validate_template_syntax(self, available_placeholders=None, sample_data=None):
        try:
            doc = DocxTemplate(self.template)
            root = _MagicPlaceholder()
            env = get_jinja_env()
            ph = {
                name: root[name] for name in doc.get_undeclared_template_variables(env)
            }

            for image in self._extract_image_placeholders(doc):
                cleaned_image = image.strip('"').strip("'")
                ph[root[cleaned_image]] = django_file("black.png").file

            ph["_tpl"] = doc

            doc.render(ph, env)

            if sample_data:
                sample_data["_tpl"] = doc
                doc.render(sample_data, env)

            self.validate_available_placeholders(
                used_placeholders=root.reports,
                available_placeholders=available_placeholders,
            )

        except TemplateSyntaxError as exc:
            arg_str = ";".join(exc.args)
            raise exceptions.ValidationError(f"Syntax error in template: {arg_str}")

        finally:
            self.template.seek(0)

    def merge(self, data, buf):
        doc = DocxTemplate(self.template)
        data["_tpl"] = doc

        doc.render(data, get_jinja_env(), autoescape=True)
        doc.save(buf)
        return buf


class DocxMailmergeEngine(DocxValidator):
    def __init__(self, template):
        self.template = template

    def _get_placeholders(self, document):
        return [
            field.attrib.get("name")
            for part in document.parts.values()
            for field in part["part"].findall(".//MergeField")
        ]

    def validate_template_syntax(self, available_placeholders=None, sample_data=None):
        document = MailMerge(self.template)
        # syntax can't be invalid as it's validated by office
        # suites. However we need to have *some* placeholders
        self.template.seek(0)
        used_placeholders = self._get_placeholders(document)
        self.validate_available_placeholders(
            used_placeholders=used_placeholders,
            available_placeholders=available_placeholders,
        )

        if sample_data:
            buffer = io.BytesIO()
            self.merge(sample_data, buffer)
            self.template.seek(0)

        if not len(used_placeholders):
            raise exceptions.ValidationError("Template has no merge fields")

    def merge(self, data, buf):
        with MailMerge(self.template) as document:
            document.merge(**data)
            document.write(buf)
            return buf


_placeholder_match = re.compile(r"^\s*{{\s*([^{}]+)\s*}}\s*$")


class XlsxTemplateEngine:
    BUILTIN_VARS = [
        "tpl_name",
        "sheet_name",
        "[]",
        "sheet_name.decode",
    ]

    def __init__(self, template):
        self.template = template
        self.writer = None

    def validate_is_xlsx(self):
        try:
            openpyxl.load_workbook(self.template)
        except (ValueError, zipfile.BadZipfile):
            raise exceptions.ParseError("not a valid xlsx file")

    def validate(self, available_placeholders=None, sample_data=None):
        self.validate_is_xlsx()
        self.validate_template_syntax(available_placeholders, sample_data)

    def _expand_available_placeholders(self, ph_list):
        """Expand available placeholder list for (internal) correctness.

        If client gives "foo[].bar", we implicitly also allow "foo[]" and "foo":

        >>> self._expand_available_placeholders(["foo[].bar", "baz.boo"])
        ["foo[]", "foo[].bar", "baz.boo"]
        """
        out_list = []
        for ph in ph_list:
            pieces = ph.split(".")
            for offset in range(len(pieces)):
                prefixed = ".".join(pieces[:offset])
                out_list.append(prefixed)
                if prefixed.endswith("[]"):
                    out_list.append(prefixed[:-2])
            out_list.append(ph)
        return out_list

    def validate_template_syntax(self, available_placeholders=None, sample_data=None):
        # We cannot use jinja to validate because xltpl uses jinja's lexer directly
        magic = None
        if not sample_data:
            sample_data = magic = _MagicPlaceholder()
        buf = io.BytesIO()

        try:
            self.merge(sample_data, buf, is_test_merge=True)
        except TemplateSyntaxError as exc:
            arg_str = ";".join(exc.args)
            raise exceptions.ValidationError(f"Syntax error in template: {arg_str}")

        if available_placeholders and magic is not None:
            missing_set = (
                set(magic.reports)
                - set(self._expand_available_placeholders(available_placeholders))
                - set(self.BUILTIN_VARS)
            )
            if not missing_set:
                return

            missing = "; ".join(missing_set)
            raise exceptions.ValidationError(
                f"Placeholders used in template, but not available: {missing}"
            )

    def merge(self, data, buf, is_test_merge=False):
        self.writer = writer = writerx.BookWriter(self.template)
        self._current_data = data

        writer.jinja_env.filters.update(get_jinja_filters())
        if is_test_merge:
            writer.jinja_env.undefined = self._undefined_factory
        writer.jinja_env.globals.update(dir=dir, getattr=getattr)

        payloads = []
        sheets = writer.sheet_resource_map.sheet_state_list
        for sheet in sheets:
            new = dict(data)
            new["sheet_name"] = sheet.name
            new["tpl_name"] = sheet.name
            payloads.append(new)
        writer.render_book(payloads=payloads)
        writer.save(buf)
        return buf

    def _undefined_factory(self, name):
        # For test merges, we set a custom "undefined" factory that
        # doesn't really do undefined, but just fetches the right value
        # from our magic placeholder structure
        return self._current_data[name]


ENGINES = {
    models.Template.DOCX_TEMPLATE: DocxTemplateEngine,
    models.Template.DOCX_MAILMERGE: DocxMailmergeEngine,
    models.Template.XLSX_TEMPLATE: XlsxTemplateEngine,
}


def get_engine(engine, template):
    return ENGINES[engine](template)
