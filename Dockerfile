FROM python:3.6

WORKDIR /app

RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
&& chmod +x /usr/local/bin/wait-for-it.sh \
&& mkdir -p /app /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static \
&& chmod 770 /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static \
&& groupadd -r document_merge_service -g 901 && useradd -u 901 -r -g 901 document_merge_service

ARG REQUIREMENTS=requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE document_merge_service.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini
ENV STATIC_ROOT /var/www/static
ENV MEDIA_ROOT /var/lib/document-merge-service/media

COPY requirements.txt requirements-dev.txt $APP_HOME/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

COPY . $APP_HOME

RUN ENV=docker ./manage.py collectstatic --noinput

USER document_merge_service
EXPOSE 8000

CMD /bin/sh -c "./manage.py migrate && uwsgi"
