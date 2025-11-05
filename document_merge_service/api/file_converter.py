from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now
from gotenberg_client import GotenbergClient
from gotenberg_client.options import PdfAFormat
from httpx import HTTPStatusError
from rest_framework import status
from rest_framework.exceptions import ParseError


class FileConverter:
    @staticmethod
    def convert(file_contents, filename):
        with GotenbergClient(settings.GOTENBERG_URL) as client:
            with client.libre_office.to_pdf() as route:
                try:
                    timestamp = now()
                    response = (
                        route.convert_in_memory_file(file_contents, name=filename)
                        .metadata(
                            creator="document-merge-service",
                            creation_date=timestamp,
                            modification_date=timestamp,
                        )
                        .metadata(**settings.GOTENBERG_PDF_METADATA)
                        .universal_access(universal_access=settings.GOTENBERG_PDF_UA)
                        .flatten(flatten=settings.GOTENBERG_PDF_FLATTEN)
                    )

                    if format := settings.GOTENBERG_PDF_A_FORMAT:
                        response = response.pdf_format(getattr(PdfAFormat, format))

                    result = response.run()

                    return HttpResponse(
                        content=result.content,
                        status=status.HTTP_200_OK,
                        content_type="application/pdf",
                    )
                except HTTPStatusError as exc:
                    raise ParseError(f"Failed to convert {filename} to a PDF") from exc
