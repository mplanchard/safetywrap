# safetywrap

[![Build Status](https://dev.azure.com/msplanchard/safetywrap/_apis/build/status/mplanchard.safetywrap?branchName=master)](https://dev.azure.com/msplanchard/safetywrap/_build/latest?definitionId=3&branchName=master)
[![coverage report](https://img.shields.io/azure-devops/coverage/msplanchard/safetywrap/3)](https://dev.azure.com/msplanchard/safetywrap/_build?definitionId=3)

Fully typesafe, Rust-inspired wrapper types for Python values

## Summary

This library provides two main wrappers: `Result` and `Option`. These types
allow you to specify typesafe code that effectively handles errors or
absent data, without resorting to deeply nested if-statements and lots
of try-except blocks.

This is accomplished by allowing you to operate on an `Option` or `Result`
in a sort of quantum superposition, where an `Option` could be `Some` or
`Nothing` or a `Result` could be `Ok` or `Err`. In either case, all of the
methods on the type work just the same, allowing you to handle both cases
elegantly.

A `Result[T, E]` may be an instance of `Ok[T]` or `Err[E]`, while an `Option[T]`
may be an instance of `Some[T]` or `Nothing`. Either way, you get to treat
them just the same until you really need to get the wrapped value.

So, rather than this:

```py
for something in "value", None:
    if something is not None:
        val = something.upper()
    else:
        val = "DEFAULT"
    print(val)
```

You can do this:

```py
for something in Some("value"), Nothing():
    print(something.map(str.upper).unwrap_or("DEFAULT"))
```

And rather than this:

```py
for jsondata in '{"value": "myvalue"}', '{badjson':
    try:
        config = capitalize_keys(json.loads(jsondata))
    except Exception:
        config = get_default_config()
    print(config["value"])
```

You can do this:

```py
for jsondata in '{"value": "myvalue"}', '{badjson':
    print(
        Result.of(json.loads, jsondata)
        .map(capitalize_keys)
        .unwrap_or_else(get_default_config)["value"]
    )
```

These two examples are super minimal samples of how using these typesafe
wrappers can make things easier to write and reason about. Please see the
[Examples](#examples) section for more, and [Usage](#usage) for the full
suite of offered functionality.

These types are heavily influenced by the [Result][rust-result] and
[Option][rust-option] types in Rust.

Thorough type specifications for mypy or your favorite python type-checker
are provided, so that you can decorate function inputs and outputs as
returning `Result` and `Option` types and get useful feedback when supplying
arguments or passing return values.

### Sponsorship

This project was developed for and is graciously sponsored by my employer,
[Bestow, Inc.](https://hellobestow.com/). At Bestow, we aim to democratize life
insurance by providing simple, easy coverage, purchasable online in five minutes
with no doctors' visits and no hassles.

We're pretty much always hiring great developers, so if you'd like to work
with us, please check out [our careers page](https://hellobestow.com/careers/)!

## Table of Contents

- [safetywrap](#safetywrap)
  - [Summary](#summary)
    - [Sponsorship](#sponsorship)
  - [Table of Contents](#table-of-contents)
  - [Examples](#examples)
    - [Get an enum member by its value, returning the member or None](#get-an-enum-member-by-its-value-returning-the-member-or-none)
    - [Get an enum member by its value, returning an Option](#get-an-enum-member-by-its-value-returning-an-option)
    - [Serialize a dict that may be missing keys, using default values](#serialize-a-dict-that-may-be-missing-keys-using-default-values)
    - [Make an HTTP request, and if the status code is 200, convert the body to JSON and return the `data` key. If there is an error or the `data` key does not exist, return an error string](#make-an-http-request-and-if-the-status-code-is-200-convert-the-body-to-json-and-return-the-data-key-if-there-is-an-error-or-the-data-key-does-not-exist-return-an-error-string)
  - [Usage](#usage)
    - [Result[T, E]](#resultt-e)
      - [Result Constructors](#result-constructors)
        - [Ok](#ok)
        - [Err](#err)
        - [Result.of](#resultof)
        - [Result.collect](#resultcollect)
        - [Result.err_if](#resulterr_if)
        - [Result.ok_if](#resultok_if)
      - [Result Methods](#result-methods)
        - [Result.and_](#resultand_)
        - [Result.or_](#resultor_)
        - [Result.and_then](#resultand_then)
        - [Result.flatmap](#resultflatmap)
        - [Result.or_else](#resultor_else)
        - [Result.err](#resulterr)
        - [Result.ok](#resultok)
        - [Result.expect](#resultexpect)
        - [Result.raise_if_err](#resultraise_if_err)
        - [Result.expect_err](#resultexpect_err)
        - [Result.is_err](#resultis_err)
        - [Result.is_ok](#resultis_ok)
        - [Result.iter](#resultiter)
        - [Result.map](#resultmap)
        - [Result.map_err](#resultmap_err)
        - [Result.unwrap](#resultunwrap)
        - [Result.unwrap_err](#resultunwrap_err)
        - [Result.unwrap_or](#resultunwrap_or)
        - [Result.unwrap_or_else](#resultunwrap_or_else)
      - [Result Magic Methods](#result-magic-methods)
    - [Option[T]](#optiont)
      - [Option Constructors](#option-constructors)
        - [Some](#some)
        - [Nothing](#nothing)
        - [Option.of](#optionof)
        - [Option.nothing_if](#optionnothing_if)
        - [Option.some_if](#optionsome_if)
        - [Option.collect](#optioncollect)
      - [Option Methods](#option-methods)
        - [Option.and_](#optionand_)
        - [Option.or_](#optionor_)
        - [Option.xor](#optionxor)
        - [Option.and_then](#optionand_then)
        - [Option.flatmap](#optionflatmap)
        - [Option.or_else](#optionor_else)
        - [Option.expect](#optionexpect)
        - [Option.raise_if_nothing](#optionraise_if_nothing)
        - [Option.filter](#optionfilter)
        - [Option.is_nothing](#optionis_nothing)
        - [Option.is_some](#optionis_some)
        - [Option.iter](#optioniter)
        - [Option.map](#optionmap)
        - [Option.map_or](#optionmap_or)
        - [Option.map_or_else](#optionmap_or_else)
        - [Option.ok_or](#optionok_or)
        - [Option.ok_or_else](#optionok_or_else)
        - [Option.unwrap](#optionunwrap)
        - [Option.unwrap_or](#optionunwrap_or)
        - [Option.unwrap_or_else](#optionunwrap_or_else)
      - [Option Magic Methods](#option-magic-methods)
  - [Performance](#performance)
    - [Results](#results)
    - [Discussion](#discussion)
  - [Contributing](#contributing)

## Examples

In general, these examples build from simple to complex. See [Usage](#usage)
below for the full API specification.

### Get an enum member by its value, returning the member or None

```py
import typing as t
from enum import Enum

from result_types import Option, Result, Some

T = t.TypeVar("T", bound=Enum)

def enum_member_for_val(enum: t.Type[T], value: t.Any) -> t.Optional[t.Any]:
    """Return Some(enum_member) or Nothing()."""
    # Enums throw a `ValueError` if the value isn't present, so
    # we'll either have `Ok(enum_member)` or `Err(ValueError)`.
    # We unwrap and return the member if it's Ok, otherwise, we just
    # return None
    return Result.of(enum, value).unwrap_or(None)
```

### Get an enum member by its value, returning an Option

```py
import typing as t
from enum import Enum

from result_types import Option, Result, Some

T = t.TypeVar("T", bound=Enum)

def enum_member_for_val(enum: t.Type[T], value: t.Any) -> Option[T]:
    """Return Some(enum_member) or Nothing()."""
    # Enums throw a `ValueError` if the value isn't present, so
    # we'll either have `Ok(enum_member)` or `Err(ValueError)`.
    # Calling `ok()` on a `Result` returns an `Option`
    return Result.of(enum, value).ok()
```

### Serialize a dict that may be missing keys, using default values

```py
import json
from result_types import Result

def serialize(data: t.Dict[str, t.Union[int, str, float]]) -> str:
    """Serialize the data.

    Absent keys are "[absent]", rather than null. This allows us to maintain
    information about whether a key was present or actually set to None.
    """
    keys = ("first", "second", "third", "fourth")
    # We can even use Result to catch any JSON serialization errors, so that
    # this function will _always_ return a string!
    Result.of(
        json.dumps,
        # Result.of() will intercept the KeyError and return an Err. We use
        # `unwrap_or()` to discard the error and return the "[absent]" string
        # instead; if the key was present, the Result was Ok, and we just
        # return that value.
        {k: Result.of(lambda: data[k]).unwrap_or("[absent]") for k in keys}
    ).unwrap_or("Could not serialize JSON from data!")
```

### Make an HTTP request, and if the status code is 200, convert the body to JSON and return the `data` key. If there is an error or the `data` key does not exist, return an error string

```py
from functools import partial

import requests
from requests import Response
from result_types import Option, Result


def get_data(url: str) -> str:
    """Get the data!"""
    # We need to do manual type assignment sometimes when the code
    # we're wrapping does not provide types.
    # If the wrapped function raises any Exception, `res` will be
    # Err(Exception). Otherwise it will be `Ok(Response)`.
    res: Result[Response, Exception] = Result.of(requests.get, url)
    return (
        # We start as a `Result[Response, Exception]`
        res
        # And if we were an Err, map to a `Result[Response, str]`
        .map_err(str)
        # If we were Ok, and_then (aka flatmap) to a new `Result[Response, str]`
        .and_then(lambda res: (
            # Our return value starts as a `Result[Response, Response]`
            Result.ok_if(lambda r: r.status_code == 200, res).map_err(
                # So we map it to a `Result[Response, str]`
                lambda r: str(f"Bad status code: {r.status_code}")
            )
        ))
        # We are now a `Result[Response, str]`, where we are only Ok if
        # our status code was 200.
        # Now we transition to a `Result[dict, str]`
        .and_then(lambda res: Result.of(res.json).map_err(str))
        # And to a `Result[Option[str], str]`
        .map(lambda js: Option.of(js.get("data")).map(str))
        # And to a `Result[str, str]`
        .and_then(lambda data: data.ok_or("No data key in JSON!"))
        # If we are an error, convert us to an Ok with the error string
        .or_else(Ok)
        # And now we get either the Ok string or the Err string!
        .unwrap()
    )
```

## Usage

### Result[T, E]

A Result represents some value that may either be in an `Ok` state or
an `Err` state.

#### Result Constructors

##### Ok

`Ok(value: T) -> Result[T, E]`

Construct an `Ok` Result directly with the value.

Example:

```py
def check_value_not_negative(val: int) -> Result[int, str]:
    """Check that a value is not negative, or return an Err."""
    if val >= 0:
        return Ok(val)
    return Err(f"{val} is negative!")
```

##### Err

`Err(value: E) -> Result[T, E]`

Construct an `Err` Result directly with the value.

Example:

```py
def check_value_not_negative(val: int) -> Result[int, str]:
    """Check that a value is not negative, or return an Err."""
    if val >= 0:
        return Ok(val)
    return Err(f"{val} is negative!")
```

##### Result.of

`Result.of(fn: Callable[..., T], *args: t.Any, catch: t.Type[E], **kwargs) -> Result[T, E]`

Call a function with the provided arguments. If no error is thrown, return
`Ok(result)`. Otherwise, return `Err(exception)`. By default, `Exception`
is caught, but different error types may be provided with the `catch`
keyword argument.

The type of `E` MUST be `Exception` or one of its subclasses.

This constructor is designed to be useful in wrapping other APIs, builtin
functions, etc.

Note that due to a bug in mypy (see https://github.com/python/mypy/issues/3737),
sometimes you need to explicitly specify the `catch` keyword argument,
even if you're setting it to its default (`Exception`). This does not
happen consistently, but when it does, you will see mypy thinking
that the type of the `Result` is `Result[SomeType, <nothing>]`.

Example:

```py
import json

def parse_json(string: str) -> Result[dict, Exception]:
    """Parse a JSON object into a dict."""
    return Result.of(json.loads, string)
```

##### Result.collect

`Result.collect(iterable: Iterable[T, E]) -> Result[Tuple[T, ...], E]`

Convert an iterable of Results into a single Result. If all Results were
Ok, Ok values are collected into a Tuple in the final Result. If any Results
were Err, the Err result is returned directly.

Example:

```py
assert Result.collect([Ok(1), Ok(2), Ok(3)]) == Ok((1, 2, 3))
assert Result.collect([Ok(1), Err("no"), Ok(3)]) == Err("no")
```

##### Result.err_if

`Result.err_if(predicate: t.Callable[[T], bool], value: T) -> Result[T, T]`

Run a predicate on some value, and return `Err(val)` if the predicate returns
True, or `Ok(val)` if the predicate returns False.

Example:

```py
from requests import Response

def checked_response(response: Response) -> Result[Response, Response]:
    """Try to get a response from the server."""
    return Result.err_if(lambda r: r.status_code >= 300, response)
```

##### Result.ok_if

`Result.ok_if(predicate: t.Callable[[T], bool], value: T) -> Result[T, T]`

Run a predicate on some value, and return `Ok(val)` if the predicate returns
True, or `Err(val)` if the predicate returns False.

Example:

```py
def checked_data(data: dict) -> Result[dict, dict]:
    """Check if data has expected keys."""
    expected_keys = ("one", "two", "three")
    return Result.ok_if(lambda d: all(k in d for k in expected_keys), data)
```

#### Result Methods

##### Result.and_

`Result.and_(self, res: Result[U, E]) -> Result[U, E]`

If this Result is `Ok`, return `res`. If this result is `Err`, return this
Result. This can be used to short circuit a chain of Results on encountering
the first error.

Example:

```py
assert Ok(5).and_(Ok(6)) == Ok(6)
assert Err(1).and_(Ok(6)) == Err(1)
assert Err(1).and_(Err(2)).and_(Ok(5)) == Err(1)
assert Ok(5).and_(Err(1)).and_(Ok(6)) == Err(1)
```

##### Result.or_

`Result.or_(self, res: Result[T, F]) -> Result[T, F]`

If this Result is `Err`, return `res`. Otherwise, return this Result.

Example:

```py
assert Err(1).or_(Ok(5)) == Ok(5)
assert Err(1).or_(Err(2)) == Err(2)
assert Ok(5).or_(Ok(6)) == Ok(5)
assert Ok(5).or_(Err(1)) == Ok(5)
```

##### Result.and_then

`Result.and_then(self, fn: t.Callable[[T], Result[U, E]]) -> Result[U, E]`

If this Result is `Ok`, call the provided function with the wrapped value of
this Result and return the Result of that function. This allows easily
chaining multiple Result-generating calls together to yield a final
Result. This method is an alias of [`Result.flatmap`](#resultflatmap)

Example:

```py
assert Ok(5).and_then(lambda val: Ok(val + 1)) == Ok(6)
assert Err(1).and_then(lambda val: Ok(val + 1)) == Err(1)
```

##### Result.flatmap

`Result.flatmap(self, fn: t.Callable[[T], Result[U, E]]) -> Result[U, E]`

If this Result is `Ok`, call the provided function with the wrapped value of
this Result and return the Result of that function. This allows easily
chaining multiple Result-generating calls together to yield a final
Result. This method is an alias of [`Result.and_then`](#resultand_then)

Example:

```py
assert Ok(5).flatmap(lambda val: Ok(val + 1)) == Ok(6)
assert Err(1).flatmap(lambda val: Ok(val + 1)) == Err(1)
```

##### Result.or_else

`Result.or_else(self, fn: t.Callable[[E], Result[T, F]]) -> Result[T, F])`

If this result is `Err`, call the provided function with the wrapped error
value of this Result and return the Result of that function. This allows
easily handling potential errors in a way that still returns a final Result.

Example:

```py
assert Ok(5).or_else(Ok) == Ok(5)
assert Err(1).or_else(Ok) == Ok(1)
```

##### Result.err

`Result.err(self) -> Option[E]`

Convert this Result into an Option, returning Some(err_val) if this Result
is `Err`, or Nothing() if this Result is `Ok`.

Example:

```py
assert Ok(5).err() == Nothing()
assert Err(1).err() == Some(1)
```

##### Result.ok

`Result.ok(self) -> Option[T]`

Convert this Result into an Option, returning `Some(val)` if this Result is
`Ok`, or `Nothing()` if this result is `Err`.

Example:

```py
assert Ok(5).ok() == Some(5)
assert Err(1).ok() == Nothing()
```

##### Result.expect

`Result.expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T`

Return the wrapped value if this Result is `Ok`. Otherwise, raise an error,
instantiated with the provided message and the stringified error value.
By default, a `RuntimeError` is raised, but an alternative error may be
provided using the `exc_cls` keyword argument. This method is an alias for
[`Result.raise_if_err`](#resultraise_if_err).

Example:

```py
import pytest

with pytest.raises(RuntimeError) as exc:
    Err(5).expect("Bad value")
    assert str(exc.value) == "Bad value: 5"

assert Ok(1).expect("Bad value") == 1
```

##### Result.raise_if_err

`Result.raise_if_err(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T`

Return the wrapped value if this Result is `Ok`. Otherwise, raise an error,
instantiated with the provided message and the stringified error value.
By default, a `RuntimeError` is raised, but an alternative error may be
provided using the `exc_cls` keyword argument. This method is an alias for
[`Result.expect`](#resultexpect).

Example:

```py
import pytest

with pytest.raises(RuntimeError) as exc:
    Err(5).raise_if_err("Bad value")
    assert str(exc.value) == "Bad value: 5"

assert Ok(1).raise_if_err("Bad value") == 1
```

##### Result.expect_err

`Result.expect_err(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> E`

Return the wrapped value if this Result is `Err`. Otherwise, raise an error,
instantiated with the provided message and the stringified Ok value.
By default, a `RuntimeError` is raised, but an alternative error may be
provided using the `exc_cls` keyword argument.

Example:

```py
import pytest

with pytest.raises(RuntimeError) as exc:
    Ok(5).expect_err("Unexpected good value")
    assert str(exc.value) == "Unexpected good value: 5"

assert Err(1).expect_err("Unexpected good value") == 1
```

##### Result.is_err

`Result.is_err(self) -> bool`

Return True if this Result is `Err`, or `False` if this Result is `Ok`.

Example:

```py
assert Err(1).is_err() is True
assert Ok(1).is_err() is False
```

##### Result.is_ok

`Result.is_ok(self) -> bool`

Return True if this Result is `Ok`, or `False` if this Result is `Err`.

Example:

```py
assert Ok(1).is_err() is True
assert Err(1).is_err() is False
```

##### Result.iter

`Result.iter(self) -> Iterator[T]`

Return an iterator with length 1 over the wrapped value if this Result is `Ok`.
Otherwise, return a 0-length iterator.

Example:

```py
assert tuple(Ok(1).iter()) == (1,)
assert tuple(Err(1).iter()) == ()
```

##### Result.map

`Result.map(self, fn: t.Callable[[T], U]) -> Result[U, E]`

If this Result is `Ok`, apply the provided function to the wrapped value,
and return a new `Ok` Result with the result of the function. If this Result
is `Err`, do not apply the function and return this Result unchanged.

**Warning:** no error checking is performed while applying the provided
function, and exceptions applying the function are not caught. If you need
to map with error handling, consider using `and_then` (aka `flatmap`) in
conjunction with the `Result.of` constructor, e.g.
`assert Ok(0).and_then(partial(Result.of, lambda i: 10 / i)) == Err(ZeroDivisionError('division by zero'))`

Example:

```py
assert Ok(1).map(str) == Ok("1")
assert Err(1).map(str) == Err(1)
```

##### Result.map_err

`Result.map_err(self, fn: t.Callable[[E], F]) -> Result[T, F]`

If this Result is `Err`, apply the provided function to the wrapped value,
and return a new `Err` Result with the result of the function. If this Result
is `Ok`, do not apply the function and return this Result unchanged.

**Warning:** no error checking is performed while applying the provided
function, and exceptions applying the function are not caught.

Example:

```py
assert Err(1).map_err(lambda i: i + 1) == Err(2)
assert Ok(1).map_err(lambda i: i + 1) == Ok(1)
```

##### Result.unwrap

`Result.unwrap(self) -> T`

If this Result is `Ok`, return the wrapped value. If this Result is `Err`,
throw a `RuntimeError`.

Example:

```py
import pytest

assert Ok(1).unwrap() == 1

with pytest.raises(RuntimeError):
    Err(1).unwrap()
```

##### Result.unwrap_err

`Result.unwrap_err(self) -> E`

If this Result is `Err`, return the wrapped value. If this Result is `Ok`,
throw a `RuntimeError`.

Example:

```py
import pytest

assert Err(1).unwrap() == 1

with pytest.raises(RuntimeError):
    Ok(1).unwrap()
```

##### Result.unwrap_or

`Result.unwrap_or(self, alternative: U) -> t.Union[T, U]`

If this Result is `Ok`, return the wrapped value. Otherwise, if this Result
is `Err`, return the provided alternative.

Example:

```py
assert Ok(1).unwrap_or(5) == 1
assert Err(1).unwrap_or(5) == 5
```

##### Result.unwrap_or_else

`Result.unwrap_or_else(self, fn: t.Callable[[E], U]) -> t.Union[T, U]`

If this Result is `Ok`, return the wrapped value. Otherwise, if this Result
is `Err`, call the supplied function with the wrapped error value and return
the result.

Example:

```py
assert Ok(1).unwrap_or_else(str) == 1
assert Err(1).unwrap_or_else(str) == "1"
```

#### Result Magic Methods

##### Result.__iter__  <!-- omit in toc -->

`Result.__iter__(self) -> t.Iterator[T]`

Implement the iterator protocol, allowing iteration over the results of
[`Result.iter`](#resultiter). If this Result is `Ok`, return an iterator
of length 1 containing the wrapped value. Otherwise, if this Result is `Err`,
return a 0-length iterator.

Example:

```py
# Can be passed to methods that take iterators
assert tuple(Ok(1)) == (1,)
assert tuple(Err(1)) == ()

# Can be used in `for in` constructs, including comprehensions
assert [val for val in Ok(5)] == [5]
assert [val for val in Err(5)] == []


# More for-in usage.
for val in Ok(5):
    pass
assert val == 5

val = None
for val in Err(1):
    pass
assert val is None
```

##### Result.__eq__ <!-- omit in toc -->

`Result.__eq__(self, other: Any) -> bool`

Enable equality checking using `==`.

Compare the Result with `other`. Return True if `other` is the same type of
Result with the same wrapped value. Otherwise, return False.

Example:

```py
assert (Ok(5) == Ok(5)) is True
assert (Ok(5) == Ok(6)) is False
assert (Ok(5) == Err(5)) is False
assert (Ok(5) == 5) is False
```

##### Result.__ne__ <!-- omit in toc -->

`Result.__ne__(self, other: Any) -> bool`

Enable inequality checking using `!=`.

Compare the Result with `other`. Return False if `other` is the same type of
Result with the same wrapped value. Otherwise, return True.

Example:

```py
assert (Ok(5) != Ok(5)) is False
assert (Ok(5) != Ok(6)) is True
assert (Ok(5) != Err(5)) is True
assert (Ok(5) != 5) is True
```

##### Result.__str__ <!-- omit in toc -->

`Result.__str__(self) -> str`

Enable useful stringification via `str()`.

Example:

```py
assert str(Ok(5)) == "Ok(5)"
assert str(Err(5)) == "Err(5)"
```

##### Result.__repr__ <!-- omit in toc -->

`Result.__repr__(self) -> str`

Enable useful stringification via `repr()`.

Example:

```py
assert repr(Ok(5)) == "Ok(5)"
assert repr(Err(5)) == "Err(5)"
```

### Option[T]

An Option represents either `Some` value or `Nothing`.

#### Option Constructors

##### Some

`Some(value: T) -> Option[T]`

Construct a `Some` Option directly with a value.

Example:

```py
def file_contents(path: str) -> Option[str]:
    """Return the file contents or Nothing."""
    try:
        with open(path) as f:
            return Some(f.read())
    except IOError:
        return Nothing()
```

##### Nothing

`Nothing() -> Option[T]`

Construct a `Nothing` Option directly with a value.

Note: as an implementation detail, `Nothing` is implemented as a singleton,
to avoid instantiation time for any `Nothing` created after the first.
However since this is an implementation detail, `Nothing` Options should
still be compared with `==` rather than `is`.

Example:

```py
def file_contents(path: str) -> Option[str]:
    """Return the file contents or Nothing."""
    try:
        with open(path) as f:
            return Some(f.read())
    except IOError:
        return Nothing()
```

##### Option.of

`Option.of(value: t.Optional[T]) -> Option[T]`

Convert an optional value into an Option. If the value is not `None`, return
`Some(value)`. Otherwise, if the value is `None`, return `Nothing()`.

Example:

```py
assert Option.of(None) == Nothing()
assert Option.of({}.get("a")) == Nothing()
assert Option.of("a") == Some("a")
assert Option.of({"a": "b"}) == Some("b")
```

##### Option.nothing_if

`Option.nothing_if(predicate: t.Callable[[T], bool], value: T) -> Option[T]`

Call the provided predicate function with the provided value. If the predicate
returns True, return `Nothing()`. If the predicate returns False, return
`Some(value)`.

Example:

```py
assert Option.nothing_if(lambda val: val.startswith("_"), "_private") == Nothing()
assert Option.nothing_if(lambda val: val.startswith("_"), "public") == Some("public")
```

##### Option.some_if

`Option.some_if(predicate: t.Callable[[T], bool], value: T) -> Option[T]`

Call the provided predicate function with the provided value. If the predicate
returns True, return `Some(value)`. If the predicate returns False, return
`Nothing()`.

Example:

```py
assert Option.some_if(bool, [1, 2, 3]) == Some([1, 2, 3])
assert Option.some_if(bool, []) == Nothing()
```

##### Option.collect

`Option.collect(options: t.Iterable[Option[T]]) -> Option[t.Tuple[T, ...]]`

Collect a series of Options into single Option.

If all options are `Some[T]`, the result is `Some[Tuple[T]]`. If
any options are `Nothing`, the result is `Nothing`.

Example:

```py
assert Option.collect([Some(1), Some(2), Some(3)]) == Some((1, 2, 3))
assert Option.collect([Some(1), Nothing(), Some(3)]) == Nothing()
```

#### Option Methods

##### Option.and_

`Option.and_(alternative: Option[U]) -> Option[U]`

If this Option is `Nothing`, return it unchanged. Otherwise, if this Option
is `Some`, return the provided `alternative` Option.

Example:

```py
assert Some(1).and_(Some(2)) == Some(2)
assert Nothing().and_(Some(2)) == Nothing()
assert Some(1).and_(Nothing()) == Nothing()
assert Nothing().and_(Nothing()) == Nothing()
assert Some(1).and_(Nothing()).and_(Some(2)) == Nothing()
```

##### Option.or_

`Option.or_(alternative: Option[T]) -> Option[T]`

If this Option is `Nothing`, return the provided `alternative` Option.
Otherwise, if this Option is `Some`, return it unchanged.

Example:

```py
assert Some(1).or_(Some(2)) == Some(1)
assert Some(1).or_(Nothing()) == Some(1)
assert Nothing().or_(Some(1)) == Some(1)
assert Nothing().or_(Nothing()) == Nothing()
```

##### Option.xor

`Option.xor(alternative: Option[T]) -> Option[T]`

Exclusive or. Return `Some` Option iff (if and only if) exactly one of
this Option and hte provided `alternative` are Some. Otherwise, return
`Nothing`.

Example:

```py
assert Some(1).xor(Nothing()) == Some(1)
assert Nothing().xor(Some(1)) == Some(1)
assert Some(1).xor(Some(2)) == Nothing()
assert Nothing().xor(Nothing()) == Nothing()
```

##### Option.and_then

`Option.and_then(self, fn: t.Callable[[T], Option[U]]) -> Option[U]`

If this Option is `Some`, call the provided, Option-returning function with
the contained value and return whatever Option it returns. If this Option
is `Nothing`, return it unchanged. This method is an alias for
[`Option.flatmap`](#optionflatmap)

Example:

```py
assert Some(1).and_then(lambda i: Some(i + 1)) == Some(2)
assert Nothing().and_then(lambda i: Some(i + 1)) == Nothing()
```

##### Option.flatmap

`Option.flatmap(self, fn: t.Callable[[T], Option[U]]) -> Option[U]`

If this Option is `Some`, call the provided, Option-returning function with
the contained value and return whatever Option it returns. If this Option
is `Nothing`, return it unchanged. This method is an alias for
[`Option.and_then`](#optionand_then)

Example:

```py
assert Some(1).flatmap(Some) == Some(1)
assert Nothing().flatmap(Some) == Nothing()
```

##### Option.or_else

`Option.or_else(self, fn: t.Callable[[], Option[T]]) -> Option[T]`

If this Option is `Nothing`, call the provided, Option-returning function
and return whatever Option it returns. If this Option is `Some`, return it
unchanged.

Example:

```py
assert Nothing().or_else(lambda: Some(1)) == Some(1)
assert Some(1).or_else(lambda: Some(2)) == Some(1)
```

##### Option.expect

`Option.expect(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T`

If this Option is `Some`, return the wrapped value. Otherwise, if this
Option is `Nothing`, raise an error instantiated with the provided message.
By default, a `RuntimeError` is raised, but a custom exception class may be
provided via the `exc_cls` keyword argument. This method is an alias
of [`Option.raise_if_nothing`](#optionraise_if_nothing).

Example:

```py
import pytest

with pytest.raises(RuntimeError) as exc:
    Nothing().expect("Nothing here")
    assert str(exc.value) == "Nothing here"

assert Some(1).expect("Nothing here") == 1
```

##### Option.raise_if_nothing

`Option.raise_if_nothing(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T`

If this Option is `Some`, return the wrapped value. Otherwise, if this
Option is `Nothing`, raise an error instantiated with the provided message.
By default, a `RuntimeError` is raised, but a custom exception class may be
provided via the `exc_cls` keyword argument. This method is an alias
of [`Option.expect`](#optionexpect).

Example:

```py
import pytest

with pytest.raises(RuntimeError) as exc:
    Nothing().raise_if_nothing("Nothing here")
    assert str(exc.value) == "Nothing here"

assert Some(1).raise_if_nothing("Nothing here") == 1
```

##### Option.filter

`Option.filter(self, predicate: t.Callable[[T], bool]) -> Option[T]`

If this Option is `Some`, call the provided predicate function with the wrapped
value. If the predicate returns True, return `Some` containing the wrapped
value of this Option. If the predicate returns False, return `Nothing`. If
this Option is `Nothing`, return it unchanged.

Example:

```py
def is_even(val: int) -> bool:
    """Return whether the value is even."""
    return val % 2 == 0

assert Some(2).filter(is_even) == Some(2)
assert Some(1).filter(is_even) == Nothing()
assert Nothing().filter(is_even) == Nothing()
```

##### Option.is_nothing

`Option.is_nothing(self) -> bool`

If this Option is `Nothing`, return True. Otherwise, if this Option is
`Some`, return False.

Example:

```py
assert Nothing().is_nothing() is True
assert Some(1).is_nothing() is False
```

##### Option.is_some

`Option.is_some(self) -> bool`

If this Option is `Some`. Otherwise, if this Option is `Nothing`, return False.

Example:

```py
assert Some(1).is_some() is True
assert Nothing().is_some() is False
```

##### Option.iter

`Option.iter(self) -> t.Iterator[T]`

If this Option is `Some`, return an iterator of length one over the wrapped
value. Otherwise, if this Option is `Nothing`, return a 0-length iterator.

Example:

```py
assert tuple(Some(1).iter()) == (1,)
assert tuple(Nothing().iter()) == ()
```

##### Option.map

`Option.map(self, fn: t.Callable[[T], U]) -> Option[U]`

If this Option is `Some`, apply the provided function to the wrapped value,
and return `Some` wrapping the result of the function. If this Option is
`Nothing`, return this Option unchanged.

Example:

```py
assert Some(1).map(str) == Some("1")
assert Nothing().map(str) == Nothing()
assert Some(1).map(str).map(lambda x: x + "a").map(str.upper) == Some("1A")
```

##### Option.map_or

`Option.map_or(self, default: U, fn: t.Callable[[T], U]) -> U`

If this Option is `Some`, apply the provided function to the wrapped value
and return the result. If this Option is `Nothing`, return the provided
default value.

Example:

```py
assert Some(1).map_or("no value", str) == "1"
assert Nothing().map_or("no value", str) == "no value"
```

##### Option.map_or_else

`Option.map_or_else(self, default: t.Callable[[], U], fn: t.Callable[[T], U]) -> U`

If this Option is `Some`, apply the provided function to the wrapped value and
return the result. If this Option is `Nothing`, call the provided default
function with no arguments and return the result.

Example:

```py
from datetime import datetime, date

assert Some("2005-08-28").map_or_else(
    date.today,
    lambda t: datetime.strptime(t, "%Y-%m-%d").date()
) == datetime(2005, 8, 28).date()

assert Nothing().map_or_else(
    date.today,
    lambda t: datetime.strptime(t, "%Y-%m-%d").date()
) == date.today()
```

##### Option.ok_or

`Option.ok_or(self, err: E) -> Result[T, E]`

If this Option is `Some`, return an `Ok` Result wrapping the contained
value. Otherwise, return an `Err` result wrapping the provided error.

Example:

```py
assert Some(1).ok_or("no value!") == Ok(1)
assert Nothing().ok_or("no value!") == Err("no value!")
```

##### Option.ok_or_else

`Option.ok_or_else(self, err_fn: t.Callable[[], E]) -> Result[T, E]`

If this Option is `Some`, return an `Ok` Result wrapping the contained
value. Otherwise, call the provided `err_fn` and wrap its return value
in an `Err` Result.

Example:

```py
from functools import partial

def make_err_msg(msg: str) -> str:
    """Make an error message with some starting text."""
    return f"[MY_APP_ERROR] -- {msg}"

assert Some(1).ok_or_else(partial(make_err_msg, "no value!")) == Ok(1)
assert Nothing().ok_or_else(partial(make_err_msg, "no value!")) == Err(
    "[MY_APP_ERROR] -- no value!"
)
```

##### Option.unwrap

`Option.unwrap(self) -> T`

If this Option is `Some`, return the wrapped value. Otherwise, raise a
`RuntimeError`.

Example:

```py
import pytest

assert Some(1).unwrap() == 1

with pytest.raises(RuntimeError):
    Nothing().unwrap()
```

##### Option.unwrap_or

`Option.unwrap_or(self, default: U) -> t.Union[T, U]`

If this Option is `Some`, return the wrapped value. Otherwise, return the
provided default.

Example:

```py
assert Some(1),unwrap_or(-1) == 1
assert Nothing().unwrap_or(-1) == -1
```

##### Option.unwrap_or_else

`Option.unwrap_or_else(self, fn: t.Callable[[], U]) -> t.Union[T, U]`

If this Option is `Some`, return the wrapped value. Otherwise, return the
result of the provided function.

Example:

```py
from datetime import date

assert Some(date(2001, 1, 1)).unwrap_or_else(date.today) == date(2001, 1, 1)
assert Nothing().unwrap_or_else(date.today) == date.today()
```

#### Option Magic Methods

##### Option.__iter__ <!-- omit in toc -->

`Option.__iter__(self) -> t.Iterator[T]`

Implement the iterator protocol, allowing iteration over the results of
[`Option.iter`](#optioniter). If this Option is `Ok`, return an iterator
of length 1 containing the wrapped value. Otherwise, if this Option is `Nothing`,
return a 0-length iterator.

Example:

```py
# Can be passed to methods that take iterators
assert tuple(Some(1)) == (1,)
assert tuple(Nothing()j) == ()

# Can be used in `for in` constructs, including comprehensions
assert [val for val in Some(1)] == [1]
assert [val for val in Nothing()] == []


# More for-in usage.
for val in Some(1):
    pass
assert val == 1

val = None
for val in Nothing():
    pass
assert val is None
```

##### Option.__eq__ <!-- omit in toc -->

`Option.__eq__(self, other: Any) -> bool`

Enable equality checking using `==`.

Compare this Option with `other`. Return True if `other` is the same type of
Option with the same wrapped value. Otherwise, return False.

Example:

```py
assert (Some(1) == Some(1)) is True
assert (Some(1) == Some(2)) is False
assert (Some(1) == Nothing()) is False
assert (Some(1) == 1) is False
```

##### Option.__ne__ <!-- omit in toc -->

`Option.__ne__(self, other: Any) -> bool`

Enable inequality checking using `!=`.

Compare the Option with `other`. Return False if `other` is the same type of
Option with the same wrapped value. Otherwise, return True.

Example:

```py
assert (Some(1) != Some(1)) is False
assert (Some(1) != Some(2)) is True
assert (Some(1) != Nothing()) is True
assert (Some(1) != 1) is True
```

##### Option.__str__ <!-- omit in toc -->

`Option.__str__(self) -> str`

Enable useful stringification via `str()`.

Example:

```py
assert str(Some(1)) == "Some(1)"
assert str(Nothing()) == "Nothing()"
```

##### Option.__repr__ <!-- omit in toc -->

`Option.__repr__(self) -> str`

Enable useful stringification via `repr()`.

Example:

```py
assert repr(Some(1)) == "Some(1)"
assert repr(Nothing()) == "Nothing()"
```

## Performance

Benchmarks may be run with `make bench`. Benchmarking utilities are provided
in [`bench/`](/bench).

Currently, the [`sample.py`](/bench/sample.py) benchmark defines two data
stores, one using classical python error handling (or lack thereof), and
the other using this library's wrapper types. Some simple operations
are performed using each data store for comparison.

[`runner.sh`](/bench/runner.sh) runs the benchmarks two ways. First, it uses
[hyperfine] to run the benchmarks as a normal python script 100 times and
display information about the run time. It then uses python's builtin
[timeit](https://docs.python.org/3/library/timeit.html) module to measure
the code execution time in isolation over one million runs, without the
added overhead of spinning up the interpreter to parse and run the script.

### Results

The `Result` and `Option` wrapper types add minimal overhead to
execution time, which will not be noticeable for most real-world workloads.
However, care should be taken if using these types in "hot paths."

Run in isolation, the sample code using `Result` and `Option` types is
about six times slower than builtin exception handling:

| Method    | Number of Executions | Average Execution Time | Relative to Classical |
| --------- | -------------------- | ---------------------- | --------------------- |
| Classical | 1,000,000 (1E6)      | 3.79E-6 s (3.79 &mu;s) | 1x                    |
| Wrapper   | 1,000,000 (1E6)      | 2.31E-5 s (23.1 &mu;s) | 6.09x                 |

When run as part of a Python script, there is no significant difference
between using code with these wrapper types versus code that uses builtin
exception handling and nested if statements.

| Method    | Number of Executions | Average Execution Time | Relative to Classical |
| --------- | -------------------- | ---------------------- | --------------------- |
| Classical | 100                  | 32.2 ms                | 1x                    |
| Wrapper   | 100                  | 32.5 ms                | 1.01x                 |

### Discussion

Care has been taken to make the wrapper types in this library as performant
as possible. All types use `__slots__` to avoid allocating a dictionary for
instance variables, and wrapper variants (e.g. `Ok` and `Err` for `Result`)
are implemented as separate subclasses of `Result` rather than a shared
class in order to avoid needing to perform if/else branching or `isinstance()`
checks, which are notoriously slow in Python.

That being said, using these types _is_ doing more than the builtin error
handling! Instances are being constructed and methods are being accessed.
Both of these are relatively quick in Python, but definitely not quicker
than doing nothing, so this library will probably never be quite as performant
as raw exception handling. That being said, that is not its aim! The goal
is to be as quick as possible, preferably within striking distance of
regular old idiomatic python, while providing significantly more ergonomics
and type safety around handling errors and absent data.

## Contributing

Contributions are welcome! To get started, you'll just need a local install
of Python 3.

Once you've forked and cloned the repo, you can run:

- `make test` - run tests using your local interpreter
- `make fmt` - format code using [black](https://github.com/python/black)
- `make lint` - check code with a variety of analysis tools
- `make bench` - run benchmarks

See the [`Makefile`](Makefile) for other commands.

The CI system requires that `make lint` and `make test` run successfully
(exit status of 0) in order to merge code.

`result_types` is compatible with Python >= 3.6. You can run against
all supported python versions with `make test-all-versions`. This requires
that `docker` be installed on your local system. Alternatively, if you
have all required Python versions installed, you may run `make tox` to
run against your local interpreters.

[hyperfine]: https://github.com/sharkdp/hyperfine
[rust-result]: https://doc.rust-lang.org/std/result/
[rust-option]: https://doc.rust-lang.org/std/option/
