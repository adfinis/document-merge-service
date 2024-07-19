import os
import re

import environ

from .sentry import sentry_init

env = environ.Env()
django_root = environ.Path(__file__) - 2

ENV_FILE = env.str("ENV_FILE", default=django_root(".env"))
if os.path.exists(ENV_FILE):  # pragma: no cover
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str("ENV", "production")


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


# Unoconv
ISOLATE_UNOCONV = env.bool("ISOLATE_UNOCONV", default=False)
SECRET_KEY = env.str("SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASE_DIR = env.str("DATABASE_DIR", default="/var/lib/document-merge-service/data")
DATABASES = {
    "default": {
        "ENGINE": env.str("DATABASE_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": env.str("DATABASE_NAME", default=f"{DATABASE_DIR}/sqlite3.db"),
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
    "generic_permissions.apps.GenericPermissionsConfig",
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

STORAGES = {
    "default": {
        "BACKEND": env.str(
            "FILE_STORAGE", default="django.core.files.storage.FileSystemStorage"
        )
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
MEDIA_ROOT = env.str("MEDIA_ROOT", "")
# TODO: This should be removed in favor of storing the files in a bucket
# https://code.djangoproject.com/ticket/32991
MEDIA_URL = env.str("MEDIA_URL", "api/v1/template/")

# django-storages S3 settings
DMS_ENABLE_AT_REST_ENCRYPTION = env.bool("DMS_ENABLE_AT_REST_ENCRYPTION", False)
S3_STORAGE_OPTIONS = {
    "access_key": env.str("DMS_S3_ACCESS_KEY_ID", "minio"),
    "secret_key": env.str("DMS_S3_SECRET_ACCESS_KEY", "minio123"),
    "bucket_name": env.str("DMS_STORAGE_BUCKET_NAME", "dms-media"),
    "endpoint_url": env.str("DMS_S3_ENDPOINT_URL", "http://minio:9000"),
    "region_name": env.str("DMS_S3_REGION_NAME", None),
    "location": env.str("DMS_LOCATION", ""),
    "file_overwrite": env.bool("DMS_S3_FILE_OVERWRITE", False),
    "signature_version": env.str("DMS_S3_SIGNATURE_VERSION", "v2"),
    "use_ssl": env.bool("DMS_S3_USE_SSL", default=True),
    "verify": env.bool("DMS_S3_VERIFY", default=None),
}

if DMS_ENABLE_AT_REST_ENCRYPTION:  # pragma: no cover
    S3_STORAGE_OPTIONS["object_parameters"] = {
        "SSECustomerKey": env.str(
            "DMS_S3_STORAGE_SSEC_SECRET",
            default=default("x" * 32),
        ),
        "SSECustomerAlgorithm": "AES256",
    }

if (
    STORAGES["default"]["BACKEND"] == "storages.backends.s3.S3Storage"
):  # pragma: no cover
    STORAGES["default"]["OPTIONS"] = S3_STORAGE_OPTIONS

# unoconv
UNOCONV_ALLOWED_TYPES = env.list("UNOCOV_ALLOWED_TYPES", default=["pdf"])
UNOCONV_PYTHON = env.str("UNOCONV_PYTHON", default="/usr/bin/python3")
UNOCONV_PATH = env.str("UNOCONV_PATH", default="/usr/bin/unoconv")


# Jinja2
DOCXTEMPLATE_JINJA_EXTENSIONS = env.list(
    "DOCXTEMPLATE_JINJA_EXTENSIONS", default=default([])
)

# Authentication

REQUIRE_AUTHENTICATION = env.bool("REQUIRE_AUTHENTICATION", False)

OIDC_USERINFO_ENDPOINT = env.str("OIDC_USERINFO_ENDPOINT", default=None)
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
OIDC_GROUPS_CLAIM = env.str("OIDC_GROUPS_CLAIM", default="")
OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME", default=0
)

# Rest framework
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "document_merge_service.api.permissions.AsConfigured",
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

PAGINATION_ENABLED = env.bool("PAGINATION_ENABLED", True)
PAGINATION_DEFAULT_PAGE_SIZE = env.int("PAGINATION_DEFAULT_PAGE_SIZE", 100)
PAGINATION_MAX_PAGE_SIZE = env.int("PAGINATION_MAX_PAGE_SIZE", 1000)

if PAGINATION_ENABLED:
    REST_FRAMEWORK.update(
        {
            "DEFAULT_PAGINATION_CLASS": "document_merge_service.api.pagination.APIPagination",
            "PAGE_SIZE": PAGINATION_DEFAULT_PAGE_SIZE,
        }
    )

# Logging
ENABLE_ADMIN_EMAIL_LOGGING = env.bool("ENABLE_ADMIN_EMAIL_LOGGING", False)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "WARNING",
            "filters": None,
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": None,
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {"django": {"handlers": ["console"], "level": "WARNING"}},
}

URL_PREFIX = env.str("URL_PREFIX", default="")

# Email settings
SERVER_EMAIL = env.str("SERVER_EMAIL", default="root@localhost")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="webmaster@localhost")
EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=25)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)

# Email error handler
if ENABLE_ADMIN_EMAIL_LOGGING:  # pragma: no cover
    LOGGING["loggers"]["django"]["handlers"].append("mail_admins")  # type: ignore

# Sentry error tracking
SENTRY_DSN = env.str("SENTRY_DSN", default="")
SENTRY_ENVIRONMENT = env.str("SENTRY_ENVIRONMENT", default="development")
SENTRY_TRACES_SAMPLE_RATE = env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.01)
SENTRY_SEND_DEFAULT_PII = env.bool("SENTRY_SEND_DEFAULT_PII", default=False)

if SENTRY_DSN:  # pragma: no cover
    sentry_init(
        SENTRY_DSN,
        SENTRY_ENVIRONMENT,
        SENTRY_TRACES_SAMPLE_RATE,
        SENTRY_SEND_DEFAULT_PII,
    )

# https://github.com/adfinis/django-generic-api-permissions
GENERIC_PERMISSIONS_PERMISSION_CLASSES = env.list("DMS_PERMISSION_CLASSES", default=[])
GENERIC_PERMISSIONS_VISIBILITY_CLASSES = env.list("DMS_VISIBILITY_CLASSES", default=[])

# App specific arguments for the extension classes
EXTENSIONS_ARGUMENTS = env.dict("EXTENSIONS_ARGUMENTS", default={})
