import pytest
from django.urls import reverse
from rest_framework import status

from document_merge_service.api.data import django_file


# @pytest.mark.parametrize("template__description", ["test description"])
@pytest.mark.parametrize(
    "target_format,response_content_type",
    [
        ("pdf", "application/pdf"),
    ],
)
def test_convert(db, client, template, target_format, response_content_type):
    url = reverse("convert")
    file_to_convert = django_file("docx-template-syntax.docx")

    data = {"file": file_to_convert.file, "target_format": target_format}
    response = client.post(url, data=data, format="multipart")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("Content-Type") == response_content_type
