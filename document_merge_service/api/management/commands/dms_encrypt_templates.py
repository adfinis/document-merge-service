from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import storages
from django.core.management.base import BaseCommand
from tqdm import tqdm

from document_merge_service.api.models import Template


class Command(BaseCommand):
    help = "Swaps plain text template content to encrypted content"

    def handle(self, *args, **options):
        if not settings.DMS_ENABLE_AT_REST_ENCRYPTION:
            return self.stdout.write(
                self.style.WARNING(
                    "Encryption is not enabled. Skipping encryption of templates."
                )
            )

        failed_templates = []

        # flip between default and encrypted storage to have the correct parameters in the requests
        encrypted_storage = storages.create_storage(settings.STORAGES["default"])
        unencrypted_storage_setting = settings.STORAGES["default"]
        if (
            "OPTIONS" not in unencrypted_storage_setting
            or "object_parameters" not in unencrypted_storage_setting["OPTIONS"]
        ):
            raise ImproperlyConfigured(
                "Encryption is enabled but no object_parameters found in the storage settings."
            )
        del unencrypted_storage_setting["OPTIONS"]["object_parameters"]
        unencrypted_storage = storages.create_storage(unencrypted_storage_setting)

        query = Template.objects.all()
        for template in tqdm(query.iterator(50), total=query.count()):
            # get original template content
            template.template.storage = unencrypted_storage
            try:
                content = template.template.open()

                # overwrite with encrypted content
                template.template.storage = encrypted_storage
                template.template.save(template.template.name, content)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Error for template {str(template.pk)}: {e}")
                )
                failed_templates.append(str(template.pk))
                continue

        if failed_templates:
            self.stdout.write(
                self.style.WARNING(f"These templates failed:\n{failed_templates}")
            )
        self.stdout.write(self.style.SUCCESS("Encryption finished"))
