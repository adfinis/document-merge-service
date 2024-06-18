import pytest
from docx.shared import Mm

from document_merge_service.api.data import django_file

from ..jinja import (
    dateformat,
    datetimeformat,
    emptystring,
    getwithdefault,
    image,
    timeformat,
)


@pytest.mark.parametrize(
    "inp,locale,expected", [("2019-12-31", "de_CH", "31.12.2019"), (None, "de_CH", "")]
)
def test_dateformat(inp, expected, locale):
    formatted = dateformat(inp, locale=locale)
    assert formatted == expected


@pytest.mark.parametrize(
    "inp,locale,expected",
    [("2019-12-31 23:59", "de_CH", "31.12.2019, 23:59:00"), (None, "de_CH", "")],
)
def test_datetimeformat(inp, expected, locale):
    formatted = datetimeformat(inp, locale=locale)
    assert formatted == expected


@pytest.mark.parametrize(
    "inp,locale,expected", [("23:59", "de_CH", "23:59:00"), (None, "de_CH", "")]
)
def test_timeformat(inp, expected, locale):
    formatted = timeformat(inp, locale=locale)
    assert formatted == expected


@pytest.mark.parametrize("inp,expected", [("text", "text"), (None, "")])
def test_emptystring(inp, expected):
    formatted = emptystring(inp)
    assert formatted == expected


@pytest.mark.parametrize(
    "inp,default,expected",
    [("text", "", "text"), (None, "", ""), (None, "something", "something")],
)
def test_getwithdefault(inp, default, expected):
    formatted = getwithdefault(inp, default=default)
    assert formatted == expected


@pytest.mark.parametrize(
    "width,height,keep_aspect_ratio,expected_size",
    [
        (20, 10, False, (20, 10)),
        (20, 10, True, (10, 10)),
        (10, 20, True, (10, 10)),
        (10, None, False, (10, None)),
        (None, 10, False, (None, 10)),
        (10, None, True, (10, None)),
        (None, 10, True, (None, 10)),
    ],
)
def test_image(width, height, keep_aspect_ratio, expected_size):
    # The size of "black.png" is 32x32 pixels which is an aspect ratio of 1
    inline_image = image(
        {"_tpl": None, "black.png": django_file("black.png").file},
        "black.png",
        width,
        height,
        keep_aspect_ratio,
    )

    w, h = expected_size

    assert inline_image.width == (Mm(w) if w else None)
    assert inline_image.height == (Mm(h) if h else None)
