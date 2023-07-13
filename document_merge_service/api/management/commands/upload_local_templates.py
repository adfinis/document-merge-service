import os

from django.conf import settings
from django.core.files.storage import DefaultStorage
from django.core.management.base import BaseCommand

from document_merge_service.api.models import Template


class Command(BaseCommand):
    help = "Add filesystem files to configured storage backend"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", dest="dry", action="store_true", default=False)

    def handle(self, *args, **options):
        storage = DefaultStorage()
        for template in Template.objects.all():
            try:
                with open(
                    os.path.join(settings.MEDIA_ROOT, template.template.name), "rb"
                ) as file:
                    if not options.get("dry"):
                        storage.save(template.template.name, file)
                        self.stdout.write(
                            self.style.SUCCESS(f"Uploaded file for '{template.pk}'")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"Would upload file for '{template.pk}'")
                        )
            except Exception as e:  # pragma: no cover
                self.stdout.write(
                    self.style.ERROR(f"Could not upload file '{template.pk}': {str(e)}")
                )
