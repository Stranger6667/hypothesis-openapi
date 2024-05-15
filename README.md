# hypothesis-openapi

[![Build](https://github.com/Stranger6667/hypothesis-openapi/workflows/ci/badge.svg)](https://github.com/Stranger6667/hypothesis-main/actions)
[![Coverage](https://codecov.io/gh/Stranger6667/hypothesis-openapi/branch/main/graph/badge.svg)](https://codecov.io/gh/Stranger6667/hypothesis-openapi/branch/main)
[![Version](https://img.shields.io/pypi/v/hypothesis-openapi.svg)](https://pypi.org/project/hypothesis-openapi/)
[![Python versions](https://img.shields.io/pypi/pyversions/hypothesis-openapi.svg)](https://pypi.org/project/hypothesis-openapi/)
[![License](https://img.shields.io/pypi/l/hypothesis-openapi.svg)](https://opensource.org/licenses/MIT)

Hypothesis plugin for generating valid Open API documents.

## Usage

```python
from hypothesis import given
from hypothesis_openapi import openapis


@given(openapis(version="2.0"))
def test_openapi(spec):
    assert spec["swagger"] == "2.0"
    assert "info" in spec
```

## License

The code in this project is licensed under [MIT license](https://opensource.org/licenses/MIT).
By contributing to `hypothesis-openapi`, you agree that your contributions will be licensed under its MIT license.
