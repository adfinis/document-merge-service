import functools
import hashlib

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_bytes, smart_str
from django.utils.translation import gettext as _
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
    def __init__(self, userinfo):
        self.username = userinfo["sub"]
        groups = []
        if settings.OIDC_GROUPS_CLAIM:
            groups = userinfo[settings.OIDC_GROUPS_CLAIM]
        self.groups = groups
        self.userinfo = userinfo

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

        if smart_str(auth[0].lower()) != self.header_prefix.lower():
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
            headers={"Authorization": f"Bearer {smart_str(token)}"},
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise exceptions.AuthenticationFailed(
                f"Retrieving userinfo from {settings.OIDC_USERINFO_ENDPOINT} "
                f"failed with error '{str(e)}'."
            )

        return response.json()

    def authenticate(self, request):
        if not settings.REQUIRE_AUTHENTICATION:
            return None

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

        return (
            AuthenticatedUser(userinfo),
            token,
        )

    def authenticate_header(self, request):
        return f"{self.header_prefix} realm={settings.OIDC_USERINFO_ENDPOINT}"
