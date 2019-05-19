"""A result wrapper for data types."""

import typing as t

# pylint: disable=invalid-name

T = t.TypeVar("T")
E = t.TypeVar("E")
U = t.TypeVar("U")
F = t.TypeVar("F")


class Result(t.Generic[T, E]):
    """Standard wrapper for results."""

    _value: t.Union[T, E]

    def __init__(self, result: t.Union[T, E]) -> None:
        """Results may not be instantiated directly."""
        raise NotImplementedError(
            "Results are only for type hinting and may not be instantiated "
            "directly. Please use Ok() or Err() instead."
        )

    def and_(self, res: "Result[U, E]") -> "Result[U, E]":
        """Return `res` if the result is `Ok`, otherwise return `self`."""
        if self.is_ok():
            return res
        return t.cast(Result[U, E], self)

    def or_(self, res: "Result[T, F]") -> "Result[T, F]":
        """Return `res` if the result is `Err`, otherwise `self`."""
        if self.is_err():
            return res
        return t.cast(Result[T, F], self)

    def and_then(self, fn: t.Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """Call `fn` if Ok, or ignore an error.

        This can be used to chain functions that return results.
        """
        if self.is_ok():
            res: Result[U, E] = fn(t.cast(T, self._value))
            return res
        return t.cast(Result[U, E], self)

    def or_else(self, fn: t.Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        """Return `self` if `Ok`, or call `fn` with `self` if `Err`."""
        if self.is_err():
            return fn(t.cast(E, self._value))
        return t.cast(Result[T, F], self)

    def err(self) -> "Option[E]":
        """Return Err value if result is Err."""
        if self.is_err():
            return Some(t.cast(E, self._value))
        return Nothing()

    def ok(self) -> "Option[T]":
        """Return OK value if result is Ok."""
        if self.is_ok():
            return Some(t.cast(T, self._value))
        return Nothing()

    def expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T:
        """Return `Ok` value or raise an error with the specified message.

        The raised exception class may be specified with the `exc_cls`
        keyword argument.
        """
        if self.is_ok():
            return t.cast(T, self._value)
        raise exc_cls(msg)

    def expect_err(
        self, msg: str, exc_cls: t.Type[Exception] = RuntimeError
    ) -> E:
        """Return `Err` value or raise an error with the specified message.

        The raised exception class may be specified with the `exc_cls`
        keyword argument.
        """
        if self.is_err():
            return t.cast(E, self._value)
        raise exc_cls(msg)

    def is_err(self) -> bool:
        """Returl whether the result is an Err."""
        return isinstance(self, Err)

    def is_ok(self) -> bool:
        """Return whether the result is OK."""
        return isinstance(self, Ok)

    def iter(self) -> t.Iterator[T]:
        """Return a one-item iterator whose sole member is the result if `Ok`.

        If the result is `Err`, the iterator will contain no items.
        """
        if self.is_ok():
            yield t.cast(T, self._value)

    def map(self, fn: t.Callable[[T], U]) -> "Result[U, E]":
        """Map a function onto an okay result, or ignore an error."""
        if self.is_ok():
            return Ok(fn(t.cast(T, self._value)))
        return t.cast(Result[U, E], self)

    def map_err(self, fn: t.Callable[[E], F]) -> "Result[T, F]":
        """Map a function onto an error, or ignore a success."""
        if self.is_err():
            return Err(fn(t.cast(E, self._value)))
        return t.cast(Result[T, F], self)

    def unwrap(self) -> T:
        """Return an Ok result, or throw an error if an Err."""
        if self.is_err():
            raise RuntimeError(f"Tried to unwrap {self}!")
        return t.cast(T, self._value)

    def unwrap_err(self) -> E:
        """Return an Ok result, or throw an error if an Err."""
        if self.is_ok():
            raise RuntimeError(f"Tried to unwrap_err {self}!")
        return t.cast(E, self._value)

    def unwrap_or(self, alternative: T) -> T:
        """Return the `Ok` value, or `alternative` if `self` is `Err`."""
        if self.is_ok():
            return t.cast(T, self._value)
        return alternative

    def unwrap_or_else(self, fn: t.Callable[[E], T]) -> T:
        """Return the `Ok` value, or the return from `fn`."""
        if self.is_ok():
            return t.cast(T, self._value)
        return fn(t.cast(E, self._value))

    def __eq__(self, other: t.Any) -> bool:
        """Compare two results. They are equal if their values are equal."""
        if not isinstance(other, Result):
            return False
        eq: bool
        if self.is_ok() and other.is_ok():
            eq = self.unwrap() == other.unwrap()
            return eq
        elif self.is_err() and other.is_err():
            eq = self.unwrap_err() == other.unwrap_err()
            return eq
        return False

    def __ne__(self, other: t.Any) -> bool:
        """Compare two results. They are equal if their values are equal."""
        return not self == other

    def __str__(self) -> str:
        """Return string value of result."""
        return f"{self.__class__.__name__}({repr(self._value)})"

    def __repr__(self) -> str:
        """Return repr for result."""
        return self.__str__()


class Ok(Result[T, E]):
    """An Ok result."""

    def __init__(self, result: T) -> None:
        """Wrap a result."""
        self._value = result


class Err(Result[T, E]):
    """An error result."""

    def __init__(self, result: E) -> None:
        """Wrap a result."""
        self._value = result


class Option(t.Generic[T]):
    """A value that may be `Some` or `Nothing`."""

    _value: t.Union[T, None]

    def __init__(self, value: t.Optional[T]) -> None:
        """Options may not be instantiated directly."""
        raise NotImplementedError(
            "Options may not be instantiated directly. Use Some() or "
            "Nothing() instead."
        )

    def and_(self, alternative: "Option[U]") -> "Option[U]":
        """Return `Nothing` if `self` is `Nothing`, or the `alternative`."""
        if self.is_nothing():
            return t.cast(Option[U], self)
        return alternative

    def or_(self, alternative: "Option[T]") -> "Option[T]":
        """Return option if it is `Some`, or the `alternative`."""
        if self.is_some():
            return t.cast(Option[T], self)
        return alternative

    def and_then(self, fn: t.Callable[[T], "Option[U]"]) -> "Option[U]":
        """Return `Nothing`, or call `fn` with the `Some` value."""
        if self.is_nothing():
            return t.cast(Option[U], self)
        return fn(t.cast(T, self._value))

    def or_else(self, fn: t.Callable[[], "Option[T]"]) -> "Option[T]":
        """Return option if it is `Some`, or calculate an alternative."""
        if self.is_some():
            return t.cast(Option[T], self)
        return fn()

    def expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T:
        """Unwrap and yield a `Some`, or throw an exception if `Nothing`.

        The exception class may be specified with the `exc_cls` keyword
        argument.
        """
        if self.is_some():
            return t.cast(T, self._value)
        raise exc_cls(msg)

    def filter(self, predicate: t.Callable[[T], bool]) -> "Option[T]":
        """Return `Nothing`, or an option determined by the predicate.

        If `self` is `Some`, call `predicate` with the wrapped value and
        return:

        * `self` (`Some(t)` where `t` is the wrapped value) if the predicate
          is `True`
        * `Nothing` if the predicate is `False`
        """
        if self.is_some():
            predicate_satisfied = predicate(t.cast(T, self._value))
            if predicate_satisfied:
                return t.cast(Option[T], self)
            nothing: Option[T] = Nothing()
            return nothing
        return t.cast(Option[T], self)

    def is_nothing(self) -> bool:
        """Return whether the option is `Nothing`."""
        return isinstance(self, Nothing)

    def is_some(self) -> bool:
        """Return whether the option is a `Some` value."""
        return isinstance(self, Some)

    def iter(self) -> t.Iterator[T]:
        """Return an iterator over the possibly contained value."""
        if self.is_some():
            yield t.cast(T, self._value)

    def map(self, fn: t.Callable[[T], U]) -> "Option[U]":
        """Apply `fn` to the contained value if any."""
        if self.is_some():
            option: Option[U] = Some(fn(t.cast(T, self._value)))
            return option
        return t.cast(Option[U], self)

    def map_or(self, default: U, fn: t.Callable[[T], U]) -> U:
        """Apply `fn` to contained value, or return the default."""
        if self.is_some():
            return fn(t.cast(T, self._value))
        return default

    def map_or_else(
        self, default: t.Callable[[], U], fn: t.Callable[[T], U]
    ) -> U:
        """Apply `fn` to contained value, or compute a default."""
        if self.is_some():
            return fn(t.cast(T, self._value))
        return default()

    def ok_or(self, err: E) -> Result[T, E]:
        """Transform an option into a `Result`.

        Maps `Some(v)` to `Ok(v)` or `None` to `Err(err)`.
        """
        res: Result[T, E]
        if self.is_some():
            res = Ok(t.cast(T, self._value))
            return res
        res = Err(err)
        return res

    def ok_or_else(self, err_fn: t.Callable[[], E]) -> Result[T, E]:
        """Transform an option into a `Result`.

        Maps `Some(v)` to `Ok(v)` or `None` to `Err(err_fn())`.
        """
        res: Result[T, E]
        if self.is_some():
            res = Ok(t.cast(T, self._value))
            return res
        res = Err(err_fn())
        return res

    def unwrap(self) -> T:
        """Return `Some` value, or raise an error."""
        if self.is_some():
            return t.cast(T, self._value)
        raise RuntimeError("Tried to unwrap Nothing")

    def unwrap_or(self, default: T) -> T:
        """Return the contained value or `default`."""
        if self.is_some():
            return t.cast(T, self._value)
        return default

    def unwrap_or_else(self, fn: t.Callable[[], T]) -> T:
        """Return the contained value or calculate a default."""
        if self.is_some():
            return t.cast(T, self._value)
        return fn()

    def __eq__(self, other: t.Any) -> bool:
        """Options are equal if their values are equal."""
        if not isinstance(other, Option):
            return False
        if self.is_some() and other.is_some():
            eq: bool = self.unwrap() == other.unwrap()
            return eq
        elif self.is_nothing() and other.is_nothing():
            return True
        return False

    def __ne__(self, other: t.Any) -> bool:
        """Options are equal if their values are equal."""
        return not self == other

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()


class Some(Option[T]):
    """A value that is something."""

    def __init__(self, value: T) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"Some({repr(self._value)})"


class Nothing(Option[T]):
    """A value that is nothing."""

    def __init__(self, value: None = None) -> None:
        self._value = None

    def __str__(self) -> str:
        return f"Nothing()"
