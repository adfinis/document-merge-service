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
    "template__slug,template__engine", [("test-slug", models.Template.DOCX_TEMPLATE)]
)
def test_template_list(db, client, template, snapshot):
    url = reverse("template-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


def test_template_detail(db, client, template):
    url = reverse("template-detail", args=[template.pk])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "template_name,status_code",
    [
        ("docx-template.docx", status.HTTP_201_CREATED),
        ("test.txt", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_template_create(db, client, template_name, status_code):
    url = reverse("template-list")

    template_file = django_file(template_name)
    data = {
        "slug": "test-slug",
        "template": template_file.file,
        "engine": models.Template.DOCX_TEMPLATE,
    }
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

    docx = Document(io.BytesIO(response.content))
    xml = etree.tostring(docx._element.body, encoding="unicode", pretty_print=True)
    try:
        snapshot.assert_match(xml)
    except AssertionError:  # pragma: no cover
        with open(f"/tmp/{template.slug}.docx", "wb") as output:
            output.write(response.content)
        print("Template output changed. Check file at %s" % output.name)
        raise


@pytest.mark.parametrize(
    "template__engine,template__template",
    [(models.Template.DOCX_TEMPLATE, django_file("docx-template.docx"))],
)
def test_template_merge_as_pdf(db, client, template):
    url = reverse("template-merge", args=[template.pk])

    response = client.post(
        url, data={"data": {"test": "Test input"}, "convert": "pdf"}, format="json"
    )
    assert response.status_code == status.HTTP_200_OK


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
