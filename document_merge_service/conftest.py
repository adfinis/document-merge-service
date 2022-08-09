import shutil
from io import BytesIO
from pathlib import Path

import pytest
from django.core.cache import cache
from pytest_factoryboy import register
from rest_framework.test import APIClient

from document_merge_service.api import models
from document_merge_service.api.data import django_file

from .api import engines, factories
from .api.authentication import AnonymousUser

register(factories.TemplateFactory)


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
def mock_filefield_name_validation(mocker):
    mocker.patch(
        "django.db.models.fields.files.validate_file_name",
        side_effect=lambda name, *args, **kwargs: name,
    )


@pytest.fixture
def docx_template_with_placeholder(admin_client, template):
    """Return a factory function to build a docx template with a given placeholder."""
    template.engine = models.Template.DOCX_TEMPLATE
    template.template = django_file("docx-template.docx")
    template.save()

    def make_template(placeholder):
        engine = engines.get_engine(template.engine, template.template)
        binary = BytesIO()
        engine.merge({"test": placeholder}, binary)
        binary.seek(0)
        template.template.save("foo.docx", binary)
        template.save()
        return template

    return make_template


@pytest.fixture
def dms_test_bin():
    sleep_path = Path(shutil.which("sleep"))
    test_path = Path(Path(__file__).parent.absolute(), "tmpb5nw53v5")
    with test_path.open("wb") as f, open(sleep_path, "rb") as g:
        f.write(g.read())
    test_path.chmod(0o755)
    yield test_path
    test_path.unlink()
