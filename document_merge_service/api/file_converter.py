from pathlib import Path
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.http import HttpResponse

from .unoconv import Unoconv


class FileConverter:
    def convert(file_contents, target_format):
        dir = Path(settings.DATABASE_DIR, "tmp")
        dir.mkdir(parents=True, exist_ok=True)

        with NamedTemporaryFile("wb", dir=dir) as tmp:
            tmp.write(file_contents)
            unoconv = Unoconv(
                pythonpath=settings.UNOCONV_PYTHON,
                unoconvpath=settings.UNOCONV_PATH,
            )
            result = unoconv.process(tmp.name, target_format)

        status = 200 if result.returncode == 0 else 500

        return HttpResponse(
            content=result.stdout, status=status, content_type=result.content_type
        )
