"""Test meta-requirements of the implementations."""

import typing as t

import pytest

from result_types import Some, Nothing, Option, Ok, Err, Result


class TestInterfaceConformance:
    """Ensure the implementations implement and do not extend the interfaces.

    This is a bit of a unique situation, where the usual open-closed
    principle does not apply. We want our implementations to conform
    EXACTLY to the interface, and not to extend it, since the whole
    idea here is that you can treat an Ok() the same as an Err(),
    or a Some() the same as a Nothing.
    """

    @staticmethod
    def _public_method_names(obj: object) -> t.Tuple[str, ...]:
        """Return public method names from an object."""
        return tuple(
            sorted(
                map(
                    lambda i: i[0],
                    filter(
                        lambda i: not i[0].startswith("_") and callable(i[1]),
                        obj.__dict__.items(),
                    ),
                )
            )
        )

    def test_ok_interface(self) -> None:
        """"The Ok interface matches Result."""
        assert self._public_method_names(Ok) == self._public_method_names(
            Result
        )

    def test_err_interface(self) -> None:
        """The Err interface matches Result."""
        assert self._public_method_names(Err) == self._public_method_names(
            Result
        )

    def test_some_interface(self) -> None:
        """The Some interface matches Option."""
        assert self._public_method_names(Some) == self._public_method_names(
            Option
        )

    def test_nothing_interface(self) -> None:
        """The Nothing interface matches Option."""
        assert self._public_method_names(Nothing) == self._public_method_names(
            Option
        )


class TestInterfaceAbstractness:
    """Interfaces should not contain any implementations."""

    def test_result_abstract(self) -> None:
        """The result interface contains no implementations."""
        with pytest.raises(NotImplementedError):
            r: Result[str, str] = Result("a")
            assert r

    def test_option_abstract(self) -> None:
        """The option interface contains no implementations."""
        with pytest.raises(NotImplementedError):
            Option("a")
