FROM python:3.6

WORKDIR /app

RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
  && chmod +x /usr/local/bin/wait-for-it.sh \
  && mkdir -p /app \
&& groupadd -r document_merge_service -g 901 && useradd -u 901 -r -g 901 document_merge_service

ARG REQUIREMENTS=requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE document_merge_service.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini

COPY requirements.txt requirements-dev.txt $APP_HOME/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

USER document_merge_service

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && uwsgi"
