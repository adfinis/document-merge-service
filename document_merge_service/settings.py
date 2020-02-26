import os
import re

import environ
from django.core.exceptions import ImproperlyConfigured

from .api.unoconv import Unoconv

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
    "corsheaders",
]

if "postgresql" in DATABASES["default"]["ENGINE"]:  # pragma: no cover
    INSTALLED_APPS.append("django.contrib.postgres")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
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
    }
}


# CORS
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", False)
CORS_ORIGIN_REGEX_WHITELIST = [r"^(https?://)?127\.0\.0\.1:\d{4}$"]
CORS_ORIGIN_REGEX_WHITELIST += env.list(
    "CORS_ORIGIN_REGEX_WHITELIST", default=[r"^(https?://)?127\.0\.0\.1:\d{4}$"]
)


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

UNOCONV_ALLOWED_TYPES = env.list("UNOCOV_ALLOWED_TYPES", default=["pdf"])
UNOCONV_PYTHON = env.str("UNOCONV_PYTHON", default="/usr/bin/python3")
UNOCONV_PATH = env.str("UNOCONV_PATH", default="/usr/bin/unoconv")


def get_unoconv_formats():
    uno = Unoconv(pythonpath=UNOCONV_PYTHON, unoconvpath=UNOCONV_PATH)
    formats = uno.get_formats()
    not_supported = set(UNOCONV_ALLOWED_TYPES) - formats

    if not_supported:
        raise ImproperlyConfigured(
            f"Unoconv doesn't support types {', '.join(not_supported)}."
        )

    return formats


UNOCONV_FORMATS = get_unoconv_formats()

# Jinja2
DOCXTEMPLATE_JINJA_EXTENSIONS = env.list(
    "DOCXTEMPLATE_JINJA_EXTENSIONS", default=default([])
)

# Authentication

REQUIRE_AUTHENTICATION = env.bool("REQUIRE_AUTHENTICATION", False)
GROUP_ACCESS_ONLY = env.bool("GROUP_ACCESS_ONLY", False)

OIDC_USERINFO_ENDPOINT = env.str("OIDC_USERINFO_ENDPOINT", default=None)
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
OIDC_GROUPS_CLAIM = env.str("OIDC_GROUPS_CLAIM", default="")
OIDC_GROUPS_API = env.str("OIDC_GROUPS_API", default="")
OIDC_GROUPS_API_REVALIDATION_TIME = env.int(
    "OIDC_GROUPS_API_REVALIDATION_TIME", default=0
)
OIDC_GROUPS_API_VERIFY_SSL = env.str("OIDC_GROUPS_API_VERIFY_SSL", default=True)
# environ interprets leading jsonpath dollar to be an proxied environ var
# which is not the case
OIDC_GROUPS_API_JSONPATH = os.environ.get("OIDC_GROUPS_API_JSONPATH", "")
OIDC_GROUPS_API_HEADERS = [
    header.upper()
    for header in env.list("OIDC_GROUPS_API_HEADERS", default=["AUTHORIZATION"])
]
OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME", default=0
)

if OIDC_GROUPS_API and not OIDC_GROUPS_API_JSONPATH:  # pragma: no cover
    raise ImproperlyConfigured(
        f"OIDC_GROUSP_API` is set to {OIDC_GROUPS_API} but no `OIDC_GROUPS_API_JSONPATH` is configured."
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

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "WARNING",
            "filters": None,
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {"django": {"handlers": ["console"], "level": "WARNING"}},
}
