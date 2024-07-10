import pytest
from hypothesis import HealthCheck, given, settings
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT4

from hypothesis_openapi import openapis

from .v2 import VALIDATOR as SWAGGER_VALIDATOR
from .v3 import VALIDATOR as OPENAPI_30_VALIDATOR


def assert_resolvable_references(spec, specification):
    resource = Resource(contents=spec, specification=specification)
    registry = Registry().with_resource(uri="urn:root", resource=resource)
    _assert_resolvable_references(registry, spec)


def _assert_resolvable_references(registry, spec):
    if isinstance(spec, dict):
        for key, value in spec.items():
            if key == "$ref":
                registry.resolver().lookup(f"urn:root{value}")
            else:
                _assert_resolvable_references(registry, value)
    elif isinstance(spec, list):
        for item in spec:
            _assert_resolvable_references(registry, item)


@given(openapis(version="2.0"))
@settings(deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_swagger(spec):
    SWAGGER_VALIDATOR.validate(spec)
    assert_resolvable_references(spec, DRAFT4)


@given(openapis(version="3.0"))
@settings(deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_openapi_30(spec):
    OPENAPI_30_VALIDATOR.validate(spec)
    assert_resolvable_references(spec, DRAFT4)


def test_unsupported_version():
    with pytest.raises(ValueError):
        openapis(version="45.0")
