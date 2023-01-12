# Migration from v5 to v6
**Warning**

The `group` attribute will be removed from the Template model.
A suggested migration would be to move the value to `meta` before migrating.

----

The previous pre-defined permission and visibility system was removed in favour of [dgap](https://github.com/adfinis/django-generic-api-permissions).

The integration of `OIDC_GROUPS_API` and `OIDC_GROUPS_API_JSONPATH` was removed with it.
Because every consuming app can now define its own way to handle the permissions.

Example Permissions:
```py
import requests
from rest_framework import exceptions
from generic_permissions.permissions import object_permission_for

from document_merge_service.models import Template


class CustomPermission:
    """
    Current settings and how to refactor them
    OIDC_GROUPS_API = "https://example.com/users/{sub}/group"
    OIDC_GROUPS_API_JSONPATH = "$$.included[?(@.type=='services')].id"
    """
    @object_permission_for(Template)
    def has_object_permission_template(self, request, instance):
        uri = "https://example.com/users/{sub}/group"
        # extract header
        token = request.headers["AUTHORIZATION"]

        # previously OIDC_GROUPS_API
        groups_api = f"https://example.com/users/{request.user.username}/group"

        response = requests.get(
            groups_api, verify=True, headers={"authorization": token}
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise exceptions.AuthenticationFailed(
                f"Retrieving groups from {uri} "
                f"failed with error '{str(e)}'."
            )

        result = response.json()

        # previously OIDC_GROUPS_API_JSONPATH was used here to extract the group from the response
        for data in result["included"]:
            if data.type == "services"
                groups = data.id

        return instance.meta["group"] in groups
```

After creating the permission define it in `settings.py` for dgap.
```py
GENERIC_PERMISSIONS_PERMISSION_CLASSES = ['app.permissions.CustomPermission']
```

Example Visibility:
```py
from django.db.models import Q
from generic_permissions.visibilities import filter_queryset_for

from document_merge_service.models import Template


class CustomVisibility:
    """Example Visibility class to replicate previous behaviour."""

    @filter_queryset_for(Template)
    def filter_templates(self, queryset, request):
        queryset = queryset.filter(
            Q(meta__group__in=self.request.user.groups or []) | Q(meta__group__isnull=True)
        )

        return queryset
```

After creating the visibility define it in `settings.py` for dgap.
```py
GENERIC_PERMISSIONS_VISIBILITY_CLASSES = ['app.visibilites.CustomVisibility']
```
