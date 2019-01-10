# Document Merge Service

[![Build Status](https://travis-ci.com/adfinis-sygroup/document-merge-service.svg?branch=master)](https://travis-ci.com/adfinis-sygroup/document-merge-service)
[![Pyup](https://pyup.io/repos/github/adfinis-sygroup/document-merge-service/shield.svg)](https://pyup.io/account/repos/github/adfinis-sygroup/document-merge-service/)
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

Per default [Sqlite3](https://sqlite.org/) is used as database for simple deployment. To scale service a different database storage is needed. Any database supported by [Django](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE) can be used.

* `DATABASE_ENGINE`: Database backend to use.
* `DATABASE_HOST`: Host to use when connecting to database
* `DATABASE_PORT`: Port to use when connecting to database
* `DATABASE_NAME`: Name of database to use
* `DATABASE_USER`: Username to use when connecting to the database
* `DATABASE_PASSWORD`: Password to use when connecting to database

#### Unoconv

* `UNOCONV_URL`: url to [tfk-api-unoconv service](https://github.com/zrrrzzt/tfk-api-unoconv) (e.g. http://localhost:3000)
* `UNOCONV_ALLOWED_TYPES`: list of types allowed to convert to. See [supported formats](https://github.com/zrrrzzt/tfk-api-unoconv#formats) (default: ['pdf'])

#### Authentication / Authorization

Per default no authentication is needed. To protect api, integrate it with your [IAM](https://en.wikipedia.org/wiki/Identity_management) supporting Open ID Connect. If not availbale you might consider using [Keycloak](https://www.keycloak.org/).

* `REQUIRE_AUTHENTICATION`: Force authentication to be required (default: False)
* `GROUP_ACCESS_ONLY`: Force visibility to templates of group only. See also `OIDC_GROUPS_CLAIM`. (default: False)
* `OIDC_USERINFO_ENDPOINT`: Url of userinfo endpoint as [described](https://openid.net/specs/openid-connect-core-1_0.html#UserInfo)
* `OIDC_GROUPS_CLAIM`: Name of claim to be used to define group membership (default: document_merge_service_groups)
* `OIDC_BEARER_TOKEN_REVALIDATION_TIME`: Time in seconds before bearer token validity is verified again. For best security token is validated on each request per default. It might be helpful though in case of slow Open ID Connect provider to cache it. It uses [cache](#cache) mechanism for memorizing userinfo result. Number has to be lower than access token expiration time. (default: 0)

#### Cache

* `CACHE_BACKEND`: [cache backend](https://docs.djangoproject.com/en/1.11/ref/settings/#backend) to use (default: django.core.cache.backends.locmem.LocMemCache)
* `CACHE_LOCATION`: [location](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-CACHES-LOCATION) of cache to use

## Contributing

Look at our [contributing guidelines](CONTRIBUTION.md) to start with your first contribution.

## License

Code released under the [MIT license](LICENSE).
