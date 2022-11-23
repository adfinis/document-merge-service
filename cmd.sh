#!/bin/sh

GUNICORN_WORKERS="${GUNICORN_WORKERS:-8}"

poetry run gunicorn --workers=$GUNICORN_WORKERS --bind=0.0.0.0:8000 document_merge_service.wsgi:application
