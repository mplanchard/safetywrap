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

**Get an enum member by its value, returning the member or None.**

```py
import typing as t
from enum import Enum

from result_types import Option, Result, Some

E = t.TypeVar("E", bound=Enum)

def enum_member_for_val(enum: t.Type[E], value: t.Any) -> Option[E]:
    """Return Some(enum_member) or Nothing()."""
    # Enums throw a `ValueError` if the value isn't present, so
    # we'll either have `Ok(enum_member)` or `Err(ValueError)`.
    # We unwrap and return the member if it's Ok, otherwise, we just
    # return None
    return Result.of(enum, value).unwrap_or(None)
```

**Get an enum member by its value, returning an Option.**

```py
import typing as t
from enum import Enum

from result_types import Option, Result, Some

E = t.TypeVar("E", bound=Enum)

def enum_member_for_val(enum: t.Type[E], value: t.Any) -> Option[E]:
    """Return Some(enum_member) or Nothing()."""
    return (
        # Enums throw a `ValueError` if the value isn't present, so
        # we'll either have `Ok(enum_member)` or `Err(ValueError)`
        Result.of(enum, value)
        # If it's Ok, wrap it in a Some
        .map(Some)
        # Return our Some(enum_member), or return Nothing()
        .unwrap_or(Nothing())
    )
```

**Serialize a dict that may be missing keys, using default values.**

```py
import json
from result_types import Result

def serialize(data: t.Dict[str, t.Union[int, str, float]]) -> str:
    """Serialize the data. Absent keys are [absent], rather than Null."""
    absent = "[absent]"
    keys = ("first", "second", "third", "fourth")
    # We can even use Result to catch any JSON serialization errors, so that
    # this function will _always_ return a string!
    Result.of(
        json.dumps,
        # Result.of() will intercept the KeyError and return an Err. We use
        # `unwrap_or()` to discard the error and return the "[absent]" string
        # instead; if the key was present, the Result was Ok, and we just
        # return that value.
        {k: Result.of(lambda: data[k]).unwrap_or(absent) for k in keys}
    ).unwrap_or("Could not serialize JSON from data!")
```

**Make an HTTP request, and if the status code is 200, convert the body
to JSON and return the `data` key. If there is an error or the `data`
key does not exist, return an error string.**

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

[rust-result]: (https://doc.rust-lang.org/std/result/)
[rust-option]: (https://doc.rust-lang.org/std/option/)
