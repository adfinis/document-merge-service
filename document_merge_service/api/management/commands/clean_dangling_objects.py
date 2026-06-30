import boto3
import botocore
from django.conf import settings
from django.core.management.base import BaseCommand

from document_merge_service.api.models import Template

S3_ENDPOINT_URL = settings.S3_STORAGE_OPTIONS["endpoint_url"]
S3_ACCESS_KEY_ID = settings.S3_STORAGE_OPTIONS["access_key"]
S3_SECRET_ACCESS_KEY = settings.S3_STORAGE_OPTIONS["secret_key"]
S3_BUCKET = settings.S3_STORAGE_OPTIONS["bucket_name"]
S3_SSEC_ENABLED = settings.DMS_ENABLE_AT_REST_ENCRYPTION


class Command(BaseCommand):
    help = "Deletes unreferenced objects and warns about unencrypted objects in the S3 storage bucket"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Delete data for real",
        )

    def get_object_keys(self):
        """Fetch keys for all objects in the bucket, in batches.

        This is an iterator, yielding batch after batch.
        """
        have_next = True
        continuation_token = None
        while have_next:
            data = self.s3_client.list_objects_v2(
                Bucket=S3_BUCKET,
                **(
                    {"ContinuationToken": continuation_token}
                    if continuation_token
                    else {}
                ),
            )
            if data["KeyCount"] > 0:
                yield [o["Key"] for o in data["Contents"]]
            have_next = data["IsTruncated"]
            if have_next:
                continuation_token = data["NextContinuationToken"]

    def delete_object(self, object_key):
        """Delete the object with the given key (if running in commit mode)."""
        self.stdout.write(f"Deleting unreferenced file: {object_key}")
        if self.commit:
            self.s3_client.delete_object(Bucket=S3_BUCKET, Key=object_key)
        self.stats["deleted"] += 1

    def check_object_encryption(self, object_key):
        """Check if an object is encrypted.

        Collect statistics about encryption status, and print a warning for unencrypted
        objects.
        """
        # Our approach is rather unsophisticated: we try to fetch an object without
        # encryption key, and if that succeeds, it means the object is not encrypted,
        # and therefore we print a warning.
        try:
            self.s3_client.head_object(Bucket=S3_BUCKET, Key=object_key)
            self.stdout.write(self.style.WARNING(f"Unencrypted file: {object_key}"))
            self.stats["unencrypted"] += 1
        except botocore.exceptions.ClientError:
            self.stats["encrypted"] += 1

    def handle(self, *args, **options):
        self.commit = options["commit"]

        if settings.STORAGES["default"]["BACKEND"] != "storages.backends.s3.S3Storage":
            self.stderr.write(
                self.style.ERROR(
                    "This command is only for setups using the S3 storage backend"
                )
            )
            return

        s3_session = boto3.session.Session()
        self.s3_client = s3_session.client(
            service_name="s3",
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
            endpoint_url=S3_ENDPOINT_URL,
        )

        self.stats = {}
        for objects in self.get_object_keys():
            templates = Template.objects.filter(template__in=objects).values_list(
                "template", flat=True
            )

            self.stdout.write(
                f"Cleaning up among {len(objects)} bucket objects and {len(templates)} DB entries"
            )
            self.stats = {
                "total": len(objects),
                "encrypted": 0,
                "unencrypted": 0,
                "deleted": 0,
            }
            for o in objects:
                if o in templates:
                    # file found in db, object not dangling
                    if S3_SSEC_ENABLED:
                        self.check_object_encryption(o)
                else:
                    # file not found in db, object dangling
                    self.delete_object(o)

        self.stdout.write(self.style.SUCCESS(f"Stats: {self.stats}"))
