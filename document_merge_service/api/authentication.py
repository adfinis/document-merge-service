import functools

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import smart_text
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


class OIDCUser(AnonymousUser):
    def __init__(self, userinfo):
        self.username = userinfo["sub"]
        self.groups = userinfo.get(settings.OIDC_GROUPS_CLAIM) or []

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

    def authenticate(self, request):
        token = self.get_bearer_token(request)
        if token is None:
            return None

        userinfo_method = functools.partial(self.get_userinfo, token=token)
        userinfo = cache.get_or_set(
            f"authentication.userinfo.{smart_text(token)}", userinfo_method
        )

        return OIDCUser(userinfo), token

    def authenticate_header(self, request):
        return f"{self.header_prefix} realm={settings.OIDC_USERINFO_ENDPOINT}"
