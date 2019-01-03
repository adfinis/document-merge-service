import io

import requests
from django.conf import settings
from rest_framework import exceptions, status


def convert(from_file, to_type):
    """
    Use docker-unoconv-webservice to convert document to given type.

    Returns `io.BytesIO` of file or raises `exceptions.ParseError` when conversion failed.

    See: https://github.com/zrrrzzt/tfk-api-unoconv
    """
    url = f"{settings.UNOCONV_URL}/unoconv/{to_type}"
    response = requests.post(url, files={"file": from_file})

    if response.status_code == status.HTTP_200_OK:
        return io.BytesIO(response.content)

    raise exceptions.ParseError(f"Conversion to type {to_type} failed")
