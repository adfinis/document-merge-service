import os

wsgi_app = "document_merge_service.wsgi:application"
bind = f"{os.environ.get('GUNICORN_HOST', '0.0.0.0')}:{os.environ.get('GUNICORN_PORT', 8000)}"
workers = os.environ.get("GUNICORN_WORKERS", 8)
proc_name = "document-merge-service"
timeout = os.environ.get("GUNICORN_TIMEOUT", 60)
limit_request_line = os.environ.get("GUNICORN_LIMIT_REQUEST_LINE", 8190)
