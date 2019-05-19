"""Typesafe python versions of Rust-inspired result types."""


__version__ = "1.0.0"
__version_info__ = tuple(map(lambda part: int(part), __version__.split(".")))


# pylama: ignore=W0611
from ._interface import Option, Result
from ._impl import Ok, Err, Some, Nothing
