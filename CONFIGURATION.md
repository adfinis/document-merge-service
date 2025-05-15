# Configuration

Document Merge Service is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

## Common

- `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
- `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).

## Database

Per default [Sqlite3](https://sqlite.org/) is used as database for simple deployment and stored at `/var/lib/document-merge-service/data/sqlite3.db`. Create a volume to make it persistent.

To scale the service a different database storage is needed. Any database supported by [Django](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE) can be used.

- `DATABASE_ENGINE`: Database backend to use.
- `DATABASE_HOST`: Host to use when connecting to database
- `DATABASE_PORT`: Port to use when connecting to database
- `DATABASE_NAME`: Name of database to use
- `DATABASE_USER`: Username to use when connecting to the database
- `DATABASE_PASSWORD`: Password to use when connecting to database

## Unoconv

- `UNOCONV_ALLOWED_TYPES`: List of types allowed to convert to. See `unoconv --show` (default: ['pdf'])
- `UNOCONV_PYTHON`: String, defaults to "/usr/bin/python3.5"
- `UNOCONV_PATH`: String, defaults to "/usr/bin/unoconv"

## python-docx-template

- `DOCXTEMPLATE_JINJA_EXTENSIONS`: list of [jinja2 extensions](http://jinja.pocoo.org/docs/2.10/extensions/) to load

In python-docx-template following additional custom filters are implemented:

- multiline(value) - wraps the value in a [Listing](https://docxtpl.readthedocs.io/en/latest/#escaping-newline-new-paragraph-listing) for multiline support
- datetimeformat(value, format, locale)
- dateformat(value, format, locale)
- timeformat(value, format, locale)
- getwithdefault(value, default) - converts None to empty string (or provided default value) or leaves strings as is
- emptystring(value) - converts None to empty string or leaves strings as is (deprecated in favor of getwithdefault)
- image(width, height, keep_aspect_ratio) - Creates an [inline image](https://docxtpl.readthedocs.io/en/latest/) from provided file with the same name. `width` and `height` are optional and represent millimetres. If `keep_aspect_ratio` is `True` the image will be scaled keeping it's original aspect ratio and the width/height parameters become a size limit instead. `keep_aspect_ration` has no effect if `width` and `height` are not given.

For formatting use babel and its uniode compatible [format](http://babel.pocoo.org/en/latest/dates.html#date-fields).

## Authentication / Authorization

By default, no authentication is needed. To protect the API, integrate
it with your [IAM](https://en.wikipedia.org/wiki/Identity_management)
supporting Open ID Connect. If not available, you might consider using
[Keycloak](https://www.keycloak.org/).

- `REQUIRE_AUTHENTICATION`: Force authentication to be required (default: False)
- `OIDC_USERINFO_ENDPOINT`: Url of userinfo endpoint as [described](https://openid.net/specs/openid-connect-core-1_0.html#UserInfo)
- `OIDC_VERIFY_SSL`: Verify ssl certificate of oidc userinfo endpoint (default: True)
- `OIDC_GROUPS_CLAIM`: Name of claim to be used to define group membership (default: document_merge_service_groups)
- `OIDC_USERNAME_CLAIM`: Name of claim to be used to define user (default: sub)
- `OIDC_BEARER_TOKEN_REVALIDATION_TIME`: Time in seconds before bearer token validity is verified again. For best security token is validated on each request per default. It might be helpful though in case of slow Open ID Connect provider to cache it. It uses [cache](#cache) mechanism for memorizing userinfo result. Number has to be lower than access token expiration time. (default: 0)

## Permissions / Visibilities

Document Merge Service uses [dgap](https://github.com/adfinis/django-generic-api-permissions)
to handle permissions and visibilities. It can be configured using the following
environment variables:

- `DMS_VISIBILITY_CLASSES`: List of classes that handle [dgap visibilities](https://github.com/adfinis/django-generic-api-permissions#visibilities)
- `DMS_PERMISSION_CLASSES`: List of classes that handle [dgap permissions](https://github.com/adfinis/django-generic-api-permissions#permissions)
- `EXTENSIONS_ARGUMENTS`: Custom arguments from the app to be used in the
  visibility and permission classes. This is expected to be a `dict`, e.g.
  `EXTENSIONS_ARGUMENTS=foo=bar` could then be used in the extension classes as
  `settings.EXTENSIONS_ARGUMENTS["foo"]`

## Cache

- `CACHE_BACKEND`: [cache backend](https://docs.djangoproject.com/en/4.2/ref/settings/#backend) to use (default: django.core.cache.backends.locmem.LocMemCache)
- `CACHE_LOCATION`: [location](https://docs.djangoproject.com/en/4.2/ref/settings/#location) of cache to use
- `CACHE_OPTIONS`: [options](https://docs.djangoproject.com/en/4.2/ref/settings/#options) for cache library

## CORS

- `CORS_ORIGIN_ALLOW_ALL`: [allow all](https://github.com/ottoyiu/django-cors-headers#cors_origin_allow_all)
- `CORS_ORIGIN_REGEX_WHITELIST`: List of [whitelist regexes](https://github.com/ottoyiu/django-cors-headers#cors_origin_regex_whitelist) defaults to "^(https?://)?127\.0\.0\.1:\d{4}$"

Users of nginx/apache must ensure to have matching CORS configurations.

## Pagination

- `PAGINATION_ENABLED`: whether the pagination is enabled (default: `True`)
- `PAGINATION_DEFAULT_PAGE_SIZE`: the default page size if no query param (`page_size`) is given (default: `100`)
- `PAGINATION_MAX_PAGE_SIZE`: the max value of the page size query param (`page_size`) (default: `1000`)

## Email

- `SERVER_EMAIL`: the email address that error messages come from
- `DEFAULT_FROM_EMAIL`: default email address to use for various automated correspondence. This doesn’t include error messages sent to `ADMINS`.
- `EMAIL_HOST`: the host to use for sending email (default: `localhost`)
- `EMAIL_PORT`: port to use for the SMTP server (default: `25`)
- `EMAIL_HOST_USER`: username for the SMTP server(default: "")
- `EMAIL_HOST_PASSWORD`: password for the SMTP server user (default: "")
- `EMAIL_USE_TLS`: whether to use an implicit TLS (secure) connection when talking to the SMTP server (default: `False`)

If either `EMAIL_HOST_USER` or `EMAIL_HOST_PASSWORD` is empty, Django won't attempt authentication.

## Email error handler

- `ENABLE_ADMIN_EMAIL_LOGGING`: enable Django to send email to admins on errors (default: `False`)
- `ADMINS`: list of people who will get code error notifications. Items in the list should follow this example: `Test Example <test@example.com>,Test2 <test2@example.com>`

## Sentry

- `SENTRY_DSN`: identifier (data source name) for where to send events to. If no value is provided, sentry won't be activated (default: "")
- `SENTRY_ENVIRONMENT`: which app environment sent an event to sentry (default: `development`)
- `SENTRY_TRACES_SAMPLE_RATE`: percentage chance a given transaction will be sent to Sentry (default: `1.0`)
- `SENTRY_SEND_DEFAULT_PII`: enable send PII data that associates users to errors (default: `True`)

## Template storage

- `FILE_STORAGE`: Django file storage backend (default: `django.core.files.storage.FileSystemStorage`)
- `MEDIA_ROOT`: Absolute filesystem path to the directory that will hold user-uploaded files. (default: "")
- `MEDIA_URL`: URL that handles the media served from MEDIA_ROOT, used for managing stored files. When using buckets this needs to be changed. (default: `api/v1/template/`)

### [django-storages](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html) S3 settings

Refer to for example [Digital Ocean](https://django-storages.readthedocs.io/en/latest/backends/s3_compatible/digital-ocean-spaces.html) configuration if using a S3 compatible storage which isn't AWS.

Required to use S3 storage:

- `DMS_S3_ACCESS_KEY_ID`: AWS access key id
- `DMS_S3_SECRET_ACCESS_KEY`: AWS secret access key
- `DMS_STORAGE_BUCKET_NAME`: Storage bucket name

Optional:

- `DMS_S3_ENDPOINT_URL`: Custom S3 URL to use when connecting to S3, including scheme. (default: "")
- `DMS_S3_REGION_NAME`: Region of the storage (default: "")
- `DMS_LOCATION`: A path prefix that will be prepended to all uploads (default: "")
- `DMS_S3_FILE_OVERWRITE`: If `True` Files with the same name will overwrite each other. Otherwise extra characters are appended. (default: `False`)
- `DMS_S3_SIGNATURE_VERSION`: S3 signature version to use (default: `s2`)
- `DMS_S3_USE_SSL`: Whether or not to use SSL when connecting to S3 (default: `True`)
- `DMS_S3_VERIFY`: Whether or not to verify the connection to S3. Can be set to False to not verify SSL/TLS certificates. (default: `None`)
- `DMS_ENABLE_AT_REST_ENCRYPTION`: Whether to use SSEC to encrypt files uploaded to S3 (default: `False`)
- `DMS_S3_STORAGE_SSEC_SECRET`: Secret key for SSEC encryption, has to be 32 bytes long (default: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

## Gunicorn

Document Merge Service uses [Gunicorn](https://gunicorn.org/) as its app server.
A reasonable configuration is included in the docker image and can be customized
using the following environment variables:

- `GUNICORN_HOST`: IP address to bin gunicorn to (default `0.0.0.0`)
- `GUNICORN_PORT`: Port to bin gunicorn to (default `8000`)
- `GUNICORN_WORKERS`: Number of workers for handling requests (default `8`)
- `GUNICORN_TIMEOUT`: Number of seconds until worker processing a request is killed and restarted (default `60`)
- `GUNICORN_LIMIT_REQUEST_LINE`: Maximum size of HTTP request line in bytes (default `8190`)

If you want to further customize your configuration, you may do that by
overwriting the file [`document_merge_service/gunicorn.py`](document_merge_service/gunicorn.py)
and add your own custom settings:

```dockerfile
FROM ghcr.io/adfinis/document-merge-service:latest

COPY my_gunicorn_config.py /app/document_merge_service/gunicorn.py
```

Such a configuration file might look like this:

```python
# my_gunicorn_config.py

wsgi_app = "document_merge_service.wsgi:application" # must not be changed
bind = "0.0.0.0:80"
workers = 16
timeout = 120
loglevel = "debug"
```

For more information on how to customize Gunicorn, please refer to [the official documentation](https://docs.gunicorn.org/en/latest/settings.html).
