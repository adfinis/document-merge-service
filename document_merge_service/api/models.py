from django.core.files.storage import DefaultStorage
from django.db import models
from django.dispatch import receiver


class Template(models.Model):
    DOCX_TEMPLATE = "docx-template"
    DOCX_MAILMERGE = "docx-mailmerge"
    XLSX_TEMPLATE = "xlsx-template"
    ENGINE_CHOICES_LIST = (DOCX_TEMPLATE, DOCX_MAILMERGE, XLSX_TEMPLATE)
    ENGINE_CHOICES_TUPLE = (
        (
            DOCX_TEMPLATE,
            "Docx Template engine (https://github.com/elapouya/python-docx-template)",
        ),
        (
            DOCX_MAILMERGE,
            "Docx MailMerge engine (https://github.com/Bouke/docx-mailmerge)",
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
    meta = models.JSONField(default=dict)


@receiver(models.signals.post_delete, sender=Template)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete template file from filesystem when `Template` object is deleted."""

    DefaultStorage().delete(instance.template.name)


@receiver(models.signals.pre_save, sender=Template)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Delete old template file from filesystem when `Template` is given a new template file."""

    try:
        old_file = Template.objects.get(pk=instance.pk).template
    except Template.DoesNotExist:
        return

    if old_file:
        new_file = instance.template
        if not old_file == new_file:
            DefaultStorage().delete(old_file.name)
