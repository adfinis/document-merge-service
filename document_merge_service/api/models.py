import os

from django.db import models
from django.dispatch import receiver


class Template(models.Model):
    DOCX_TEMPLATE = "docx-template"
    DOCX_MAILMERGE = "docx-mailmerge"
    ENGINE_CHOICES_LIST = (DOCX_TEMPLATE, DOCX_MAILMERGE)
    ENGINE_CHOICES_TUPLE = (
        (
            DOCX_TEMPLATE,
            "Docx Template engine (https://github.com/elapouya/python-docx-template)",
        ),
        (
            DOCX_MAILMERGE,
            "Docx MailMerge engine (https://github.com/Bouke/docx-mailmerge)",
        ),
    )

    slug = models.SlugField(primary_key=True)
    description = models.TextField(default="")
    template = models.FileField(max_length=1024)
    engine = models.CharField(max_length=20, choices=ENGINE_CHOICES_TUPLE)
    group = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    meta = models.JSONField(default=dict)


@receiver(models.signals.post_delete, sender=Template)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete template file from filesystem when `Template` object is deleted."""

    if os.path.isfile(instance.template.path):
        os.remove(instance.template.path)


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
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
