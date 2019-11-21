FROM python:3.8.0

WORKDIR /app

ARG UNOCONV_LOCAL=false
ARG UID=901

RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
&& chmod +x /usr/local/bin/wait-for-it.sh \
&& mkdir -p /app /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static \
&& useradd -u $UID -r document-merge-service --create-home \
&& mkdir /home/document-merge-service/.config \
&& chmod -R 770 /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static /home/document-merge-service \
&& bash -c 'if [ "$UNOCONV_LOCAL" = true ]; then apt-get update && apt-get install -y --no-install-recommends unoconv libreoffice-writer && rm -rf /var/lib/apt/lists/*; fi' \
# all project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
&& chown -R document-merge-service:root /var/lib/document-merge-service/data /var/lib/document-merge-service/media /var/www/static /home/document-merge-service

# needs to be set for users with manually set UID
ENV HOME=/home/document-merge-service

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE document_merge_service.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini
ENV STATIC_ROOT /var/www/static
ENV MEDIA_ROOT /var/lib/document-merge-service/media

ARG REQUIREMENTS=requirements.txt
COPY requirements.txt requirements-dev.txt $APP_HOME/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check
COPY . $APP_HOME

RUN ENV=docker ./manage.py collectstatic --noinput \
&& chown -R document-merge-service:root /var/www/static \
&& chmod 770 -R /var/www/static

USER document-merge-service
EXPOSE 8000

CMD /bin/sh -c "./manage.py migrate && uwsgi"
