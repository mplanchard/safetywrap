"""Mixins for common class functionality."""

import typing as t


class Immutable:
    """Disallow setting attributes on a class.

    Utilizers must call `Immutable.__init__(self)` in their
    initialization code.
    """

    __slots__ = ("_instantiated",)

    def __init__(self) -> None:
        """Set the _instantiated instance var."""
        self._instantiated = True

    def __setattr__(self, key: str, val: t.Any) -> None:
        """Prevent attribute setting on instantiated classes."""
        try:
            if self._instantiated:
                raise TypeError(
                    "{} is immutable.".format(self.__class__.__name__)
                )
        except AttributeError:
            pass
        object.__setattr__(self, key, val)
