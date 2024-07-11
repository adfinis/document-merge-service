from copy import deepcopy
from io import StringIO

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File as DjangoFile
from django.core.management import call_command
from storages.backends.s3 import S3Storage

from document_merge_service.api.data import django_file


@pytest.fixture
def settings_storage(settings):
    settings.STORAGES = deepcopy(settings.STORAGES)
    return settings.STORAGES


def test_encrypt_templates(db, settings, settings_storage, mocker, template_factory):
    template_factory(template=django_file("docx-template.docx"))

    settings.DMS_ENABLE_AT_REST_ENCRYPTION = True
    settings_storage["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            **settings.S3_STORAGE_OPTIONS,
            "object_parameters": {
                "SSECustomerKey": "x" * 32,
                "SSECustomerAlgorithm": "AES256",
            },
        },
    }

    mocker.patch("storages.backends.s3.S3Storage.open")
    mocker.patch("storages.backends.s3.S3Storage.save")
    S3Storage.save.return_value = "name-of-the-file"
    S3Storage.open.return_value = DjangoFile(open("README.md", "rb"))

    call_command("dms_encrypt_templates")

    assert S3Storage.open.call_count == 1
    assert S3Storage.save.call_count == 1


def test_encrypt_templates_disabled(db, template_factory):
    template_factory(template=django_file("docx-template.docx"))

    out = StringIO()
    call_command("dms_encrypt_templates", stdout=out)

    assert (
        "Encryption is not enabled. Skipping encryption of templates." in out.getvalue()
    )


def test_encrypt_template_improperyconfigured(db, settings, template_factory):
    template_factory(template=django_file("docx-template.docx"))
    settings.DMS_ENABLE_AT_REST_ENCRYPTION = True

    out = StringIO()
    with pytest.raises(ImproperlyConfigured):
        call_command("dms_encrypt_templates", stdout=out)


def test_encrypt_templates_failed(
    db, settings, settings_storage, mocker, template_factory
):
    template_factory(template=django_file("docx-template.docx"))

    settings.DMS_ENABLE_AT_REST_ENCRYPTION = True
    settings_storage["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            **settings.S3_STORAGE_OPTIONS,
            "object_parameters": {
                "SSECustomerKey": "x" * 32,
                "SSECustomerAlgorithm": "AES256",
            },
        },
    }

    mocker.patch("storages.backends.s3.S3Storage.open", side_effect=FileNotFoundError)
    mocker.patch("storages.backends.s3.S3Storage.save")
    S3Storage.save.return_value = "name-of-the-file"
    S3Storage.open.return_value = DjangoFile(open("README.md", "rb"))

    out = StringIO()
    call_command("dms_encrypt_templates", stdout=out)

    assert S3Storage.open.call_count == 1
    assert S3Storage.save.call_count == 0
    assert "failed" in out.getvalue()
