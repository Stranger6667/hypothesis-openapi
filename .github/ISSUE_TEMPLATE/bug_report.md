---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: Stranger6667

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
A minimal test that reproduces the problem, and the full traceback if there is one.

```python
from hypothesis import given

from hypothesis_openapi import openapis


@given(openapis(version="3.0"))
def test_example(spec): ...
```

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment (please complete the following information):**

- OS: [e.g. Linux or Windows]
- Python version: [e.g. 3.13.1]
- Hypothesis version: [e.g. 6.140.0]
- hypothesis-openapi version: [e.g. 0.3.0]

**Additional context**
Add any other context about the problem here.
