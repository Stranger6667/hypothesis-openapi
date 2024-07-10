import pytest
from hypothesis import HealthCheck, given, settings

from hypothesis_openapi import openapis

from .v2 import VALIDATOR as SWAGGER_VALIDATOR
from .v3 import VALIDATOR as OPENAPI_30_VALIDATOR


@given(openapis(version="2.0"))
@settings(deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_swagger(spec):
    SWAGGER_VALIDATOR.validate(spec)


@given(openapis(version="3.0"))
@settings(deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_openapi_30(spec):
    OPENAPI_30_VALIDATOR.validate(spec)


def test_unsupported_version():
    with pytest.raises(ValueError):
        openapis(version="45.0")
