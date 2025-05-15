from django.core.files.storage import DefaultStorage
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.dispatch import receiver


class Template(models.Model):
    DOCX_TEMPLATE = "docx-template"
    XLSX_TEMPLATE = "xlsx-template"
    ENGINE_CHOICES_LIST = (DOCX_TEMPLATE, XLSX_TEMPLATE)
    ENGINE_CHOICES_TUPLE = (
        (
            DOCX_TEMPLATE,
            "Docx Template engine (https://github.com/elapouya/python-docx-template)",
        ),
        (
            XLSX_TEMPLATE,
            "Xlsx Template engine (https://github.com/zhangyu836/python-xlsx-template)",
        ),
    )

    slug: models.SlugField = models.SlugField(primary_key=True)
    description: models.TextField = models.TextField(default="")
    template: models.FileField = models.FileField(max_length=1024)
    engine: models.CharField = models.CharField(
        max_length=20, choices=ENGINE_CHOICES_TUPLE
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, db_index=True, null=True
    )
    created_by_user: models.CharField = models.CharField(
        max_length=150, blank=True, null=True
    )
    created_by_group: models.CharField = models.CharField(
        max_length=255, blank=True, null=True
    )
    modified_at: models.DateTimeField = models.DateTimeField(
        auto_now=True, db_index=True, null=True
    )
    modified_by_user: models.CharField = models.CharField(
        max_length=150, blank=True, null=True
    )
    modified_by_group: models.CharField = models.CharField(
        max_length=255, blank=True, null=True
    )
    meta = models.JSONField(default=dict)


@receiver(models.signals.post_delete, sender=Template)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete template file from filesystem when `Template` object is deleted."""

    if instance.template:
        DefaultStorage().delete(instance.template.name)


@receiver(models.signals.pre_save, sender=Template)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Delete old template file from filesystem when `Template` is given a new template file.

    If a new template file is uploaded, we need to explicitly delete the old file
    to prevent dangling files in the storage. If no new file is being uploaded (i.e.
    only other, normal attributes are changed), we keep the file.
    """

    try:
        old_file = Template.objects.get(pk=instance.pk).template
    except Template.DoesNotExist:
        return

    if old_file:
        new_file = instance.template
        if isinstance(new_file.file, UploadedFile):
            DefaultStorage().delete(old_file.name)
