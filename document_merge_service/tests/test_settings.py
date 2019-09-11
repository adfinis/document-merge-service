import pytest
from django.core.exceptions import ImproperlyConfigured

from .. import settings


def test_get_unoconv_formats():
    formats = settings.get_unoconv_formats()
    assert "pdf" in formats


def test_get_unoconv_formats_invalid_format(monkeypatch):
    monkeypatch.setattr(settings, "UNOCONV_ALLOWED_TYPES", ["invalid"])

    with pytest.raises(ImproperlyConfigured):
        settings.get_unoconv_formats()
