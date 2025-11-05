import io
import json

import pytest
from django.http.multipartparser import MultiPartParser
from django.urls import reverse
from rest_framework import status

from document_merge_service.api.data import django_file


def parse_httpx_request(request):
    return MultiPartParser(
        {
            "CONTENT_TYPE": request.headers["content-type"],
            "CONTENT_LENGTH": request.headers["content-length"],
        },
        io.BytesIO(request.content),
        [],
        "utf-8",
    ).parse()


@pytest.fixture
def gotenberg_url(settings):
    return f"{settings.GOTENBERG_URL}/forms/libreoffice/convert"


@pytest.mark.freeze_time("2026-01-16 14:43")
@pytest.mark.parametrize("with_options", [True, False])
@pytest.mark.parametrize(
    "filename,target_filename",
    [
        ("docx-template.docx", "docx-template.pdf"),
        ("2023.test.test.docx-template.docx", "2023.test.test.docx-template.pdf"),
    ],
)
def test_convert(
    db,
    client,
    filename,
    gotenberg_url,
    httpx_mock,
    target_filename,
    settings,
    with_options,
):
    if with_options:
        settings.GOTENBERG_PDF_METADATA = {
            "author": "custom-test",
            "creator": "override!",
        }
        settings.GOTENBERG_PDF_A_FORMAT = "A2b"
        settings.GOTENBERG_PDF_UA = True
        settings.GOTENBERG_PDF_FLATTEN = True

    httpx_mock.add_response(
        method="POST",
        url=gotenberg_url,
        status_code=status.HTTP_200_OK,
        content=django_file("test-pdf.pdf"),
    )

    response = client.post(
        reverse("convert"),
        data={"file": django_file(filename).file, "target_format": "pdf"},
        format="multipart",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("Content-Type") == "application/pdf"
    assert (
        response.headers.get("Content-Disposition")
        == f'attachment; filename="{target_filename}"'
    )

    data, _ = parse_httpx_request(httpx_mock.get_request())
    data = data.dict()
    metadata = json.loads(data["metadata"])

    if with_options:
        assert metadata == {
            "CreationDate": "2026-01-16T14:43:00+00:00",
            "Creator": "override!",
            "ModDate": "2026-01-16T14:43:00+00:00",
            "Author": "custom-test",
        }
        assert data["pdfa"] == "PDF/A-2b"
        assert data["pdfua"] == "true"
        assert data["flatten"] == "true"
    else:
        assert metadata == {
            "CreationDate": "2026-01-16T14:43:00+00:00",
            "Creator": "document-merge-service",
            "ModDate": "2026-01-16T14:43:00+00:00",
        }
        assert "pdfa" not in data
        assert data["pdfua"] == "false"
        assert data["flatten"] == "false"


def test_incorrect_file_type(db, client):
    url = reverse("convert")
    file_to_convert = django_file("invalid-template.xlsx")

    data = {"file": file_to_convert.file, "target_format": "pdf"}
    response = client.post(url, data=data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_gotenberg_error(db, client, httpx_mock, settings):
    httpx_mock.add_response(
        method="POST",
        url=f"{settings.GOTENBERG_HOST}:{settings.GOTENBERG_PORT}/forms/libreoffice/convert",
        status_code=status.HTTP_502_BAD_GATEWAY,
    )

    response = client.post(
        reverse("convert"),
        data={"file": django_file("docx-template.docx").file, "target_format": "pdf"},
        format="multipart",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
