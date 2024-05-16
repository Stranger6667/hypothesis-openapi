import pytest

from hypothesis import HealthCheck, given, settings, Phase, Verbosity, seed

from hypothesis_openapi import openapis


@pytest.mark.benchmark
def test_generate():
    @given(openapis(version="2.0"))
    @seed(1)
    @settings(
        deadline=None,
        database=None,
        derandomize=True,
        max_examples=10,
        suppress_health_check=list(HealthCheck),
        phases=[Phase.generate],
        verbosity=Verbosity.quiet,
    )
    def test(spec):
        pass

    test()
