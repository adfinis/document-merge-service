from django.conf import settings
from rest_framework import permissions


class AsConfigured(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if settings.REQUIRE_AUTHENTICATION:
            return super().has_permission(request, view)
        return True
