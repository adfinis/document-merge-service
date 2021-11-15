from django.urls import re_path
from rest_framework.routers import DefaultRouter

from . import views

r = DefaultRouter()

r.register("template", views.TemplateView)

urlpatterns = [
    re_path(
        r"^template-download/(?P<pk>.+)$",
        views.DownloadTemplateView.as_view(),
        name="template-download",
    )
]

urlpatterns.extend(r.urls)
