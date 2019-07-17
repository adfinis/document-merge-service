from django.apps import AppConfig
from django.conf import settings
from django.db.models import TextField
from django.db.models.lookups import IContains


class DefaultConfig(AppConfig):
    name = "document_merge_service.api"

    def ready(self):
        if "sqlite3" in settings.DATABASES["default"]["ENGINE"]:  # pragma: no cover
            TextField.register_lookup(IContains, lookup_name="search")
