import os
import logging


from django.db import migrations
from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def cleanup_files(apps, schema_editor):
    Template = apps.get_model("api", "Template")
    used_files = [template.template.path for template in Template.objects.all()]

    with os.scandir(settings.MEDIA_ROOT) as files:
        for f in files:
            if not f.path in used_files and os.path.isfile(f.path):
                os.remove(f.path)


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_template_meta"),
    ]

    operations = [migrations.RunPython(cleanup_files, migrations.RunPython.noop)]
