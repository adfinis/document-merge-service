FROM python:3.12-slim

# Needs to be set for users with manually set UID
ENV HOME=/home/document-merge-service

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=document_merge_service.settings
ENV APP_HOME=/app
ENV UWSGI_INI=/app/uwsgi.ini
ENV MEDIA_ROOT=/var/lib/document-merge-service/media
ENV DATABASE_DIR=/var/lib/document-merge-service/data

ARG UID=901

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
  --mount=type=cache,target=/var/cache/apt \
  apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libreoffice-writer \
    pkg-config \
    unoconv \
    util-linux \
    wait-for-it \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -U poetry

USER document-merge-service

ARG ENV=docker
COPY pyproject.toml poetry.lock $APP_HOME/
RUN if [ "$ENV" = "dev" ]; then poetry install --no-root --all-extras; else poetry install --no-root --all-extras --without dev; fi

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "poetry run python ./manage.py migrate && poetry run uwsgi"
