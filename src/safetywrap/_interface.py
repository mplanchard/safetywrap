"""Result and Option interfaces."""

import typing as t

if t.TYPE_CHECKING:
    from ._impl import Option, Result  # pylint: disable=unused-import

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
    def of(
        fn: t.Callable[..., T],
        *args: t.Any,
        catch: t.Type[ExcType] = Exception,  # type: ignore
        **kwargs: t.Any
    ) -> "Result[T, ExcType]":
        """Call `fn` and wrap its result in an `Ok()`.

        If an exception is intercepted, return `Err(exception)`. By
        default, any `Exception` will be intercepted. If you specify
        `exc_type`, only that exception will be intercepted.
        """
        raise NotImplementedError

    @staticmethod
    def collect(
        iterable: t.Iterable["Result[T, E]"],
    ) -> "Result[t.Tuple[T, ...], E]":
        """Convert an iterable of Results into a Result of an iterable.

        Given some iterable of type Iterable[Result[T, E]], try to collect
        all Ok values into a tuple of type Tuple[T, ...]. If any of the
        iterable items are Errs, short-circuit and return Err of type
        Result[E].
        """
        raise NotImplementedError

    @staticmethod
    def err_if(predicate: t.Callable[[T], bool], value: T) -> "Result[T, T]":
        """Return Err(val) if predicate(val) is True, otherwise Ok(val)."""
        raise NotImplementedError

    @staticmethod
    def ok_if(predicate: t.Callable[[T], bool], value: T) -> "Result[T, T]":
        """Return Ok(val) if predicate(val) is True, otherwise Err(val)."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def and_(self, res: "Result[U, E]") -> "Result[U, E]":
        """Return `res` if self is `Ok`, otherwise return `self`."""
        raise NotImplementedError

    def or_(self, res: "Result[T, F]") -> "Result[T, F]":
        """Return `res` if self is `Err`, otherwise `self`."""
        raise NotImplementedError

    def and_then(self, fn: t.Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """Call `fn` if Ok, or ignore an error. Alias of `flatmap`.

        This can be used to chain functions that return results.
        """
        raise NotImplementedError

    def flatmap(self, fn: t.Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """Call `fn` if Ok, or ignore an error. Alias of `and_then`

        This can be used to chain functions that return results.
        """
        raise NotImplementedError

    def or_else(self, fn: t.Callable[[E], "Result[T, F]"]) -> "Result[T, F]":
        """Return `self` if `Ok`, or call `fn` with `self` if `Err`."""
        raise NotImplementedError

    def err(self) -> "Option[E]":
        """Return Err value if result is Err."""
        raise NotImplementedError

    def ok(self) -> "Option[T]":
        """Return OK value if result is Ok."""
        raise NotImplementedError

    def expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T:
        """Return `Ok` value or raise an error with the specified message.

        The raised exception class may be specified with the `exc_cls`
        keyword argument.

        The underlying error will be stringified and appended to the
        provided message.
        """
        raise NotImplementedError

    def raise_if_err(
        self, msg: str, exc_cls: t.Type[Exception] = RuntimeError
    ) -> T:
        """Return `Ok` value or raise an error with the specified message.

        The raised exception class may be specified with the `exc_cls`
        keyword argument.

        The underlying error will be stringified and appended to the
        provided message.

        Alias of `expect`.
        """
        raise NotImplementedError

    def expect_err(
        self, msg: str, exc_cls: t.Type[Exception] = RuntimeError
    ) -> E:
        """Return `Err` value or raise an error with the specified message.

        The raised exception class may be specified with the `exc_cls`
        keyword argument.

        The underlying result will be stringified and appended to the
        provided message.
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

    def map(self, fn: t.Callable[[T], U]) -> "Result[U, E]":
        """Map a function onto an okay result, or ignore an error."""
        raise NotImplementedError

    def map_err(self, fn: t.Callable[[E], F]) -> "Result[T, F]":
        """Map a function onto an error, or ignore a success."""
        raise NotImplementedError

    def unwrap(self) -> T:
        """Return an Ok result, or throw an error if an Err."""
        raise NotImplementedError

    def unwrap_err(self) -> E:
        """Return an Ok result, or throw an error if an Err."""
        raise NotImplementedError

    def unwrap_or(self, alternative: U) -> t.Union[T, U]:
        """Return the `Ok` value, or `alternative` if `self` is `Err`."""
        raise NotImplementedError

    def unwrap_or_else(self, fn: t.Callable[[E], U]) -> t.Union[T, U]:
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
    def of(value: t.Optional[T]) -> "Option[T]":
        """Construct an _Option[T] from an Optional[T]."""
        raise NotImplementedError

    @staticmethod
    def nothing_if(predicate: t.Callable[[T], bool], value: T) -> "Option[T]":
        """Return Nothing() if predicate(val) is True, else Some(val)."""
        raise NotImplementedError

    @staticmethod
    def some_if(predicate: t.Callable[[T], bool], value: T) -> "Option[T]":
        """Return Some(val) if predicate(val) is True, else Nothing()."""
        raise NotImplementedError

    @staticmethod
    def collect(options: t.Iterable["Option[T]"]) -> "Option[t.Tuple[T, ...]]":
        """Collect a series of Options into single Option.

        If all options are `Some[T]`, the result is `Some[Tuple[T]]`. If
        any options are `Nothing`, the result is `Nothing`.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def and_(self, alternative: "Option[U]") -> "Option[U]":
        """Return `Nothing` if `self` is `Nothing`, or the `alternative`."""
        raise NotImplementedError

    def or_(self, alternative: "Option[T]") -> "Option[T]":
        """Return option if it is `Some`, or the `alternative`."""
        raise NotImplementedError

    def xor(self, alternative: "Option[T]") -> "Option[T]":
        """Return Some IFF exactly one of `self`, `alternative` is `Some`."""
        raise NotImplementedError

    def and_then(self, fn: t.Callable[[T], "Option[U]"]) -> "Option[U]":
        """Return `Nothing`, or call `fn` with the `Some` value."""
        raise NotImplementedError

    def flatmap(self, fn: t.Callable[[T], "Option[U]"]) -> "Option[U]":
        """Return `Nothing`, or call `fn` with the `Some` value."""
        raise NotImplementedError

    def or_else(self, fn: t.Callable[[], "Option[T]"]) -> "Option[T]":
        """Return option if it is `Some`, or calculate an alternative."""
        raise NotImplementedError

    def expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T:
        """Unwrap and yield a `Some`, or throw an exception if `Nothing`.

        The exception class may be specified with the `exc_cls` keyword
        argument.
        """
        raise NotImplementedError

    def raise_if_err(
        self, msg: str, exc_cls: t.Type[Exception] = RuntimeError
    ) -> T:  # noqa: D401
        """DEPRECATED: Use `raise_if_nothing` or `expect`.

        Unwrap and yield a `Some`, or throw an exception if `Nothing`.

        The exception class may be specified with the `exc_cls` keyword
        argument.

        Alias of `expect`.
        """
        raise NotImplementedError

    def raise_if_nothing(
        self, msg: str, exc_cls: t.Type[Exception] = RuntimeError
    ) -> T:
        """Unwrap and yield a `Some`, or throw an exception if `Nothing`.

        The exception class may be specified with the `exc_cls` keyword
        argument.

        Alias of `expect`.
        """
        raise NotImplementedError

    def filter(self, predicate: t.Callable[[T], bool]) -> "Option[T]":
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

    def map(self, fn: t.Callable[[T], U]) -> "Option[U]":
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

    def ok_or(self, err: E) -> "Result[T, E]":
        """Transform an option into a `Result`.

        Maps `Some(v)` to `Ok(v)` or `None` to `Err(err)`.
        """
        raise NotImplementedError

    def ok_or_else(self, err_fn: t.Callable[[], E]) -> "Result[T, E]":
        """Transform an option into a `Result`.

        Maps `Some(v)` to `Ok(v)` or `None` to `Err(err_fn())`.
        """
        raise NotImplementedError

    def unwrap(self) -> T:
        """Return `Some` value, or raise an error."""
        raise NotImplementedError

    def unwrap_or(self, default: U) -> t.Union[T, U]:
        """Return the contained value or `default`."""
        raise NotImplementedError

    def unwrap_or_else(self, fn: t.Callable[[], U]) -> t.Union[T, U]:
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
