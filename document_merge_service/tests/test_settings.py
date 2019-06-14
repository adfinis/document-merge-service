import pytest
from django.core.exceptions import ImproperlyConfigured

from .. import settings


@pytest.mark.parametrize(
    "format_function", ["get_unoconv_formats", "get_unoconv_formats_local"]
)
def test_get_unoconv_formats(format_function):
    formats = getattr(settings, format_function)()
    assert "pdf" in formats


def test_get_unoconv_formats_invalid_url(monkeypatch):
    monkeypatch.setattr(settings, "UNOCONV_URL", settings.UNOCONV_URL + "/invalid")

    with pytest.raises(ImproperlyConfigured):
        settings.get_unoconv_formats()


@pytest.mark.parametrize(
    "format_function", ["get_unoconv_formats", "get_unoconv_formats_local"]
)
def test_get_unoconv_formats_invalid_format(monkeypatch, format_function):
    monkeypatch.setattr(settings, "UNOCONV_ALLOWED_TYPES", ["invalid"])

    with pytest.raises(ImproperlyConfigured):
        getattr(settings, format_function)()
