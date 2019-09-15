"""Test the Result type."""

import typing as t

import pytest

from result_types import Ok, Err, Result, Some, Nothing, Option


def _sq(val: int) -> Result[int, int]:
    """Square a value."""
    return Ok(val ** 2)


def _err(val: int) -> Result[int, int]:
    """Return an error."""
    return Err(val)


def _raises(exc: t.Type[Exception]) -> None:
    raise exc


class TestResultConstructors:
    """Test Result constructors."""

    @pytest.mark.parametrize(
        "fn, exp",
        (
            (lambda: 5, Ok(5)),
            (lambda: _raises(TypeError), Err(TypeError)),
            (lambda: Nothing(), Ok(Nothing())),
        ),
    )
    def test_from_(self, fn: t.Callable, exp: Result) -> None:
        """Test getting a result from a callable."""
        if exp.is_err():
            assert isinstance(Result.from_(fn).unwrap_err(), exp.unwrap_err())
        else:
            assert Result.from_(fn) == exp

    @pytest.mark.parametrize(
        "fn, exp",
        (
            (lambda: 5, Ok(5)),
            (lambda: _raises(TypeError), Err(TypeError)),
            (lambda: Some("foo"), Ok(Some("foo"))),
        ),
    )
    def test_wrap(self, fn: t.Callable, exp: Result) -> None:
        """A wrapped function returns Ok() on success or Err() on exception."""
        wrapped = Result.wrap(fn)  # type: ignore
        res = wrapped()

        if exp.is_err():
            assert isinstance(res.unwrap_err(), exp.unwrap_err())
        else:
            assert wrapped() == exp

        @Result.wrap
        def _decorated() -> t.Any:
            return fn()

        res = _decorated()

        if exp.is_err():
            assert isinstance(res.unwrap_err(), exp.unwrap_err())
        else:
            assert wrapped() == exp

    @pytest.mark.parametrize(
        "fn, excs, exp",
        (
            (lambda: 5, (Exception,), Ok(5)),
            (lambda: _raises(TypeError), (Exception,), Err(TypeError)),
            (lambda: _raises(TypeError), (ValueError,), TypeError),
            (
                lambda: _raises(FloatingPointError),
                (ArithmeticError,),
                Err(FloatingPointError),
            ),
            (
                lambda: _raises(TypeError),
                (ValueError, TypeError),
                Err(TypeError),
            ),
        ),
    )
    def test_wrap_for(
        self, fn: t.Callable, excs: t.Tuple[t.Type[Exception], ...], exp: Result
    ) -> None:
        """Wrap_for allows intercepting only specific decorators."""
        wrapped = Result.wrap_for(excs)(fn)  # type: ignore

        @Result.wrap_for(excs)
        def _decorated() -> t.Any:
            return fn()

        if isinstance(exp, type) and issubclass(exp, Exception):
            with pytest.raises(exp):
                wrapped()
            with pytest.raises(exp):
                _decorated()
            return

        res = wrapped()

        if exp.is_err():
            assert isinstance(res.unwrap_err(), exp.unwrap_err())
        else:
            assert wrapped() == exp

        res = _decorated()

        if exp.is_err():
            assert isinstance(res.unwrap_err(), exp.unwrap_err())
        else:
            assert wrapped() == exp


class TestResult:
    """Test the result type."""

    @pytest.mark.parametrize(
        "left, right, exp",
        (
            (Ok(2), Err("late error"), Err("late error")),
            (Err("early error"), Ok(2), Err("early error")),
            (Err("early error"), Err("late error"), Err("early error")),
            (Ok(2), Ok(3), Ok(3)),
        ),
    )
    def test_and(
        self,
        left: Result[int, str],
        right: Result[int, str],
        exp: Result[int, str],
    ) -> None:
        """Test that `and` returns an alternative for `Ok` values."""
        assert left.and_(right) == exp

    def test_and_multichain(self) -> None:
        """.and() calls can be chained indefinitely."""
        assert Ok(2).and_(Ok(3)).and_(Ok(4)).and_(Ok(5)) == Ok(5)

    @pytest.mark.parametrize(
        "start, first, second, exp",
        (
            (Ok(2), _sq, _sq, Ok(16)),
            (Ok(2), _sq, _err, Err(4)),
            (Ok(2), _err, _sq, Err(2)),
            (Ok(2), _err, _err, Err(2)),
            (Err(3), _sq, _sq, Err(3)),
        ),
    )
    def test_and_then(
        self,
        start: Result[int, int],
        first: t.Callable[[int], Result[int, int]],
        second: t.Callable[[int], Result[int, int]],
        exp: Result[int, int],
    ) -> None:
        """Test that and_then chains result-generating functions."""
        assert start.and_then(first).and_then(second) == exp

    @pytest.mark.parametrize(
        "start, first, second, exp",
        (
            (Ok(2), _sq, _sq, Ok(2)),
            (Ok(2), _err, _sq, Ok(2)),
            (Err(3), _sq, _err, Ok(9)),
            (Err(3), _err, _err, Err(3)),
        ),
    )
    def test_or_else(
        self,
        start: Result[int, int],
        first: t.Callable[[int], Result[int, int]],
        second: t.Callable[[int], Result[int, int]],
        exp: Result[int, int],
    ) -> None:
        """Test that and_then chains result-generating functions."""
        assert start.or_else(first).or_else(second) == exp

    @pytest.mark.parametrize(
        "start, exp", ((Ok(2), Nothing()), (Err("err"), Some("err")))
    )
    def test_err(self, start: Result[int, str], exp: Option[str]) -> None:
        """Test converting a result to an option."""
        assert start.err() == exp

    @pytest.mark.parametrize("exc_cls", (None, IOError))
    def test_expect_raising(self, exc_cls: t.Type[Exception]) -> None:
        """Test expecting a value to be Ok()."""
        exp_exc = exc_cls if exc_cls else RuntimeError
        kwargs = {"exc_cls": exc_cls} if exc_cls else {}
        msg = "not what I expected"

        with pytest.raises(exp_exc) as exc_info:
            Err(2).expect(msg, **kwargs)

        assert msg in str(exc_info.value)

    def test_expect_ok(self) -> None:
        """Expecting an Ok() value returns the value."""
        assert Ok(2).expect("err") == 2

    @pytest.mark.parametrize("exc_cls", (None, IOError))
    def test_expect_err_raising(self, exc_cls: t.Type[Exception]) -> None:
        """Test expecting a value to be Ok()."""
        exp_exc = exc_cls if exc_cls else RuntimeError
        kwargs = {"exc_cls": exc_cls} if exc_cls else {}
        msg = "not what I expected"

        with pytest.raises(exp_exc) as exc_info:
            Ok(2).expect_err(msg, **kwargs)

        assert msg in str(exc_info.value)

    def test_expect_err_err(self) -> None:
        """Expecting an Ok() value returns the value."""
        assert Err(2).expect_err("err") == 2

    def test_is_err(self) -> None:
        """Err() returns true for is_err()."""
        assert Err(1).is_err()
        assert not Ok(1).is_err()

    def test_is_ok(self) -> None:
        """Ok() returns true for is_ok()."""
        assert Ok(1).is_ok()
        assert not Err(1).is_ok()

    @pytest.mark.parametrize("start, exp", ((Ok(1), (1,)), (Err(1), ())))
    def test_iter(
        self, start: Result[int, int], exp: t.Tuple[int, ...]
    ) -> None:
        """iter() returns a 1-member iterator on Ok(), 0-member for Err()."""
        assert tuple(start.iter()) == exp

    @pytest.mark.parametrize(
        "start, exp", ((Ok(2), Ok(4)), (Err("foo"), Err("foo")))
    )
    def test_map(self, start: Result[int, str], exp: Result[int, str]) -> None:
        """.map() will map onto Ok() and ignore Err()."""
        assert start.map(lambda x: x ** 2) == exp

    @pytest.mark.parametrize(
        "start, exp", ((Ok("foo"), Ok("foo")), (Err(2), Err("2")))
    )
    def test_map_err(
        self, start: Result[str, int], exp: Result[str, str]
    ) -> None:
        """.map_err() will map onto Err() and ignore Ok()."""
        assert start.map_err(lambda i: str(i)) == exp

    @pytest.mark.parametrize(
        "start, exp", ((Ok(1), Some(1)), (Err(1), Nothing()))
    )
    def test_ok(self, start: Result[int, int], exp: Option[int]) -> None:
        """.ok() converts a result to an Option."""
        assert start.ok() == exp

    @pytest.mark.parametrize(
        "left, right, exp",
        (
            (Ok(5), Ok(6), Ok(5)),
            (Ok(5), Err(6), Ok(5)),
            (Err(5), Ok(6), Ok(6)),
            (Err(5), Err(6), Err(6)),
        ),
    )
    def test_or(
        self,
        left: Result[int, str],
        right: Result[int, str],
        exp: Result[int, str],
    ) -> None:
        """.or_() returns the first available non-err value."""
        assert left.or_(right) == exp

    def test_or_multichain(self) -> None:
        """.or_() calls can be chained indefinitely."""
        err: Result[int, int] = Err(5)
        assert err.or_(Err(6)).or_(Err(7)).or_(Ok(8)) == Ok(8)

    def test_unwrap_is_ok(self) -> None:
        """.unwrap() returns an ok() value."""
        assert Ok(5).unwrap() == 5

    def test_unwrap_is_err(self) -> None:
        """.unwrap() raises for an error value."""
        with pytest.raises(RuntimeError):
            Err(5).unwrap()

    def test_unwrap_err_is_ok(self) -> None:
        """.unwrap_err() raises for an ok value."""
        with pytest.raises(RuntimeError):
            Ok(5).unwrap_err()

    def test_unwrap_err_is_err(self) -> None:
        """.unwrap_err() returns an error value."""
        assert Err(5).unwrap_err() == 5

    @pytest.mark.parametrize("start, alt, exp", ((Ok(5), 6, 5), (Err(5), 6, 6)))
    def test_unwrap_or(
        self, start: Result[int, int], alt: int, exp: int
    ) -> None:
        """.unwrap_or() provides the default if the result is Err()."""
        assert start.unwrap_or(alt) == exp

    @pytest.mark.parametrize(
        "start, fn, exp",
        ((Ok(5), lambda i: i + 2, 5), (Err(5), lambda i: i + 2, 7)),
    )
    def test_unwrap_or_else(
        self, start: Result[int, int], fn: t.Callable[[int], int], exp: int
    ) -> None:
        """Calculates a result from Err() value if present."""
        assert start.unwrap_or_else(fn) == exp
