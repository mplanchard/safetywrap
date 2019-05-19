"""Test the Option type."""

import typing as t

import pytest

from result_types import Option, Some, Nothing


def _sq(val: int) -> Option[int]:
    """Square the result and return an option."""
    return Some(val ** 2)


def _nothing(val: int) -> Option[int]:
    """Just return nothing."""
    return Nothing()


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

    @pytest.mark.parametrize(
        "start, first, second, exp",
        (
            (Some(2), _sq, _sq, Some(16)),
            (Some(2), _sq, _nothing, Nothing()),
            (Some(2), _nothing, _sq, Nothing()),
            (Nothing(), _sq, _sq, Nothing()),
        ),
    )
    def test_and_then(
        self,
        start: Option[int],
        first: t.Callable[[int], Option[int]],
        second: t.Callable[[int], Option[int]],
        exp: Option[int],
    ) -> None:
        """Chains option-generating functions if results are `Some`."""
        assert start.and_then(first).and_then(second) == exp

    @pytest.mark.parametrize(
        "start, fn, exp",
        (
            (Some("one"), lambda: Some("one else"), Some("one")),
            (Nothing(), lambda: Some("one else"), Some("one else")),
            (Nothing(), lambda: Nothing(), Nothing()),
        ),
    )
    def test_or_else(
        self,
        start: Option[str],
        fn: t.Callable[[], Option[str]],
        exp: Option[str],
    ) -> None:
        """Chains option-generating functions if results are `None`."""
        assert start.or_else(fn) == exp
