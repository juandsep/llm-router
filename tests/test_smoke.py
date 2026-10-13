"""Smoke test: the package imports and exposes a version.

Deliberately small. Add tests with the code, not before it: one test that fails
when the thing breaks beats a suite that tests the framework.
"""

import llm_router


def test_package_exposes_version() -> None:
    assert llm_router.__version__
