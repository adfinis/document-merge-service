FROM python:3.10

WORKDIR /app

ARG UID=901

RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
  && chmod +x /usr/local/bin/wait-for-it.sh \
  && mkdir -p /app /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static \
  && useradd -u $UID -r document-merge-service --create-home \
  && mkdir /home/document-merge-service/.config \
  && chmod -R 770 /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static /home/document-merge-service \
  && apt-get update && apt-get install -y --no-install-recommends util-linux unoconv libreoffice-writer && rm -rf /var/lib/apt/lists/* \
  # All project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
  && chown -R document-merge-service:root /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static /home/document-merge-service
RUN pip install poetry

# Needs to be set for users with manually set UID
ENV HOME=/home/document-merge-service
USER document-merge-service

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE document_merge_service.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini
ENV MEDIA_ROOT /var/lib/document-merge-service/media

ARG ENV=docker
COPY pyproject.toml poetry.lock $APP_HOME/
RUN poetry install $([ "$ENV" = "dev" ] || echo "--no-dev") --no-interaction --no-ansi
COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "poetry run python ./manage.py migrate && poetry run python uwsgi"
