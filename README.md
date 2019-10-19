# result-types

[![pipeline status](https://gitlab.com/mplanchard/result-types/badges/master/pipeline.svg)](https://gitlab.com/mplanchard/result-types/commits/master)
[![Build Status](https://dev.azure.com/msplanchard/result-types/_apis/build/status/mplanchard.result-types?branchName=master)](https://dev.azure.com/msplanchard/result-types/_build/latest?definitionId=2&branchName=master)
[![coverage report](https://gitlab.com/mplanchard/result-types/badges/master/coverage.svg)](https://gitlab.com/mplanchard/result-types/commits/master)

Fully typesafe, Rust-like result types for Python

This project was developed for and is graciously sponsored by my employer,
[Bestow, Inc.](https://hellobestow.com/). At Bestow, we aim to democratize life
insurance by providing simple, easy coverage, purchasable online in five minutes
with no doctors' visits and no hassles.

We're pretty much always hiring great developers, so if you'd like to work
with us, please check out [our careers page](https://hellobestow.com/careers/)!

## Summary

This library provides two main types: `Result` and `Option`. These types
allow you to specify typesafe code that effectively handles errors or
absent data, without resorting to deeply nested if-statements and lots
of try-except blocks.

This is accomplished by allowing you to operate on an `Option` or `Result`
in a sort of quantum superposition, where an `Option` could be `Some` or
`Nothing` or a `Result` could be `Ok` or `Err`. In either case, all of the
methods on the type work just the same, allowing you to handle both cases
elegantly.

A `Result[T, E]` may be an instance of `Ok[T]` or `Err[E]`.

An `Option[T]` may be an instance of `Some[T]` or `Nothing`.

These types are heavily influenced by the [Result][rust-result] and
[Option][rust-option] types in Rust.

Thorough type specifications for mypy or your favorite python type-checker
are provided, so that you can decorate function inputs and outputs as
returning `Result` and `Option` types and get useful feedback when supplying
arguments or passing return values.

## Examples

In general, these examples build from simple to complex. See [Usage](#usage)
below for the full API specification.

### Get an enum member by its value, returning the member or None

```py
import typing as t
from enum import Enum

from result_types import Option, Result, Some

T = t.TypeVar("T", bound=Enum)

def enum_member_for_val(enum: t.Type[T], value: t.Any) -> Option[T]:
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

### Result[T,E]

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

Example:

```py
import json

def parse_json(string: str) -> Result[dict, Exception]:
    """Parse a JSON object into a dict."""
    return Result.of(json.loads, string)
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
Result. This method is an alias of [`flatmap`](#result.flatmap)

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
Result. This method is an alias of [`and_then`](#result.and_then)

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
instantiated with the provided message. By default, a `RuntimeError` is raised,
but an alternative error may be provided using the `exc_cls` keyword argument.

Example:

```py
import pytest

with pytest.raises(RuntimeError) as exc:
    Err(5).expect("5 is right out!")
    assert str(exc.value) == "5 is right out!"

assert Ok(1).expect("5 is right out") == 1
```

##### Result.expect_err

`Result.expect_err(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> E`

Return the wrapped value if this Result is `Err`. Otherwise, raise an error,
instantiated with the provided message. By default, a `RuntimeError` is raised,
but an alternative error may be provided using the `exc_cls` keyword argument.

Example:

```py
import pytest

with pytest.raises(RuntimeError) as exc:
    Ok(5).expect_err("5 is right out!")
    assert str(exc.value) == "5 is right out!"

assert Err(1).expect_err("5 is right out") == 1
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

##### Result.__iter__

`Result.__iter__(self) -> t.Iterator[T]`

Implement the iterator protocol, allowing iteration over the results of
[`Result.iter`](#result.iter). If this Result is `Ok`, return an iterator
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

##### Result.__eq__

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

##### Result.__ne__

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

##### Result.__str__

`Result.__str__(self) -> str`

Enable useful stringification via `str()`.

Example:

```py
assert str(Ok(5)) == "Ok(5)"
assert str(Err(5)) == "Err(5)"
```

##### Result.__repr__

`Result.__repr__(self) -> str`

Enable useful stringification via `repr()`.

Example:

```py
assert repr(Ok(5)) == "Ok(5)"
assert repr(Err(5)) == "Err(5)"
```

## Performance

Benchmarks may be run with `make bench`. Benchmarking utilities are provided
in [`bench`](/bench).

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

Summary: the `Result` and `Option` wrapper types add minimal overhead to
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
class in order to avoid needing to perform lots of `isinstance()` checks,
which are notoriously slow in Python.

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

* `make test` - run tests using your local interpreter
* `make fmt` - format code using [black](https://github.com/python/black)
* `make lint` - check code with a variety of analysis tools
* `make bench` - run benchmarks

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
