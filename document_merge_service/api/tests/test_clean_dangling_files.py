import os

import pytest
from django.core.management import call_command

from document_merge_service.api.data import django_file


@pytest.mark.parametrize("dry", [True, False])
def test_clean_dangling_files(db, dry, settings, template_factory):
    templates = [
        template_factory(template=django_file("docx-template.docx")),
        template_factory(template=django_file("docx-template-syntax.docx")),
    ]
    dangling_files = [
        django_file("docx-template-filters.docx"),
        django_file("docx-template-loopcontrols.docx"),
    ]

    call_command("clean_dangling_files", dry=dry)

    assert (
        all(
            [
                os.path.isfile(os.path.join(settings.MEDIA_ROOT, file.name)) is dry
                for file in dangling_files
            ]
        )
        is True
    )
    assert (
        all([os.path.isfile(template.template.path) is True for template in templates])
        is True
    )
