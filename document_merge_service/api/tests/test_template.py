import io

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from docx import Document
from lxml import etree
from rest_framework import status

from .. import models
from .data import django_file


@pytest.mark.parametrize(
    "template__group,group_access_only,size",
    [(None, False, 1), ("admin", True, 1), ("unknown", True, 0), ("unknown", False, 1)],
)
def test_template_list_group_access(
    db, admin_client, template, snapshot, size, group_access_only, settings
):
    settings.GROUP_ACCESS_ONLY = group_access_only
    url = reverse("template-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == size


@pytest.mark.parametrize("template__description", ["test description"])
@pytest.mark.parametrize(
    "query_params,size",
    [
        ({"description__icontains": "test"}, 1),
        ({"description__search": "test"}, 1),
        ({"description__icontains": "unknown"}, 0),
        ({"description__search": "unknown"}, 0),
    ],
)
def test_template_list_query_params(
    db, admin_client, template, snapshot, size, query_params
):
    url = reverse("template-list")

    response = admin_client.get(url, data=query_params)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == size


def test_template_detail(db, client, template):
    url = reverse("template-detail", args=[template.pk])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "template_name,status_code,group,require_authentication,authenticated",
    [
        ("docx-template.docx", status.HTTP_201_CREATED, None, False, False),
        ("docx-template.docx", status.HTTP_201_CREATED, None, True, True),
        ("docx-template.docx", status.HTTP_401_UNAUTHORIZED, None, True, False),
        ("docx-template.docx", status.HTTP_400_BAD_REQUEST, "unknown", True, True),
        ("docx-template.docx", status.HTTP_201_CREATED, "admin", True, True),
        ("test.txt", status.HTTP_400_BAD_REQUEST, None, False, False),
    ],
)
def test_template_create(
    db,
    client,
    admin_client,
    template_name,
    status_code,
    group,
    require_authentication,
    settings,
    authenticated,
):
    if authenticated:
        client = admin_client

    settings.REQUIRE_AUTHENTICATION = require_authentication
    url = reverse("template-list")

    template_file = django_file(template_name)
    data = {
        "slug": "test-slug",
        "template": template_file.file,
        "engine": models.Template.DOCX_TEMPLATE,
    }
    if group:
        data["group"] = group
    response = client.post(url, data=data, format="multipart")
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        data = response.json()
        template_link = data["template"]
        response = client.get(template_link)
        assert response.status_code == status.HTTP_200_OK
        Document(io.BytesIO(response.content))


@pytest.mark.parametrize(
    "template_name,status_code",
    [
        ("docx-template.docx", status.HTTP_200_OK),
        ("test.txt", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_template_update(db, client, template, template_name, status_code):
    url = reverse("template-detail", args=[template.pk])

    template_file = django_file(template_name)
    data = {"description": "Test description", "template": template_file.file}
    response = client.patch(url, data=data, format="multipart")
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        template.refresh_from_db()
        assert template.description == "Test description"


def test_template_destroy(db, client, template):
    url = reverse("template-detail", args=[template.pk])

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    "template__slug,template__engine,template__template",
    [
        (
            "TestNameTemplate",
            models.Template.DOCX_TEMPLATE,
            django_file("docx-template.docx"),
        ),
        (
            "TestNameMailMerge",
            models.Template.DOCX_MAILMERGE,
            django_file("docx-mailmerge.docx"),
        ),
    ],
)
def test_template_merge_docx(db, client, template, snapshot):
    url = reverse("template-merge", args=[template.pk])

    response = client.post(url, data={"data": {"test": "Test input"}}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert (
        response._headers["content-type"][1]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    docx = Document(io.BytesIO(response.content))
    xml = etree.tostring(docx._element.body, encoding="unicode", pretty_print=True)
    try:
        snapshot.assert_match(xml)
    except AssertionError:  # pragma: no cover
        with open(f"/tmp/{template.slug}.docx", "wb") as output:
            output.write(response.content)
        print("Template output changed. Check file at %s" % output.name)
        raise


# This needs a strange parametrization. If `unoconv_local` is in a separate
# `parametrize()`, the template filename in the second test will be appended with a
# hash and the test fails
@pytest.mark.parametrize(
    "template__engine,template__template,unoconv_local",
    [
        (models.Template.DOCX_TEMPLATE, django_file("docx-template.docx"), True),
        (models.Template.DOCX_TEMPLATE, django_file("docx-template.docx"), False),
    ],
)
def test_template_merge_as_pdf(db, settings, unoconv_local, client, template):
    settings.UNOCONV_LOCAL = unoconv_local
    settings.UNOCONV_URL = "" if unoconv_local else "http://unoconv:3000"
    url = reverse("template-merge", args=[template.pk])

    response = client.post(
        url, data={"data": {"test": "Test input"}, "convert": "pdf"}, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response["Content-Type"] == "application/pdf"
    assert f"{template.pk}.pdf" in response["Content-Disposition"]
    assert response.content[0:4] == b"%PDF"


@pytest.mark.parametrize(
    "template__engine,template__template",
    [(models.Template.DOCX_TEMPLATE, django_file("docx-template.docx"))],
)
def test_template_merge_as_pdf_without_unoconv(db, client, template, settings):
    settings.UNOCONV_URL = None
    url = reverse("template-merge", args=[template.pk])

    with pytest.raises(ImproperlyConfigured):
        client.post(
            url, data={"data": {"test": "Test input"}, "convert": "pdf"}, format="json"
        )


@pytest.mark.parametrize(
    "template__engine,template__template",
    [(models.Template.DOCX_TEMPLATE, django_file("docx-template-loopcontrols.docx"))],
)
def test_template_merge_jinja_extensions_docx(db, client, template, settings, snapshot):
    settings.DOCXTEMPLATE_JINJA_EXTENSIONS = ["jinja2.ext.loopcontrols"]

    url = reverse("template-merge", args=[template.pk])

    response = client.post(url, data={"data": {"test": "Test input"}}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert (
        response._headers["content-type"][1]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    docx = Document(io.BytesIO(response.content))
    xml = etree.tostring(docx._element.body, encoding="unicode", pretty_print=True)
    snapshot.assert_match(xml)


@pytest.mark.parametrize(
    "template__engine,template__template",
    [(models.Template.DOCX_TEMPLATE, django_file("docx-template-filters.docx"))],
)
def test_template_merge_jinja_filters_docx(db, client, template, snapshot, settings):
    settings.LANGUAGE_CODE = "de-ch"
    url = reverse("template-merge", args=[template.pk])

    data = {
        "data": {
            "test_date": "1984-09-15",
            "test_time": "23:24",
            "test_datetime": "1984-09-15 23:23",
            "test_datetime2": "23:23-1984-09-15",
            "test_none": None,
        }
    }

    response = client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert (
        response._headers["content-type"][1]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    docx = Document(io.BytesIO(response.content))
    xml = etree.tostring(docx._element.body, encoding="unicode", pretty_print=True)
    snapshot.assert_match(xml)
