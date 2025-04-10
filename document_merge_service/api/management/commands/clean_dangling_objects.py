import boto3
import botocore
from django.conf import settings
from django.core.management.base import BaseCommand

from document_merge_service.api.models import Template

S3_ENDPOINT_URL = settings.S3_STORAGE_OPTIONS["endpoint_url"]
S3_ACCESS_KEY_ID = settings.S3_STORAGE_OPTIONS["access_key"]
S3_SECRET_ACCESS_KEY = settings.S3_STORAGE_OPTIONS["secret_key"]
S3_BUCKET = settings.S3_STORAGE_OPTIONS["bucket_name"]


class Command(BaseCommand):
    help = "Cleans up unreferenced files and warns about unencrypted files in the storage bucket"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Delete data for real",
        )

    def get_object_keys(self, s3_client):
        keys = []
        have_next = True
        continuation_token = None
        while have_next:
            data = s3_client.list_objects_v2(
                Bucket=S3_BUCKET,
                **(
                    {"ContinuationToken": continuation_token}
                    if continuation_token
                    else {}
                ),
            )
            if data["KeyCount"] > 0:
                keys += [o["Key"] for o in data["Contents"]]
            have_next = data["IsTruncated"]
            if have_next:
                continuation_token = data["NextContinuationToken"]
        return keys

    def delete_file(self, s3_client, stats, fname, commit):
        print(f"Deleting unreferenced file: {fname}")
        if commit:
            s3_client.delete_object(Bucket=S3_BUCKET, Key=fname)
        stats["deleted"] += 1

    def check_encryption(self, s3_client, stats, fname):
        # Our approach is rather unsophisticated: we try to download an object
        # without encryption key, and if that succeeds, it means the object is
        # not encrypted, and therefore we print a warning.
        try:
            s3_client.get_object(Bucket=S3_BUCKET, Key=fname)
            print(f"WARNING, unencrypted file: {fname}")
            stats["unencrypted"] += 1
        except botocore.exceptions.ClientError:
            stats["encrypted"] += 1

    def handle(self, *args, **options):
        s3_session = boto3.session.Session()
        s3_client = s3_session.client(
            service_name="s3",
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
            endpoint_url=S3_ENDPOINT_URL,
        )
        bucket_files = self.get_object_keys(s3_client)
        used_files = Template.objects.all().values_list("template", flat=True)

        print(
            f"Cleaning up among {len(bucket_files)} bucket objects and {len(used_files)} DB entries"
        )
        stats = {
            "total": len(bucket_files),
            "encrypted": 0,
            "unencrypted": 0,
            "deleted": 0,
        }
        for f in bucket_files:
            if f in used_files:
                # file found in db, check if it's encrypted
                self.check_encryption(s3_client, stats, f)
            else:
                # file not found in db, can be deleted
                self.delete_file(s3_client, stats, f, options["commit"])

        print(f"stats: {stats}")
