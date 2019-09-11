# Document Merge Service

[![Build Status](https://travis-ci.com/adfinis-sygroup/document-merge-service.svg?branch=master)](https://travis-ci.com/adfinis-sygroup/document-merge-service)
![Dependabot](https://badgen.net/dependabot/adfinis-sygroup/document-merge-service/?icon=dependabot)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/adfinis-sygroup/document-merge-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A document template merge service providing an API to manage templates and merge them with given data.

## Getting started

### Installation

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/adfinis-sygroup/document-merge-service/master/docker-compose.yml) and run the following command:

```bash
docker-compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) which includes a browsable api.

### Usage

Upload templates using the following:

```bash
curl --form template=@docx-template.docx --form name="Test Template" --form engine=docx-template http://localhost:8000/api/v1/template/
```

And merge template with:

```bash
curl -H "Content-Type: application/json" --data '{"data": {"test": "Test Input"}}' http://localhost:8000/api/v1/template/test-template/merge/ > output.docx
```

Additionally you can also convert output to pdf or other types supported by unoconv:

```bash
curl -H "Content-Type: application/json" --data '{"data": {"test": "Test Input"}, "convert": "pdf"}' http://localhost:8000/api/v1/template/test-template/merge/ > output.pdf
```

For this [unoconv service](#unoconv) needs to be configured.

### Supported engines

Following template engines are currently supported:

* [docx-template](https://github.com/elapouya/python-docx-template)
* [docx-mailmerge](https://github.com/Bouke/docx-mailmerge)

### Configuration

Document Merge Service is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

#### Common

* `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
* `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).

#### Database

Per default [Sqlite3](https://sqlite.org/) is used as database for simple deployment and stored at `/var/lib/document-merge-service/data/sqlite3.db`. Create a volume to make it persistent.

To scale the service a different database storage is needed. Any database supported by [Django](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE) can be used.

* `DATABASE_ENGINE`: Database backend to use.
* `DATABASE_HOST`: Host to use when connecting to database
* `DATABASE_PORT`: Port to use when connecting to database
* `DATABASE_NAME`: Name of database to use
* `DATABASE_USER`: Username to use when connecting to the database
* `DATABASE_PASSWORD`: Password to use when connecting to database

#### Unoconv

* `UNOCONV_ALLOWED_TYPES`: list of types allowed to convert to. See `unoconv --show` (default: ['pdf'])
* `UNOCONV_SERVER`: hostname or ip of unoconv listener. Defaults to `None`.
* `UNOCONV_PORT`: port of unoconv listener. Only relevant if `UNOCONV_SERVER` is set. Defaults to `2002`.
* `UNOCONV_PYTHON`: string defaults to "/usr/bin/python3.5"
* `UNOCONV_PATH`: string defaults to "/usr/bin/unoconv"

#### python-docx-template
* `DOCXTEMPLATE_JINJA_EXTENSIONS`: list of [jinja2 extensions](http://jinja.pocoo.org/docs/2.10/extensions/) to load

In python-docx-template following additional custom filters are implemented:

* multiline(value) - wraps the value in a [Listing](https://docxtpl.readthedocs.io/en/latest/#escaping-newline-new-paragraph-listing) for multiline support
* datetimeformat(value, format, locale)
* dateformat(value, format, locale)
* timeformat(value, format, locale)
* getwithdefault(value, default) - converts None to empty string (or provided default value) or leaves strings as is
* emptystring(value) - converts None to empty string or leaves strings as is (deprecated in favor of getwithdefault)

For formatting use babel and its uniode compatible [format](http://babel.pocoo.org/en/latest/dates.html#date-fields).

#### Authentication / Authorization

Per default no authentication is needed. To protect api, integrate it with your [IAM](https://en.wikipedia.org/wiki/Identity_management) supporting Open ID Connect. If not availbale you might consider using [Keycloak](https://www.keycloak.org/).

* `REQUIRE_AUTHENTICATION`: Force authentication to be required (default: False)
* `GROUP_ACCESS_ONLY`: Force visibility to templates of group only. See also `OIDC_GROUPS_CLAIM` or `OIDC_GROUPS_API` (default: False)
* `OIDC_USERINFO_ENDPOINT`: Url of userinfo endpoint as [described](https://openid.net/specs/openid-connect-core-1_0.html#UserInfo)
* `OIDC_VERIFY_SSL`: Verify ssl certificate of oidc userinfo endpoint (default: True)
* `OIDC_GROUPS_CLAIM`: Name of claim to be used to define group membership (default: document_merge_service_groups)
* `OIDC_GROUPS_API`: In case authorization is done in a different service than your OpenID Connect provider you may specify an API endpoint returning JSON which is called after authentication. Use `{sub}` as placeholder for username. Replace `sub` with any claim name. Example: https://example.net/users/{sub}/
* `OIDC_GROUPS_API_REVALIDATION_TIME`: Time in seconds before groups api is called again.
* `OIDC_GROUPS_API_VERIFY_SSL`: Verify ssl certificate of groups api endpoint (default: True)
* `OIDC_GROUPS_API_JSONPATH`: [Json path expression](https://goessner.net/articles/JsonPath/index.html) to match groups in json returned by `OIDC_GROUPS_API`. See also [JSONPath online evaluator](https://jsonpath.com/)
* `OIDC_GROUPS_API_HEADER`: List of headers which are passed on to groups api. (default: ['AUTHENTICATION'])
* `OIDC_BEARER_TOKEN_REVALIDATION_TIME`: Time in seconds before bearer token validity is verified again. For best security token is validated on each request per default. It might be helpful though in case of slow Open ID Connect provider to cache it. It uses [cache](#cache) mechanism for memorizing userinfo result. Number has to be lower than access token expiration time. (default: 0)

#### Cache

* `CACHE_BACKEND`: [cache backend](https://docs.djangoproject.com/en/1.11/ref/settings/#backend) to use (default: django.core.cache.backends.locmem.LocMemCache)
* `CACHE_LOCATION`: [location](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-CACHES-LOCATION) of cache to use

#### CORS
* `CORS_ORIGIN_ALLOW_ALL`: [allow all](https://github.com/ottoyiu/django-cors-headers#cors_origin_allow_all)
* `CORS_ORIGIN_REGEX_WHITELIST`: List of [whitelist regexes](https://github.com/ottoyiu/django-cors-headers#cors_origin_regex_whitelist) defaults to "^(https?://)?127\.0\.0\.1:\d{4}$"

Users of nginx/apache must ensure to have matching CORS configurations.

## Contributing

Look at our [contributing guidelines](CONTRIBUTIONG.md) to start with your first contribution.

## License

Code released under the [MIT license](LICENSE).
