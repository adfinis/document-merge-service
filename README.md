# Document Merge Service

[![Build Status](https://travis-ci.com/adfinis-sygroup/document-merge-service.svg?branch=master)](https://travis-ci.com/adfinis-sygroup/document-merge-service)
![Dependabot](https://badgen.net/dependabot/adfinis-sygroup/document-merge-service/?icon=dependabot)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/adfinis-sygroup/document-merge-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A document template merge service providing an API to manage templates and merge them with given data.

## Installation

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/adfinis-sygroup/document-merge-service/master/docker-compose.yml) and run the following command:

```bash
docker-compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) which includes a browsable api.


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


## Further reading

* [Configuration](CONFIGURATION.md) - Further configuration and how to do a production setup
* [Usage](USAGE.md) - How to use the DMS and it's features
* [Contributing](CONTRIBUTING.md) - Look here to see how to start with your first
  contribution. Contributions are welcome!

## License

Code released under the [MIT license](LICENSE).
