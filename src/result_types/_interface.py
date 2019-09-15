"""Result and Option interfaces."""

import typing as t

# pylint: disable=invalid-name

T = t.TypeVar("T")
E = t.TypeVar("E")
U = t.TypeVar("U")
F = t.TypeVar("F")

ExcType = t.TypeVar("ExcType", bound=Exception)


class _Result(t.Generic[T, E]):
    """Standard wrapper for results."""

    __slots__ = ()

    def __init__(self, result: t.Union[T, E]) -> None:
        """Results may not be instantiated directly."""
        raise NotImplementedError(
            "Results are only for type hinting and may not be instantiated "
            "directly. Please use Ok() or Err() instead."
        )

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    # See https://github.com/python/mypy/issues/3737 for issue with
    # specifying a default type. However, type hinting of uses of this
    # method should still work just fine.
    @staticmethod
    def from_(  # type: ignore
        fn: t.Callable[[], T], exc_type: t.Type[ExcType] = Exception
    ) -> "_Result[T, ExcType]":
        """Call `fn` and wrap its result in an `Ok()`.

        If an exception is intercepted, return `Err(exception)`. By
        default, any `Exception` will be intercepted. If you specify
        `exc_type`, only that exception will be intercepted.
        """
        raise NotImplementedError

    # Same issue here with the default type
    @staticmethod
    def wrap(  # type: ignore
        fn: t.Callable[..., T],
        intercept: t.Iterable[t.Type[ExcType]] = (Exception,),
    ) -> t.Callable[..., "_Result[T, ExcType]"]:
        """Wrap or decorate a function so that it returns a Result."""
        raise NotImplementedError

    # Same issue here with the default type
    @staticmethod
    def wrap_for(
        exceptions: t.Iterable[t.Type[ExcType]],
    ) -> t.Callable[
        [t.Callable[..., T]], t.Callable[..., "_Result[T, ExcType]"]
    ]:
        """Create a wrapper/decorator to intercept the given exceptions."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def and_(self, res: "_Result[U, E]") -> "_Result[U, E]":
        """Return `res` if the result is `Ok`, otherwise return `self`."""
        raise NotImplementedError

    def or_(self, res: "_Result[T, F]") -> "_Result[T, F]":
        """Return `res` if the result is `Err`, otherwise `self`."""
        raise NotImplementedError

    def and_then(self, fn: t.Callable[[T], "_Result[U, E]"]) -> "_Result[U, E]":
        """Call `fn` if Ok, or ignore an error.

        This can be used to chain functions that return results.
        """
        raise NotImplementedError

    def or_else(self, fn: t.Callable[[E], "_Result[T, F]"]) -> "_Result[T, F]":
        """Return `self` if `Ok`, or call `fn` with `self` if `Err`."""
        raise NotImplementedError

    def err(self) -> "_Option[E]":
        """Return Err value if result is Err."""
        raise NotImplementedError

    def ok(self) -> "_Option[T]":
        """Return OK value if result is Ok."""
        raise NotImplementedError

    def expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T:
        """Return `Ok` value or raise an error with the specified message.

        The raised exception class may be specified with the `exc_cls`
        keyword argument.
        """
        raise NotImplementedError

    def expect_err(
        self, msg: str, exc_cls: t.Type[Exception] = RuntimeError
    ) -> E:
        """Return `Err` value or raise an error with the specified message.

        The raised exception class may be specified with the `exc_cls`
        keyword argument.
        """
        raise NotImplementedError

    def is_err(self) -> bool:
        """Returl whether the result is an Err."""
        raise NotImplementedError

    def is_ok(self) -> bool:
        """Return whether the result is OK."""
        raise NotImplementedError

    def iter(self) -> t.Iterator[T]:
        """Return a one-item iterator whose sole member is the result if `Ok`.

        If the result is `Err`, the iterator will contain no items.
        """
        raise NotImplementedError

    def map(self, fn: t.Callable[[T], U]) -> "_Result[U, E]":
        """Map a function onto an okay result, or ignore an error."""
        raise NotImplementedError

    def map_err(self, fn: t.Callable[[E], F]) -> "_Result[T, F]":
        """Map a function onto an error, or ignore a success."""
        raise NotImplementedError

    def unwrap(self) -> T:
        """Return an Ok result, or throw an error if an Err."""
        raise NotImplementedError

    def unwrap_err(self) -> E:
        """Return an Ok result, or throw an error if an Err."""
        raise NotImplementedError

    def unwrap_or(self, alternative: T) -> T:
        """Return the `Ok` value, or `alternative` if `self` is `Err`."""
        raise NotImplementedError

    def unwrap_or_else(self, fn: t.Callable[[E], T]) -> T:
        """Return the `Ok` value, or the return from `fn`."""
        raise NotImplementedError

    def __iter__(self) -> t.Iterator[T]:
        """Return a one-item iterator whose sole member is the result if `Ok`.

        If the result is `Err`, the iterator will contain no items.
        """
        raise NotImplementedError

    def __eq__(self, other: t.Any) -> bool:
        """Compare two results. They are equal if their values are equal."""
        raise NotImplementedError

    def __ne__(self, other: t.Any) -> bool:
        """Compare two results. They are equal if their values are equal."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Return string value of result."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Return repr for result."""
        raise NotImplementedError


class _Option(t.Generic[T]):
    """A value that may be `Some` or `Nothing`."""

    __slots__ = ()

    def __init__(self, value: t.Optional[T]) -> None:
        """Options may not be instantiated directly."""
        raise NotImplementedError(
            "Options may not be instantiated directly. Use Some() or "
            "Nothing() instead."
        )

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @staticmethod
    def of(value: t.Optional[T]) -> "_Option[T]":
        """Construct an _Option[T] from an Optional[T]."""
        raise NotImplementedError

    @staticmethod
    def wrap(
        fn: t.Callable[..., t.Optional[T]]
    ) -> t.Callable[..., "_Option[T]"]:
        """Wrap a function to convert its result to an Option."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def and_(self, alternative: "_Option[U]") -> "_Option[U]":
        """Return `Nothing` if `self` is `Nothing`, or the `alternative`."""
        raise NotImplementedError

    def or_(self, alternative: "_Option[T]") -> "_Option[T]":
        """Return option if it is `Some`, or the `alternative`."""
        raise NotImplementedError

    def xor(self, alternative: "_Option[T]") -> "_Option[T]":
        """Return Some IFF exactly one of `self`, `alternative` is `Some`."""
        raise NotImplementedError

    def and_then(self, fn: t.Callable[[T], "_Option[U]"]) -> "_Option[U]":
        """Return `Nothing`, or call `fn` with the `Some` value."""
        raise NotImplementedError

    def or_else(self, fn: t.Callable[[], "_Option[T]"]) -> "_Option[T]":
        """Return option if it is `Some`, or calculate an alternative."""
        raise NotImplementedError

    def expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T:
        """Unwrap and yield a `Some`, or throw an exception if `Nothing`.

        The exception class may be specified with the `exc_cls` keyword
        argument.
        """
        raise NotImplementedError

    def filter(self, predicate: t.Callable[[T], bool]) -> "_Option[T]":
        """Return `Nothing`, or an option determined by the predicate.

        If `self` is `Some`, call `predicate` with the wrapped value and
        return:

        * `self` (`Some(t)` where `t` is the wrapped value) if the predicate
          is `True`
        * `Nothing` if the predicate is `False`
        """
        raise NotImplementedError

    def is_nothing(self) -> bool:
        """Return whether the option is `Nothing`."""
        raise NotImplementedError

    def is_some(self) -> bool:
        """Return whether the option is a `Some` value."""
        raise NotImplementedError

    def iter(self) -> t.Iterator[T]:
        """Return an iterator over the possibly contained value."""
        raise NotImplementedError

    def map(self, fn: t.Callable[[T], U]) -> "_Option[U]":
        """Apply `fn` to the contained value if any."""
        raise NotImplementedError

    def map_or(self, default: U, fn: t.Callable[[T], U]) -> U:
        """Apply `fn` to contained value, or return the default."""
        raise NotImplementedError

    def map_or_else(
        self, default: t.Callable[[], U], fn: t.Callable[[T], U]
    ) -> U:
        """Apply `fn` to contained value, or compute a default."""
        raise NotImplementedError

    def ok_or(self, err: E) -> _Result[T, E]:
        """Transform an option into a `Result`.

        Maps `Some(v)` to `Ok(v)` or `None` to `Err(err)`.
        """
        raise NotImplementedError

    def ok_or_else(self, err_fn: t.Callable[[], E]) -> _Result[T, E]:
        """Transform an option into a `Result`.

        Maps `Some(v)` to `Ok(v)` or `None` to `Err(err_fn())`.
        """
        raise NotImplementedError

    def unwrap(self) -> T:
        """Return `Some` value, or raise an error."""
        raise NotImplementedError

    def unwrap_or(self, default: T) -> T:
        """Return the contained value or `default`."""
        raise NotImplementedError

    def unwrap_or_else(self, fn: t.Callable[[], T]) -> T:
        """Return the contained value or calculate a default."""
        raise NotImplementedError

    def __iter__(self) -> t.Iterator[T]:
        """Iterate over the contained value if present."""
        raise NotImplementedError

    def __eq__(self, other: t.Any) -> bool:
        """Options are equal if their values are equal."""
        raise NotImplementedError

    def __ne__(self, other: t.Any) -> bool:
        """Options are equal if their values are equal."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Return a string representation of the Option."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Return a string representation of the Option."""
        raise NotImplementedError
