"""Ensure CI & any other infra is set up correctly."""

import result_types


def test_pass() -> None:
    """Always pass to verify tests are running."""
    assert True


def test_import() -> None:
    """Ensure we can import our package."""
    assert result_types.__version__
