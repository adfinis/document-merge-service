import os

from django.conf import settings
from django.core.management.base import BaseCommand

from document_merge_service.api.models import Template


class Command(BaseCommand):
    help = "Remove dangling template files that are not attached to a template model anymore. Currently only usable with local filesystem."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", dest="dry", action="store_true", default=False)

    def handle(self, *args, **options):
        used_files = [template.template.path for template in Template.objects.all()]

        for subdir, dirs, files in os.walk(settings.MEDIA_ROOT):
            for f in files:
                path = os.path.join(subdir, f)
                if path not in used_files and os.path.isfile(path):
                    try:
                        if not options.get("dry"):
                            os.remove(path)
                            self.stdout.write(
                                self.style.SUCCESS(f"Deleted dangling file '{path}'")
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Would delete dangling file '{path}'"
                                )
                            )
                    except Exception as e:  # pragma: no cover
                        self.stdout.write(
                            self.style.ERROR(
                                f"Could not delete dangling file '{path}': {str(e)}"
                            )
                        )
