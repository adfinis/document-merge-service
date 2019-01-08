import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from jose import ExpiredSignatureError, JWTError, jwt
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
    def __init__(self, decoded_token):
        self.username = decoded_token["sub"]
        self.groups = decoded_token.get(settings.OIDC_GROUPS_CLAIM) or []

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username


class OIDCAuthentication(authentication.BaseAuthentication):
    header_prefix = "Bearer"

    def get_jwt_value(self, request):
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

    def get_json(self, url):
        response = requests.get(url, verify=settings.OIDC_VERIFY_SSL)
        response.raise_for_status()
        return response.json()

    def decode_token(self, token, key):
        return jwt.decode(
            token=token,
            key=key,
            options=settings.OIDC_VALIDATE_CLAIMS_OPTIONS,
            algorithms=[settings.OIDC_VERIFY_ALGORITHM],
            audience=settings.OIDC_CLIENT,
        )

    def keys(self):
        if settings.OIDC_VERIFY_ALGORITHM.startswith("RS"):
            return self.get_json(settings.OIDC_JWKS_ENDPOINT)
        return settings.OIDC_SECRET_KEY

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        for retry in range(2):
            try:
                decoded_token = self.decode_token(
                    jwt_value,
                    cache.get_or_set("authentication.keys", self.keys, timeout=None),
                )
            except ExpiredSignatureError:
                msg = _("Invalid Authorization header. JWT has expired.")
                raise exceptions.AuthenticationFailed(msg)
            except JWTError:
                if retry == 0 and settings.OIDC_VERIFY_ALGORITHM.startswith("RS"):
                    # try again with refreshed keys
                    cache.delete("authentication.keys")
                    continue

                msg = _("Invalid Authorization Token.")
                raise exceptions.AuthenticationFailed(msg)

        return OIDCUser(decoded_token), decoded_token

    def authenticate_header(self, request):
        return f"{self.header_prefix} realm={settings.OIDC_CLIENT}"
