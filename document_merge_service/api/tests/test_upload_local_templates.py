import hashlib
import os
import shutil

import pytest
from django.core.management import call_command
from faker import Faker

from document_merge_service.api.data import django_file


def sha256sum(path):
    with open(path, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()


def is_equal(a, b):
    return sha256sum(a) == sha256sum(b)


@pytest.fixture
def tmp_path(settings):
    path = os.path.join(settings.MEDIA_ROOT, f"local-templates-{Faker().uuid4()}")

    yield path

    shutil.rmtree(path, ignore_errors=True)


@pytest.mark.parametrize("dry", [True, False])
def test_upload_local_templates(db, dry, template_factory, tmp_path):
    templates = [
        template_factory(template=django_file("docx-template-syntax.docx")),
        template_factory(template=django_file("docx-template-syntax.docx")),
    ]

    files = [
        django_file(
            "docx-template.docx",
            new_path=tmp_path,
            new_name=templates[0].template.name,
        ),
        django_file(
            "docx-template.docx",
            new_path=tmp_path,
            new_name=templates[1].template.name,
        ),
        django_file(
            "docx-template.docx",
            new_path=tmp_path,
            new_name="some-file-without-template.docx",
        ),
    ]

    paths = [os.path.join(tmp_path, file.name) for file in files]

    assert not is_equal(templates[0].template.path, paths[0])
    assert not is_equal(templates[1].template.path, paths[1])

    call_command("upload_local_templates", dry=dry, source=f"{tmp_path}/*.docx")

    assert is_equal(templates[0].template.path, paths[0]) != dry
    assert is_equal(templates[1].template.path, paths[1]) != dry
