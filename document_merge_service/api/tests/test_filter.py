from document_merge_service.api.jinja import dateformat, datetimeformat, emptystring


def test_filter_date():
    plain = "2019-12-31"
    formatted = dateformat(plain)
    assert formatted == "31.12.2019"


def test_filter_date_none():
    plain = None
    formatted = dateformat(plain)
    assert formatted == ""


def test_filter_datetime():
    plain = "2019-12-31 23:59"
    formatted = datetimeformat(plain)
    assert formatted == "23:59 31.12.2019"


def test_filter_datetime_none():
    plain = None
    formatted = datetimeformat(plain)
    assert formatted == ""


def test_filter_emptystring():
    plain = "Lorem ipsum"
    formatted = emptystring(plain)
    assert formatted == plain


def test_filter_emptystring_none():
    plain = None
    formatted = emptystring(plain)
    assert formatted == ""
