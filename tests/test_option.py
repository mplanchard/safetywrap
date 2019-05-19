"""Test the Option type."""

# import typing as t

import pytest

from result_types import Option, Some, Nothing


class TestOption:
    """Test the option type."""

    @pytest.mark.parametrize(
        "left, right, exp",
        (
            (Some(2), Nothing(), Nothing()),
            (Nothing(), Some(2), Nothing()),
            (Some(1), Some(2), Some(2)),
            (Nothing(), Nothing(), Nothing()),
        ),
    )
    def test_and(
        self, left: Option[int], right: Option[int], exp: Option[int]
    ) -> None:
        """Returns an && combination of Options."""
        assert left.and_(right) == exp

    @pytest.mark.parametrize(
        "left, right, exp",
        (
            (Some(2), Nothing(), Some(2)),
            (Nothing(), Some(2), Some(2)),
            (Some(1), Some(2), Some(1)),
            (Nothing(), Nothing(), Nothing()),
        ),
    )
    def test_or(
        self, left: Option[int], right: Option[int], exp: Option[int]
    ) -> None:
        """Returns an && combination of Options."""
        assert left.or_(right) == exp

    # TODO: finish option types
