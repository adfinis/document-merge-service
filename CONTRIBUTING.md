# Contributing

Contributions to Document Merge Service are very welcome! Best have a look at the open [issues](https://github.com/adfinis/document-merge-service/issues)
and open a [GitHub pull request](https://github.com/adfinis/document-merge-service/compare). See instructions below how to setup development
environment. Before writing any code, best discuss your proposed change in a GitHub issue to see if the proposed change makes sense for the project.

## Setup development environment

### Clone

To work on Document Merge Service you first need to clone

```bash
git clone https://github.com/adfinis/document-merge-service.git
cd document-merge-service
```

### Open Shell

Once it is cloned you can easily open a shell in the docker container to
open an development environment.

```bash
# needed for permission handling
# only needs to be run once
echo UID=$UID > .env
# open shell
docker-compose run --rm document-merge-service bash
```

### Testing

Once you have shelled in docker container as described above
you can use common python tooling for formatting, linting, testing
etc.

```bash
poetry shell
# linting
flake8
# format code
black .
# running tests
pytest
# create migrations
./manage.py makemigrations
# install debugger or other temporary dependencies
pip install --user pdbpp
```

Writing of code can still happen outside the docker container of course.

### Install new requirements

In case you're adding new requirements you simply need to build the docker container
again for those to be installed and re-open shell.

```bash
docker-compose build --pull
```

### Setup pre commit

Pre commit hooks is an additional option instead of executing checks in your editor of choice.

First create a virtualenv with the tool of your choice before running below commands:

```bash
poetry shell
pip install pre-commit
pre-commit install --hook=pre-commit
pre-commit install --hook=commit-msg
```

This will activate commit hooks to validate your code as well as your commit
messages.

### Setup commit-msg hook
If you want to have your commit message automatically linted, execute below commands:

```bash
npm install @commitlint/{config-conventional,cli}
ln -s "$(pwd)/commit-msg" .git/hooks/commit-msg
```
