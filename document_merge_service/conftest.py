import importlib
import inspect

import pytest
from factory.base import FactoryMetaClass
from pytest_factoryboy import register
from rest_framework.test import APIClient

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
