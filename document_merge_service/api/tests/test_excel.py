import io

import openpyxl
import pytest
from rest_framework import exceptions

from ..data import django_file
from ..engines import XlsxTemplateEngine

_structure = {
    "key0": "xdata0",
    "key1": {
        "subkey1": "xdata1",
    },
    "key2": [
        "mixed",
        "list",
        {"subkey2": "xdata2"},
    ],
}

_available = ["key0", "key1.subkey1"]


def test_structure():
    tmpl = django_file("xlsx-structure.xlsx")
    engine = XlsxTemplateEngine(tmpl)
    buf = io.BytesIO()
    engine.merge(_structure, buf)
    buf.seek(0)
    doc = openpyxl.load_workbook(buf)
    for ws in doc.worksheets:
        assert ws["A1"].value == "xdata0"
        assert ws["A2"].value == "xdata1"
        assert ws["A5"].value == "Item: mixed"
        assert ws["A6"].value == "Item: list"
        assert ws["A7"].value == "Subitem: xdata2"
    engine.validate(_available, _structure)
    _available.append("huhu")
    with pytest.raises(exceptions.ValidationError):
        engine.validate(_available, _structure)


def test_syntax_error():
    tmpl = django_file("xlsx-syntax.xlsx")
    engine = XlsxTemplateEngine(tmpl)
    with pytest.raises(exceptions.ValidationError):
        engine.validate(_available, _structure)


def test_valid_error():
    tmpl = django_file("xlsx-not-valid.xlsx")
    engine = XlsxTemplateEngine(tmpl)
    with pytest.raises(exceptions.ParseError):
        engine.validate(_available, _structure)
