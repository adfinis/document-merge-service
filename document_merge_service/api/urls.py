from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

r = DefaultRouter()

r.register("template", views.TemplateView)

urlpatterns = [
    url(
        r"^template/(?P<template>.+\..+)$",
        views.DownloadTemplateView.as_view(),
        name="template-download",
    )
]

urlpatterns.extend(r.urls)
