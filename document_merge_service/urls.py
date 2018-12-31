from django.conf.urls import include, url

urlpatterns = [url(r"^api/v1/", include("document_merge_service.api.urls"))]
