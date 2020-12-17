# Usage

This guide is intended to help you make full use of the DMS.

All the examples here will use Python 3 with the `requests` module, as it
produces very redable and understandable code. Adaptation into other languages
should be fairly simple.

## Basic principles

### General operation

DMS mainly has two distinct operations: Uploading a template, and merging it
with some data to generate a document.

#### Supported engines

To be able to render (generate) a document, you first need to upload a
template.  DMS currently supports two formats: Mail Merge, and DocxTpl,
which in turn uses Jinja2 syntax. You can read more about them here:

* [docx-template](https://github.com/elapouya/python-docx-template)
* [docx-mailmerge](https://github.com/Bouke/docx-mailmerge)

Mail Merge uses placeholders in the office format. This means that the
placeholders are defined using the features of your office suite via
the mail merge functionality.  If you only need to fill in some values,
and don't need conditional values, this is the format for you.

The DocxTpl format enables you to put the placeholders directly in
text. This has several advantages and disadvantages:

* Since office formats can put markup anywhere in the text, it may happen that
  identifiers or other template syntax gets split up without the user noticing,
  leading to hard-to-debug syntax errors.
* However, due to the representation as text, we gain the flexibility to add
  loops, conditionals and so on to change the output document depending on the
  data that's filled in.


### Authentication / Authorization

By default no authentication is needed. To protect the API, integrate it with your
[IAM](https://en.wikipedia.org/wiki/Identity_management) supporting Open ID Connect. If not
already available, you might consider using [Keycloak](https://www.keycloak.org/).

When you enable authentication, all access must be with a valid OIDC token.
Authenticated users are able to upload and merge templates, but anonymous users
won't be anymore.

You can configure the DMS to allow users to only see templates created by other
people in the same group (by enabling the setting `GROUP_ACCESS_ONLY`).

Any further restriction is currently not possible. If you have the need for
further rules, please open an issue (or a pull request) on Github, so we can
have a discussion and extend the authorization process accordingly.

For the full details on how to configure it, see the
[configuration guide](CONFIGURATION.md).


## Uploading templates

Upload templates using the following example code:

```python
>>> import requests
>>> import json
>>> resp = requests.post(
...     'http://localhost:8000/api/v1/template/',
...     data={
...         'engine': 'docx-mailmerge',
...         'slug': 'my-template',
...         'name': 'test template'
...     },
...     files={
...         'template': open('docx-mailmerge.docx', 'rb')
...     }
... )
>>> print(resp.status_code)
201
```

The upload is using the `Content-Disposition: form-data` format, commonly used
in traditional forms when uploading files from a browser.
Make sure you pass in all required fields:

* `engine`: either `docx-mailmerge` or `docx-template`, depending on your
  template type
* `slug`: Identifier of your template. May only be used once and is your
  primary key for accessing the templates later on.
* `name`: Display name of the template
* `template`: The actual template file. Make sure you pass it in the
  right format that your HTTP library uses.

In the following examples, I'm assuming you already did the `import`
statements for the `requests` and `json` modules, so I'm not repeating it.

### Validating the template's structure and placeholders

Most times, you already know the placeholders available in the template when
uploading the template. To ensure that the template will render properly, you
can validate the template's syntax and placeholder usage at the upload stage.

The DMS provides two ways to do this: Either by providing some sample data,
or by providing a simplified list of variables.

The list of variables is using the following syntax:

* For simple variables, just mention the variable name, such as `foo`
* For lists, add square brackets after the variable name, for example `a_list[]`
* For nested objects, use "dot notation": `object.property`

You may also combine this syntax according to your needs. The following are all
valid examples:

* `foo.bar`
* `a_list[].inner_property`
* `a_list[].another_property`
* `list[].nested_list[]`

The template used here uses a single placeholder named `test`. See what
happens if we enable placeholder validation but tell the DMS that only
some some other placeholders are available:

```python
>>> resp = requests.post(
...     'http://localhost:8000/api/v1/template/',
...     data={
...         'engine': 'docx-template',
...         'slug': 'my-validated-template',
...         'name': 'test template',
...         'available_placeholders': [
...             'foo', 'bar', 'baz'
...         ]
...     },
...     files={
...         'template': open('docx-template.docx', 'rb')
...     }
... )
>>> print(resp.status_code)
400
>>> print(resp.json())
{'non_field_errors': ['Template uses unavailable placeholders: test']}
```

The above example uses the DocxTpl syntax, so the template is validated
for this (See the parameter `"engine": "docx-template"`).

You can also provide sample data to fulfill the same purpose. If you do this,
the DMS will implicitly generate the list as above from the data, but it will
also try to render the template using the sample data given. Both have to
work correctly for the upload to succeed.

As the document may have some structure, it needs to be JSON encoded as the
upload is using the `Content-Disposition: form-data` format.

```python
>>> resp = requests.post(
...     'http://localhost:8000/api/v1/template/',
...     data={
...         'engine': 'docx-mailmerge',
...         'slug': 'my-validated-template',
...         'name': 'test template',
...         'sample_data': json.dumps({
...              'foo': 'a value',
...              'test': 'another value'
...         })
...     },
...     files={
...         'template': open('docx-mailmerge.docx', 'rb')
...     }
... )
>>> print(resp.status_code)
201
>>> print(resp.json())
{'slug': 'my-validated-template', 'description': '', 'template':
'http://localhost:8000/api/v1/template/docx-mailmerge_uZCLTeY.docx', 'engine':
'docx-mailmerge', 'group': '[]', 'available_placeholders': None, 'sample_data':
None}
```

As you can see, the validation went through this time, as our sample data
covers all placeholders used in the template. Of course, the template
isn't required to use all placeholders available!

If you use a Template with the DocxTpl syntax that uses [inline images](#inline-images),
you also need to include the corresponding files along the `sample_data`. So the `files`
in the example above would become something like:

```python
...     files=(
...         ("template", open('docx-mailmerge.docx', 'rb'))),
...         ("files", ("sunset1.png", open('sunset1.png', 'rb'))),
...         ("files", ("sunset2.png", open('sunset2.png', 'rb'))),
...     ),
```

### Disabling template validation

Sometimes, templates contain advanced syntax that cannot be correctly validated
by the automatic mechanism. If you at the same time are also unable to provide
usable sample data, you can disable template validation entirely.

Please note that in this case, templates will be accepted that may cause errors
when actually used, so make sure to test them after uploading!

To disable template validation, pass in the additional parameter
`disable_template_validation` with the value `true` on template upload.


## Merging templates

In contrast to uploading templates, requests for merging documents uses JSON
as transfer format. Make sure you set the correct HTTP headers and encode your
data.

```python
>>> resp = requests.post(
...     'http://localhost:8000/api/v1/template/my-validated-template/merge/',
...     json={
...         'data': {
...              'foo': 'a value',
...              'test': 'another value'
...         }
...     }
... )
>>> print(resp.status_code)
200
>>> with open('rendered_document.docx', 'wb') as fh:
...     fh.write(resp.content)
9673
```

Merging works the same for both engines, so this is basically all you need to
know about how to use the DMS.

Additionally, you can also convert output to pdf or other types supported by unoconv:

```python
>>> resp = requests.post(
...     'http://localhost:8000/api/v1/template/my-validated-template/merge/',
...     json={
...         'data': {
...              'foo': 'a value',
...              'test': 'another value'
...         },
...         'convert': 'pdf'
...     }
... )
>>> print(resp.status_code)
200
>>> with open('rendered_document.pdf', 'wb') as fh:
...     fh.write(resp.content)
5031
```

## Inline images

The `docx-template` engine supports including inline images. Here is shown how one can
use this feature.

1. Include an image variable with the `image` filter: `{{ 'sunset.png' | image(50, 50) }}`
2. Include the image files into a multipart request to the `merge` endpoint:

```python
>>> resp = requests.post(
...     'http://localhost:8000/api/v1/template/my-template/merge/',
...     data={
...         'data': json.dumps({
...              'foo': 'a value',
...              'test': 'another value'
...         }),
...         'convert': 'pdf'
...     },
...     files=(
...         ("files", ("sunset.png", open('sunset.png', 'rb'))),
...     ),
... )
```

The value passed to the `image` filter must be identical to the name of a file that has been provided.

If you want to merge a template with an image placeholder, but you don't want to render
the image, you can add the filename as key to `data` and set it to `None` or `""`. In the
example above, `data` would look like this:

```python
...     data={
...         'data': json.dumps({
...              'foo': 'a value',
...              'test': 'another value',
...              'sunset.png': None
...         }),
...         'convert': 'pdf'
...     },
```

## Maintenance / Cleanup

The DMS allows REST verbs like `PATCH` and `DELETE` for updating and deleting
existing templates:

```python
>>> resp = requests.delete(
...     'http://localhost:8000/api/v1/template/my-validated-template',
... )
>>> print(resp.status_code)
204
```
