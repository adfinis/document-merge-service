import logging
from collections import namedtuple
from mimetypes import guess_type
from tempfile import NamedTemporaryFile

import unoserver.client
from django.conf import settings

logger = logging.getLogger(__name__)

UnoconvResult = namedtuple(
    "UnoconvResult", ["stdout", "stderr", "returncode", "content_type"]
)


class UnoConverter:
    def __init__(self):
        """Convert documents with help of LibreOffice via unoserver."""
        self.client = unoserver.client.UnoClient(
            server=settings.UNOSERVER_HOST,
            port=settings.UNOSERVER_PORT,
            host_location="remote",
        )

    def process(self, filename: str, convert: str) -> UnoconvResult:
        """Convert a file."""

        result_file = NamedTemporaryFile(suffix=f".{convert}")
        self.client.convert(
            inpath=filename,
            outpath=result_file.name,
            convert_to=convert,
        )

        content_type, _ = guess_type(result_file.name)

        result = UnoconvResult(
            stdout=result_file,
            stderr=None,
            returncode=0,
            content_type=content_type,
        )

        return result
