import functools
import hashlib

import jsonpath
import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_bytes, smart_text
from django.utils.translation import ugettext as _
from rest_framework import authentication, exceptions


class AnonymousUser(object):
    def __init__(self):
        self.username = None
        self.groups = []

    @property
    def group(self):
        return self.groups and self.groups[0]

    @property
    def is_authenticated(self):
        return False

    def __str__(self):
        return "AnonymousUser"


class AuthenticatedUser(AnonymousUser):
    def __init__(self, username, groups):
        self.username = username
        self.groups = groups

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username


class BearerTokenAuthentication(authentication.BaseAuthentication):
    header_prefix = "Bearer"

    def get_bearer_token(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth:
            return None

        if smart_text(auth[0].lower()) != self.header_prefix.lower():
            raise exceptions.AuthenticationFailed(_("No Bearer Authorization header"))

        if len(auth) == 1:
            msg = _("Invalid Authorization header. No credentials provided")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                "Invalid Authorization header. Credentials string should "
                "not contain spaces."
            )
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def get_userinfo(self, token):
        response = requests.get(
            settings.OIDC_USERINFO_ENDPOINT,
            verify=settings.OIDC_VERIFY_SSL,
            headers={"Authorization": f"Bearer {smart_text(token)}"},
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise exceptions.AuthenticationFailed(
                f"Retrieving userinfo from {settings.OIDC_USERINFO_ENDPOINT} "
                f"failed with error '{str(e)}'."
            )

        return response.json()

    def get_groups_from_api(self, request, userinfo):
        headers = {
            key: value
            for key, value in request.headers.items()
            if key.upper() in settings.OIDC_GROUPS_API_HEADERS
        }

        # replace placeholders
        groups_api = settings.OIDC_GROUPS_API
        placeholders = {k: v for k, v in userinfo.items() if isinstance(v, str)}
        for key, value in placeholders.items():
            groups_api = groups_api.replace("{" + key + "}", value)

        response = requests.get(
            groups_api, verify=settings.OIDC_GROUPS_API_VERIFY_SSL, headers=headers
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise exceptions.AuthenticationFailed(
                f"Retrieving groups from {settings.OIDC_GROUPS_API} "
                f"failed with error '{str(e)}'."
            )

        result = response.json()
        return jsonpath.jsonpath(result, settings.OIDC_GROUPS_API_JSONPATH)

    def authenticate(self, request):
        token = self.get_bearer_token(request)
        if token is None:
            return None

        userinfo_method = functools.partial(self.get_userinfo, token=token)
        # token might be too long for key so we use hash sum instead.
        hashsum_token = hashlib.sha256(force_bytes(token)).hexdigest()
        userinfo = cache.get_or_set(
            f"authentication.userinfo.{hashsum_token}",
            userinfo_method,
            timeout=settings.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )

        # retrieve groups
        groups = []
        if settings.OIDC_GROUPS_CLAIM:
            groups = userinfo[settings.OIDC_GROUPS_CLAIM]
        elif settings.OIDC_GROUPS_API:
            groups_api_method = functools.partial(
                self.get_groups_from_api, userinfo=userinfo, request=request
            )
            groups = cache.get_or_set(
                f"authentication.groups.{hashsum_token}",
                groups_api_method,
                timeout=settings.OIDC_GROUPS_API_REVALIDATION_TIME,
            )

        return AuthenticatedUser(userinfo["sub"], groups), token

    def authenticate_header(self, request):
        return f"{self.header_prefix} realm={settings.OIDC_USERINFO_ENDPOINT}"
