FROM python:3.12 AS build

ARG ENV=docker

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_HOME=/opt/poetry
ENV APP_HOME=/app

WORKDIR $APP_HOME

RUN pip install -U poetry

# Install project dependencies
COPY pyproject.toml poetry.lock $APP_HOME/
RUN \
  --mount=type=cache,target=.cache/pypoetry \
  poetry install --no-root --all-extras $(test "$ENV" = "dev" && echo "--with dev")

# Install project itself
COPY . $APP_HOME
RUN \
  --mount=type=cache,target=.cache/pypoetry \
  poetry install --only-root

FROM python:3.12-slim

ARG UID=901

# Needs to be set for users with manually set UID
ENV HOME=/home/document-merge-service
ENV DJANGO_SETTINGS_MODULE=document_merge_service.settings
ENV UWSGI_INI=/app/uwsgi.ini
ENV MEDIA_ROOT=/var/lib/document-merge-service/media
ENV DATABASE_DIR=/var/lib/document-merge-service/data

WORKDIR $APP_HOME

RUN mkdir -p $APP_HOME $DATABASE_DIR/tmp $MEDIA_ROOT /var/www/static \
  && useradd -u $UID -r document-merge-service --create-home \
  && mkdir $HOME/.config \
  && chmod -R 770 $DATABASE_DIR $MEDIA_ROOT $HOME /var/www/static \
  # All project specific folders need to be accessible by newly created user but
  # also for unknown users (when UID is set manually). Such users are in group
  # root.
  && chown -R document-merge-service:root $DATABASE_DIR $MEDIA_ROOT $HOME /var/www/static

RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    libreoffice-writer \
    unoconv \
    util-linux \
    wait-for-it \
  && rm -rf /var/lib/apt/lists/*

USER document-merge-service

COPY --from=build /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/

EXPOSE 8000

COPY . $APP_HOME

CMD ["/bin/sh", "-c", "./manage.py migrate && uwsgi"]
