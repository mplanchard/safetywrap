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

## Usage

This library provides generic `Result[T, E]` and `Option[T]` types for Python,
as well as `Ok(t)` and `Err(e)` implementations of the `Result` type, and
`Some(t)` and `Nothing` implementations of the `Option` type.

For an overview of the Result type in Rust, check out [Recoverable Errors with `Result`](https://doc.rust-lang.org/1.30.0/book/2018-edition/ch09-02-recoverable-errors-with-result.html)
from the Rust book.

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
