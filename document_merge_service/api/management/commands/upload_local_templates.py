import glob
import os

from django.core.files.storage import DefaultStorage
from django.core.management.base import BaseCommand

from document_merge_service.api.models import Template


class Command(BaseCommand):
    help = "Upload local template files to configured storage backend"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--source",
            help="Glob-style path to the template files that should be uploaded. E.g. `/tmp/templates/*.docx`",
            dest="source",
            type=str,
            required=True,
        )
        parser.add_argument(
            "--dry-run",
            help="Only show what files would be uploaded to the storage backend; don't actually upload them.",
            dest="dry",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        storage = DefaultStorage()

        for path in glob.iglob(options["source"]):
            filename = os.path.basename(path)

            try:
                template = Template.objects.get(template=filename)
            except Template.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'No template for filename "{filename}" found')
                )
                continue

            if not options.get("dry"):
                try:
                    with open(path, "rb") as file:
                        storage.delete(template.template.name)
                        storage.save(template.template.name, file)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Uploaded file for template "{template.pk}"'
                        )
                    )
                except Exception as e:  # pragma: no cover
                    self.stdout.write(
                        self.style.ERROR(
                            f'Could not upload file for template "{template.pk}": {str(e)}'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Would upload file for template "{template.pk}"'
                    )
                )
