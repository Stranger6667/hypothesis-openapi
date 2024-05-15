from .v2 import VALIDATOR as SWAGGER_VALIDATOR
from hypothesis import given, settings, HealthCheck
from hypothesis_openapi import openapis


@given(openapis(version="2.0"))
@settings(deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_openapi(spec):
    assert SWAGGER_VALIDATOR.is_valid(spec)
