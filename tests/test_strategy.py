import pytest
from hypothesis import HealthCheck, given, settings

from hypothesis_openapi import openapis

from .v2 import VALIDATOR as SWAGGER_VALIDATOR


@given(openapis(version="2.0"))
@settings(deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_openapi(spec):
    assert SWAGGER_VALIDATOR.is_valid(spec)


def test_unsupported_version():
    with pytest.raises(ValueError):
        openapis(version="45.0")
