from django.conf import settings
from django.urls import include, re_path

urlpatterns = [
    re_path(
        f"^{settings.URL_PREFIX}api/v1/", include("document_merge_service.api.urls")
    )
]
