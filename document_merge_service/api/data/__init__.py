import os.path
import shutil

from django.conf import settings
from django.core.files import File

_data_path = os.path.dirname(os.path.realpath(__file__))


def django_file(name, mode="rb", new_path=None, new_name=None):
    abspath = os.path.join(_data_path, name)

    if not new_path:
        new_path = settings.MEDIA_ROOT

    if not new_name:
        new_name = name

    try:
        os.makedirs(new_path)
    except FileExistsError:  # pragma: no cover
        pass

    shutil.copy(abspath, f"{new_path}/{new_name}")

    return File(open(abspath, mode), name=new_name)
