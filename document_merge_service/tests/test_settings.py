import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from ..api.unoconv import Unoconv


def test_get_unoconv_formats():
    uno = Unoconv(pythonpath=settings.UNOCONV_PYTHON, unoconvpath=settings.UNOCONV_PATH)
    formats = uno.get_formats()
    assert "pdf" in formats


def test_get_unoconv_formats_invalid_format(monkeypatch):
    monkeypatch.setattr(settings, "UNOCONV_ALLOWED_TYPES", ["invalid"])
    uno = Unoconv(pythonpath=settings.UNOCONV_PYTHON, unoconvpath=settings.UNOCONV_PATH)

    with pytest.raises(ImproperlyConfigured):
        uno.get_formats()
