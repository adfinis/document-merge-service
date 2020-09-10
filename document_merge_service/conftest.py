import importlib
import inspect
from io import BytesIO

import pytest
from django.core.cache import cache
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient

from document_merge_service.api.data import django_file

from .api import engines
from .api.authentication import AnonymousUser


def register_module(module):
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FactoryMetaClass) and not obj._meta.abstract:
            # name needs to be compatible with
            # `rest_framework.routers.SimpleRouter` naming for easier testing
            base_name = obj._meta.model._meta.object_name.lower()
            register(obj, base_name)


register_module(importlib.import_module(".api.factories", "document_merge_service"))


class TestUser(AnonymousUser):
    def __init__(self, username=None, groups=None):
        self.username = username if username else "admin"
        self.groups = groups or []

    @property
    def is_authenticated(self):
        return True


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()


@pytest.fixture
def admin_groups():
    return ["admin"]


@pytest.fixture
def admin_user(admin_groups):
    return TestUser(groups=admin_groups)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def docx_template_with_placeholder(admin_client, template):
    """Return a factory function to build a docx template with a given placeholder."""

    engine = engines.get_engine(template.engine, django_file("docx-template.docx"))

    def make_template(placeholder):
        binary = BytesIO()
        engine.merge({"test": placeholder}, binary)
        binary.seek(0)
        template.template.save("foo.docx", binary)
        template.save()
        return template

    return make_template
