FROM python:3.14-bookworm AS build

ARG ENV=docker
ARG APP_HOME=/app
ARG VARIANT=slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_HOME=/opt/poetry

WORKDIR $APP_HOME

RUN pip install --no-cache-dir -U poetry

# Install project dependencies
COPY pyproject.toml poetry.lock $APP_HOME/
RUN \
  --mount=type=cache,target=.cache/pypoetry \
  poetry install --no-root --extras $VARIANT $(test "$ENV" = "dev" && echo "--with dev")

# Install project itself
COPY . $APP_HOME
RUN \
  --mount=type=cache,target=.cache/pypoetry \
  poetry install --only-root

FROM python:3.14-slim-bookworm

ARG UID=901
ARG APP_HOME=/app

# Needs to be set for users with manually set UID
ENV HOME=/home/document-merge-service
ENV DJANGO_SETTINGS_MODULE=document_merge_service.settings
ENV MEDIA_ROOT=/var/lib/document-merge-service/media
ENV DATABASE_DIR=/var/lib/document-merge-service/data
# Compat setup: setuptools to take over the 'distutils' namespace
# TODO: remove when migrated away from unoconv
ENV SETUPTOOLS_USE_DISTUTILS=local

# Suppress noisy warning caused by xltpl: https://github.com/zhangyu836/xltpl/issues/27
ENV PYTHONWARNINGS="ignore:invalid escape sequence:SyntaxWarning"

RUN mkdir -p $APP_HOME $DATABASE_DIR/tmp $MEDIA_ROOT /var/www/static \
  && useradd -u $UID -r document-merge-service --create-home \
  && mkdir $HOME/.config \
  && chmod -R 770 $DATABASE_DIR $MEDIA_ROOT $HOME /var/www/static \
  # All project specific folders need to be accessible by newly created user but
  # also for unknown users (when UID is set manually). Such users are in group
  # root.
  && chown -R document-merge-service:root $DATABASE_DIR $MEDIA_ROOT $HOME /var/www/static

WORKDIR $APP_HOME

RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    libreoffice-writer \
    unoconv \
    util-linux \
    wait-for-it \
  && rm -rf /var/lib/apt/lists/*

USER document-merge-service

COPY --from=build /usr/local/lib/python3.14/site-packages/ /usr/local/lib/python3.14/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/

EXPOSE 8000

COPY . $APP_HOME

CMD ["/bin/sh", "-c", "./manage.py migrate && gunicorn -c ./document_merge_service/gunicorn.py"]
