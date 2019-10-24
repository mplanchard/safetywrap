"""Ensure CI & any other infra is set up correctly."""

import safetywrap


def test_pass() -> None:
    """Always pass to verify tests are running."""
    assert True


class TestPublicInterface:
    """Test the interface to be sure we don't accidentally drop things."""

    def test_top_level(self) -> None:
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
        assert all(map(lambda attr: bool(getattr(safetywrap, attr)), exp_attrs))
