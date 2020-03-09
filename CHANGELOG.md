# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2020-03-09

### Added

- New `Option.collect` constructor to create an `Option[Tuple[T, ...]]`
  from an iterable of `Option[T]`. If all Options in the iterator are `Some[T]`,
  they are collected into a tuple in the resulting `Some`. If any are
  `Nothing()`, the result is `Nothing()`.

## [1.3.1] - 2020-02-21

### Fixed

- Fix pylint `assignment-from-no-return` warnings for methods that can only
  raise, seen when pylint can determine whether a value is an Ok/Err or
  Some/Nothing and you try to e.g. `Err(5).expect("no good")`.

## [1.3.0] - 2019-01-12

### Added

- Testing in CI for Python 3.8
- `Option.raise_if_nothing(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T`
  added as a semantically friendly alias for `Option.expect`.

### Deprecated

- `Option.raise_if_err` is deprecated in favor of `Option.raise_if_nothing`.
  Will be removed in `2.0.0`

## [1.2.0] - 2019-01-09

### Added

- `Result.raise_if_err(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T`
  added as a semantically friendly alias for `Result.expect`.
- `Option.raise_if_err(self, msg: str, exc_cls: t.Type[Exception] = RuntimeError) -> T`
  added as a semantically friendly alias for `Option.expect`.

## [1.1.0] - 2019-01-03

### Added

- `Result.collect(iterable: Iterable[T, E]) -> Result[Tuple[T, ...], E]`  added
  to collect an iterable of results into a single result, short-circuiting
  if any errors are encountered

## [1.0.2] - 2019-12-12

### Fixed

- `Result.expect()` and `Result.expect_err()` now appends the stringified
  `Err` or `Ok` result to the provided `msg`.

## [1.0.1] - 2019-12-09

### Fixed

- All interface methods now, through the magic of dependent imports, specify
  that they should return implementation instances. This makes working with
  functions specified to return a `Result` or an `Option` much easier (1780999)

## [1.0.0] - 2019-05-19

### Added

- Result and Option generic type interfaces
- Ok and Err Result implementations
- Some and Nothing Option implementations
- CI pipeline with Azure pipelines
- Full public interface testing
- Makefile for common operations, including venv setup, linting, formatting,
  and testing
- Basic benchmarks for analyzing performance
- Apache license

[Unreleased]: https://github.com/mplanchard/safetywrap/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/mplanchard/safetywrap/compare/v1.3.1...v1.4.0
[1.3.1]: https://github.com/mplanchard/safetywrap/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/mplanchard/safetywrap/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/mplanchard/safetywrap/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/mplanchard/safetywrap/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/mplanchard/safetywrap/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/mplanchard/safetywrap/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/mplanchard/safetywrap/compare/f87fa5b1a00af5ef26213e576730039d87f7163b...v1.0.0
