import hashlib
import json

import pytest
from django.core.cache import cache
from rest_framework import exceptions, status

from .. import authentication


@pytest.mark.parametrize(
    "authentication_header,status_code,error",
    [
        ("", status.HTTP_200_OK, False),
        ("Bearer", status.HTTP_200_OK, True),
        ("Bearer Too many params", status.HTTP_200_OK, True),
        ("Basic Auth", status.HTTP_200_OK, True),
        ("Bearer Token", status.HTTP_200_OK, False),
        ("Bearer Token", status.HTTP_502_BAD_GATEWAY, True),
    ],
)
def test_bearer_token_authentication_authenticate(
    rf, authentication_header, error, requests_mock, settings, status_code
):
    settings.REQUIRE_AUTHENTICATION = True

    userinfo = {"sub": "1"}
    requests_mock.get(
        settings.OIDC_USERINFO_ENDPOINT,
        status_code=status_code,
        request_headers={"Authorization": authentication_header},
        text=json.dumps(userinfo),
    )

    request = rf.get("/openid", HTTP_AUTHORIZATION=authentication_header)

    try:
        result = authentication.BearerTokenAuthentication().authenticate(request)
    except exceptions.AuthenticationFailed:
        assert error
    else:
        if result:
            user, auth = result
            assert user.is_authenticated
            assert (
                cache.get(
                    f"authentication.userinfo.{hashlib.sha256(b'Token').hexdigest()}"
                )
                == userinfo
            )


def test_bearer_token_authentication_authenticate_groups_claim(
    settings, requests_mock, rf
):
    settings.REQUIRE_AUTHENTICATION = True
    settings.OIDC_GROUPS_CLAIM = "document-merge-service"

    userinfo = {"sub": "1", settings.OIDC_GROUPS_CLAIM: ["test"]}
    requests_mock.get(settings.OIDC_USERINFO_ENDPOINT, text=json.dumps(userinfo))

    request = rf.get("/openid", HTTP_AUTHORIZATION="Bearer Token")
    user, auth = authentication.BearerTokenAuthentication().authenticate(request)
    assert user.is_authenticated
    assert user.group == "test"
    assert user.groups == ["test"]


def test_bearer_token_authentication_header(rf):
    request = rf.get("/openid")
    assert (
        authentication.BearerTokenAuthentication().authenticate_header(request)
        == "Bearer realm=mock://document-merge-service.github.com/openid/userinfo"
    )
