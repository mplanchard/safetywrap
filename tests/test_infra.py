"""Ensure CI & any other infra is set up correctly."""

import result_types


def test_pass() -> None:
    """Always pass to verify tests are running."""
    assert True


def test_public_interface() -> None:
    """Test the public package interface."""
    exp_attrs = (
        "__version__",
        "__version_info__",
        "Option",
        "Result",
        "Ok",
        "Err",
        "Some",
        "Nothing",
    )
    assert all(map(lambda attr: bool(getattr(result_types, attr)), exp_attrs))
