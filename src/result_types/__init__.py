"""Typesafe python versions of Rust-inspired result types."""


__version__ = "0.0.1"
__version_info__ = tuple(map(lambda part: int(part), __version__.split(".")))


# pylama: ignore=W0611
from result_types._result_types import Err, Ok, Option, Nothing, Some, Result
