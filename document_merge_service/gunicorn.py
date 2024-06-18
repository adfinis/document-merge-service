wsgi_app = "document_merge_service.wsgi:application"
bind = "0.0.0.0:8000"
workers = 8
proc_name = "dms"
timeout = 60
