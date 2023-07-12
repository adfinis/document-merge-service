import os

import pytest
from django.core.management import call_command

from document_merge_service.api.data import django_file


@pytest.mark.parametrize("dry", [True, False])
def test_upload_local_templates(db, dry, settings, template_factory):
    templates = [
        template_factory(template=django_file("docx-template.docx")),
        template_factory(template=django_file("docx-template-syntax.docx")),
    ]

    call_command("upload_local_templates", dry=dry)

    assert (
        all([os.path.isfile(template.template.path) is True for template in templates])
        is True
    )
