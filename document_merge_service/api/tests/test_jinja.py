import pytest

from ..jinja import dateformat, datetimeformat, emptystring, timeformat


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
