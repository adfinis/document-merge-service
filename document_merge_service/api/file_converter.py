import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError


class FileConverter:
    def convert(file_contents, filename):
        response = requests.post(
            f"{settings.GOTENBERG_HOST}:{settings.GOTENBERG_PORT}/forms/libreoffice/convert",
            files={"files": (filename, file_contents)},
        )

        if response.status_code != status.HTTP_200_OK:
            raise ValidationError(f"Failed to convert {filename} to a PDF")

        return HttpResponse(
            content=response.content,
            status=status.HTTP_200_OK,
            content_type="application/pdf",
        )
