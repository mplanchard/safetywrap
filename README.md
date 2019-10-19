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

### Examples

In general, these examples build from simple to complex. See [Usage](#usage)
below for the full API specification.

#### Get an enum member by its value, returning the member or None

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

#### Get an enum member by its value, returning an Option

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

#### Serialize a dict that may be missing keys, using default values

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

#### Make an HTTP request, and if the status code is 200, convert the body to JSON and return the `data` key. If there is an error or the `data` key does not exist, return an error string

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
        # And now we get either the Ok string or the Err string!
        .unsafe_unwrap()
    )
```

## Usage

## Performance

Benchmarking utilities are provided in [`bench`](/bench).

Benchmarks may be run with `make bench`

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

The CI system requires that `make lint` and `make test` run successfully
(exit status of 0) in order to merge code.

`result_types` is compatible with Python >= 3.6. You can run against
all supported python versions with `make test-all-versions`. This requires
that `docker` be installed on your local system.

[hyperfine]: https://github.com/sharkdp/hyperfine
[rust-result]: https://doc.rust-lang.org/std/result/
[rust-option]: https://doc.rust-lang.org/std/option/
