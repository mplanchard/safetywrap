"""Typesafe python versions of Rust-inspired result types."""

__all__ = ("Option", "Result", "Ok", "Err", "Some", "Nothing")
__version__ = "1.4.0"
__version_info__ = tuple(map(int, __version__.split(".")))


from ._impl import Option, Result, Ok, Err, Some, Nothing
