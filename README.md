# Document Merge Service

[![Build Status](https://github.com/adfinis/document-merge-service/actions/workflows/tests.yml/badge.svg)](https://github.com/adfinis/document-merge-service/actions/workflows/tests.yml)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/adfinis/document-merge-service)
[![License: GPL-3.0-or-later](https://img.shields.io/github/license/adfinis/document-merge-service)](https://spdx.org/licenses/GPL-3.0-or-later.html)

A document template merge service providing an API to manage templates and merge them with given data. It can also be used to convert Docx files to PDF.

## Installation

**Requirements**

- docker
- docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/adfinis/document-merge-service/master/docker-compose.yml) and run the following command:

```bash
docker-compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) which includes a browsable api.

### Workaround LibreOffice lockup

The workaround has a setting called `ISOLATE_UNOCONV`, it is only enabled in the
development environment. If `ISOLATE_UNOCONV` is enabled the container needs
`CAP_SYS_ADMIN`. See docker-compose.override.yml.

```yaml
cap_add:
  - CAP_SYS_ADMIN
security_opt:
  - apparmor:unconfined
environment:
  - ISOLATE_UNOCONV=true
```

### Custom Gunicorn configuration

Document Merge Service uses [Gunicorn](https://gunicorn.org/) as its app server. A reasonable configuration is included in the docker image. However, if you want to customize your configuration, you may do that by overwriting the file [`document_merge_service/gunicorn.py`](document_merge_service/gunicorn.py) and add your own custom settings:

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
```

For more information on how to customize Gunicorn, please refer to [the official documentation](https://docs.gunicorn.org/en/latest/settings.html).

## Getting started

### Uploading templates

Upload templates using the following:

```bash
curl --form template=@docx-template.docx --form name="Test Template" --form engine=docx-template http://localhost:8000/api/v1/template/
```

### Merging a template

After uploading successfully, you can merge a template with the following call:

```bash
curl -H "Content-Type: application/json" --data '{"data": {"test": "Test Input"}}' http://localhost:8000/api/v1/template/test-template/merge/ > output.docx
```

### Converting a template

To convert a standalone Docx file the following call can be used:

```bash
curl -X POST --form file=@my-test-file.docx --form target_format="pdf" http://localhost:8000/api/v1/convert > example.pdf
```

## Further reading

- [Configuration](CONFIGURATION.md) - Further configuration and how to do a production setup
- [Usage](USAGE.md) - How to use the DMS and it's features
- [Contributing](CONTRIBUTING.md) - Look here to see how to start with your first
  contribution. Contributions are welcome!

## License

Code released under the [GPL-3.0-or-later license](LICENSE).
