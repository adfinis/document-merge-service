import os
import re

import environ
import requests
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status

env = environ.Env()
django_root = environ.Path(__file__) - 2

ENV_FILE = env.str("ENV_FILE", default=django_root(".env"))
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str("ENV", "production")


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


SECRET_KEY = env.str("SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DATABASE_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": env.str(
            "DATABASE_NAME", default="/var/lib/document-merge-service/data/sqlite3.db"
        ),
        "USER": env.str("DATABASE_USER", default=""),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=""),
        "HOST": env.str("DATABASE_HOST", default=""),
        "PORT": env.str("DATABASE_PORT", default=""),
        "OPTIONS": env.dict("DATABASE_OPTIONS", default={}),
    }
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "document_merge_service.api.apps.DefaultConfig",
]

if "postgresql" in DATABASES["default"]["ENGINE"]:  # pragma: no cover
    INSTALLED_APPS.append("django.contrib.postgres")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "document_merge_service.urls"
WSGI_APPLICATION = "document_merge_service.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


# Cache
# https://docs.djangoproject.com/en/1.11/ref/settings/#caches

CACHES = {
    "default": {
        "BACKEND": env.str(
            "CACHE_BACKEND", default="django.core.cache.backends.locmem.LocMemCache"
        ),
        "LOCATION": env.str("CACHE_LOCATION", ""),
        "TIMEOUT": env.int("CACHE_TIMEOUT", 300),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = env.str("LANGUAGE_CODE", "en-us")
TIME_ZONE = env.str("TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search(r"(.+) \<(.+@.+)\>", admin)
        if not match:  # pragma: no cover
            raise environ.ImproperlyConfigured(
                'In ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin)
            )
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list("ADMINS", default=[]))


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = env.str("STATIC_ROOT", None)

# Media files

DEFAULT_FILE_STORAGE = env.str(
    "FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
)
MEDIA_ROOT = env.str("MEDIA_ROOT", "")

# Unoconv webservice
# https://github.com/zrrrzzt/tfk-api-unoconv

UNOCONV_ALLOWED_TYPES = env.list("UNOCOV_ALLOWED_TYPES", default=["pdf"])
UNOCONV_URL = env.str("UNOCONV_URL", default="").rstrip("/")


def get_unoconv_formats():
    resp = requests.get(f"{UNOCONV_URL}/unoconv/formats")
    if resp.status_code != status.HTTP_200_OK:
        raise ImproperlyConfigured(
            f"Configured unoconv service {UNOCONV_URL} doesn't respond correctly"
        )

    formats = {fmt["format"]: fmt for fmt in resp.json().get("document", [])}
    not_supported = set(UNOCONV_ALLOWED_TYPES) - formats.keys()

    if not_supported:
        raise ImproperlyConfigured(
            f"Unoconv doesn't support types {', '.join(not_supported)}."
        )

    return formats


UNOCONV_FORMATS = UNOCONV_URL and get_unoconv_formats()

# Authentication

REQUIRE_AUTHENTICATION = env.bool("REQUIRE_AUTHENTICATION", False)
GROUP_ACCESS_ONLY = env.bool("GROUP_ACCESS_ONLY", False)

OIDC_USERINFO_ENDPOINT = env.str("OIDC_USERINFO_ENDPOINT", default=None)
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
OIDC_GROUPS_CLAIM = env.str(
    "OIDC_GROUPS_CLAIM", default="document_merge_service_groups"
)


# Rest framework
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_PERMISSION_CLASSES": [
        "document_merge_service.api.permissions.AsConfigured"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "document_merge_service.api.authentication.BearerTokenAuthentication"
    ],
    "UNAUTHENTICATED_USER": "document_merge_service.api.authentication.AnonymousUser",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.OrderingFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}
