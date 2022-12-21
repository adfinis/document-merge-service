import inspect

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .collections import list_duplicates
from .models import Template

class AllowAny(BasePermission):
    pass


class IsAuthenticated(BasePermission):
    """
    Allow access only to authenticated users.

    You can either use this in combination with your own permission
    classes, or inherit from it if you want *some* models to be accessible
    publicly.
    """

    @permission_for(Template)
    def base_permission(self, request):
        return request.user.is_authenticated

    @object_permission_for(Template)
    def base_object_permission(self, request, instance):
        return self.base_permission(request)


class AsConfigured(IsAuthenticated):
    @permission_for(Template)
    def base_permission(self, request):
        if settings.REQUIRE_AUTHENTICATION:
            return super().base_permission(request)
        return True

    @object_permission_for(Template)
    def base_object_permission(self, request, instance):
        if settings.REQUIRE_AUTHENTICATION:
            return super().base_object_permission(request, instance)
        return True
