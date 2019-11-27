import pytest
from django.conf import settings

from ..unoconv import Unoconv


@pytest.mark.parametrize(
    "unoconv_server,uses_external_unoconv", [(None, False), ("192.168.1.1", True)]
)
def test_unoconv_local(unoconv_server, uses_external_unoconv):
    uc = Unoconv(
        pythonpath=settings.UNOCONV_PYTHON,
        unoconvpath=settings.UNOCONV_PATH,
        server=unoconv_server,
    )
    assert (unoconv_server in uc.cmd) == uses_external_unoconv
