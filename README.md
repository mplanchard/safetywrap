# result-types
[![pipeline status](https://gitlab.com/mplanchard/result-types/badges/master/pipeline.svg)](https://gitlab.com/mplanchard/result-types/commits/master)
[![coverage report](https://gitlab.com/mplanchard/result-types/badges/master/coverage.svg)](https://gitlab.com/mplanchard/result-types/commits/master)

Fully typesafe, Rust-like result types for Python

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
