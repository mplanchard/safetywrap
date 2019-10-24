"""Test the Option type."""

import typing as t

import pytest

from safetywrap import Option, Some, Nothing, Result, Ok, Err


def _sq(val: int) -> Option[int]:
    """Square the result and return an option."""
    return Some(val ** 2)


def _nothing(_: int) -> Option[int]:
    """Just return nothing."""
    return Nothing()


class TestOptionConstructors:
    """Test option constructors."""

    @pytest.mark.parametrize(
        "val, exp",
        (
            (5, Some(5)),
            (None, Nothing()),
            ("", Some("")),
            (False, Some(False)),
            ({}, Some({})),
            ([], Some([])),
        ),
    )
    def test_of(self, val: t.Any, exp: Option) -> None:
        """Option.of() returns an Option from an Optional."""
        assert Option.of(val) == exp

    @pytest.mark.parametrize(
        "predicate, val, exp",
        (
            (lambda x: x is True, True, Some(True)),
            (lambda x: x is True, False, Nothing()),
            (lambda x: x > 0, 1, Some(1)),
            (lambda x: x > 0, -2, Nothing()),
        ),
    )
    def test_ok_if(
        self, predicate: t.Callable, val: t.Any, exp: Option
    ) -> None:
        """Test constructing based on some predicate."""
        assert Option.some_if(predicate, val) == exp

    @pytest.mark.parametrize(
        "predicate, val, exp",
        (
            (lambda x: x is True, True, Nothing()),
            (lambda x: x is True, False, Some(False)),
            (lambda x: x > 0, 1, Nothing()),
            (lambda x: x > 0, -2, Some(-2)),
        ),
    )
    def test_err_if(
        self, predicate: t.Callable, val: t.Any, exp: Option
    ) -> None:
        """Test constructing based on some predicate."""
        assert Option.nothing_if(predicate, val) == exp


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
        """Returns Some() if both options are Some()."""
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
        """Returns Some() if either or both is Some()."""
        assert left.or_(right) == exp

    @pytest.mark.parametrize(
        "left, right, exp",
        (
            (Some(2), Nothing(), Some(2)),
            (Nothing(), Some(2), Some(2)),
            (Some(1), Some(2), Nothing()),
            (Nothing(), Nothing(), Nothing()),
        ),
    )
    def test_xor(
        self, left: Option[int], right: Option[int], exp: Option[int]
    ) -> None:
        """Returns Some() IFF only one option is Some()."""
        assert left.xor(right) == exp

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

    @pytest.mark.parametrize("exc_cls", (None, IOError))
    def test_expect_raising(self, exc_cls: t.Type[Exception]) -> None:
        """Can specify exception msg/cls if value is not Some()."""
        exp_exc = exc_cls if exc_cls else RuntimeError
        kwargs = {"exc_cls": exc_cls} if exc_cls else {}
        msg = "not what I expected"

        with pytest.raises(exp_exc) as exc_info:
            Nothing().expect(msg, **kwargs)

        assert msg in str(exc_info.value)

    def test_expect_not_raising(self) -> None:
        """Expecting on a Some() returns the value."""
        assert Some("hello").expect("not what I expected") == "hello"

    @pytest.mark.parametrize(
        "start, exp",
        ((Nothing(), Nothing()), (Some(3), Nothing()), (Some(4), Some(4))),
    )
    def test_filter(self, start: Option[int], exp: Option[int]) -> None:
        """A satisfied predicate returns `Some()`, otherwise `None()`."""

        def is_even(val: int) -> bool:
            return val % 2 == 0

        assert start.filter(is_even) == exp

    @pytest.mark.parametrize("opt, exp", ((Nothing(), True), (Some(1), False)))
    def test_is_nothing(self, opt: Option[int], exp: bool) -> None:
        """"Nothings() are nothing, Some()s are not."""
        assert opt.is_nothing() is exp

    @pytest.mark.parametrize("opt, exp", ((Nothing(), False), (Some(1), True)))
    def test_is_some(self, opt: Option[int], exp: bool) -> None:
        """"Nothings() are nothing, Some()s are not."""
        assert opt.is_some() is exp

    @pytest.mark.parametrize("opt, exp", ((Nothing(), ()), (Some(5), (5,))))
    def test_iter(self, opt: Option[int], exp: t.Tuple[int, ...]) -> None:
        """Iterating on a Some() yields the Some(); on a None() nothing."""
        assert tuple(opt.iter()) == tuple(iter(opt)) == exp

    @pytest.mark.parametrize(
        "opt, exp", ((Some("hello"), Some(5)), (Nothing(), Nothing()))
    )
    def test_map(self, opt: Option[str], exp: Option[int]) -> None:
        """Maps fn() onto `Some()` to make a new option, or ignores None()."""
        assert opt.map(len) == exp

    @pytest.mark.parametrize("opt, exp", ((Some("hello"), 5), (Nothing(), -1)))
    def test_map_or(self, opt: Option[str], exp: Option[int]) -> None:
        """Maps fn() onto `Some()` & return the value, or return a default."""
        assert opt.map_or(-1, lambda s: len(s)) == exp

    @pytest.mark.parametrize("opt, exp", ((Some("hello"), 5), (Nothing(), -1)))
    def test_map_or_else(self, opt: Option[str], exp: Option[int]) -> None:
        """Maps fn() onto `Some()` & return the value, or return a default."""
        assert opt.map_or_else(lambda: -1, lambda s: len(s)) == exp

    @pytest.mark.parametrize(
        "opt, exp", ((Some(2), Ok(2)), (Nothing(), Err("oh no")))
    )
    def test_ok_or(self, opt: Option[str], exp: Result[str, int]) -> None:
        """Map `Some(t)` to `Ok(t)`, or `Nothing()` to an `Err()`."""
        assert opt.ok_or("oh no") == exp

    @pytest.mark.parametrize(
        "opt, exp", ((Some(2), Ok(2)), (Nothing(), Err("oh no")))
    )
    def test_ok_or_else(self, opt: Option[str], exp: Result[str, int]) -> None:
        """Map `Some(t)` to `Ok(t)`, or `Nothing()` to an `Err()`."""
        assert opt.ok_or_else(lambda: "oh no") == exp

    def test_unwrap_raising(self) -> None:
        """Unwraping a Nothing() raises an error."""
        with pytest.raises(RuntimeError):
            Nothing().unwrap()

    def test_unwrap_success(self) -> None:
        """Unwrapping a Some() returns the wrapped value."""
        assert Some("thing").unwrap() == "thing"

    @pytest.mark.parametrize("opt, exp", ((Some(2), 2), (Nothing(), 42)))
    def test_unwrap_or(self, opt: Option[int], exp: int) -> None:
        """Unwraps a `Some()` or returns a default."""
        assert opt.unwrap_or(42) == exp

    @pytest.mark.parametrize("opt, exp", ((Some(2), 2), (Nothing(), 42)))
    def test_unwrap_or_else(self, opt: Option[int], exp: int) -> None:
        """Unwraps a `Some()` or returns a default."""
        assert opt.unwrap_or_else(lambda: 42) == exp

    @pytest.mark.parametrize(
        "inst, other, eq",
        (
            (Some(1), Some(1), True),
            (Some(1), Some(2), False),
            (Some(1), Nothing(), False),
            (Some(1), 1, False),
            (Nothing(), Nothing(), True),
            (Nothing(), Some(1), False),
            (Nothing(), None, False),
        ),
    )
    def test_equality_inequality(
        self, inst: t.Any, other: t.Any, eq: bool
    ) -> None:
        """Test equality and inequality of results."""
        assert (inst == other) is eq
        assert (inst != other) is not eq

    def test_stringify(self) -> None:
        """Repr and str representations are equivalent."""
        assert repr(Some(1)) == str(Some(1)) == "Some(1)"
        assert repr(Nothing()) == str(Nothing()) == "Nothing()"
