import json
import time

import pytest
from django.conf import settings
from jose import jwt
from rest_framework import exceptions

from .. import authentication

KEYS = {
    "keys": [
        {
            "kty": "RSA",
            "alg": "RS256",
            "use": "sig",
            "kid": "3e52a77bd1b480d14e070fcd40554f79",
            "n": "7P5mh6TCYUPFPAeig-3ZqaqGgXnQuNcRGNowCgAUg8XJ2mfL0F07M27hTOmJIv15j68s3tkk1MEOy4xq436ArgKfy7utrTzOf9kC9maVg1w1RwXiprVzRAR0yM3gfn3hAlQ2TBaI7_ICasJgXpM1BC6q-baLUy9DqobhoprqpvE",
            "e": "AQAB",
        }
    ]
}


def expired_token():
    token = {
        "iss": settings.OIDC_JWKS_ENDPOINT,
        "sub": "1",
        "aud": settings.OIDC_CLIENT,
        "exp": time.time() - 60 * 60 * 24,
    }

    return f'Bearer {jwt.encode(token, settings.OIDC_SECRET_KEY, algorithm="HS256")}'


def valid_token():
    token = {
        "iss": settings.OIDC_JWKS_ENDPOINT,
        "sub": "1",
        "aud": settings.OIDC_CLIENT,
        "exp": time.time() + 60 * 60 * 24,
        settings.OIDC_GROUPS_CLAIM: ["test"],
    }

    return f'Bearer {jwt.encode(token, settings.OIDC_SECRET_KEY, algorithm="HS256")}'


@pytest.mark.parametrize(
    "token,algorithm,error",
    [
        ("", "", False),
        ("Bearer", "RS256", True),
        ("Bearer Too many params", "RS256", True),
        ("Basic Auth", "", True),
        ("Bearer InvalidToken", "RS256", True),
        (expired_token(), "HS256", True),
        (valid_token(), "HS256", False),
    ],
)
def test_oidc_authentication_authenticate(
    rf, token, algorithm, error, requests_mock, settings
):
    settings.OIDC_VERIFY_ALGORITHM = algorithm
    requests_mock.get(settings.OIDC_JWKS_ENDPOINT, text=json.dumps(KEYS))

    request = rf.get("/openid", HTTP_AUTHORIZATION=token)

    try:
        result = authentication.OIDCAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
    else:
        if result:
            user, auth = result
            assert user.is_authenticated
            assert user.group == "test"


def test_oidc_authentication_header(rf):
    request = rf.get("/openid")
    assert (
        authentication.OIDCAuthentication().authenticate_header(request)
        == "Bearer realm=document-merge-service"
    )
