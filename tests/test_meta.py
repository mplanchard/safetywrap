"""Test meta-requirements of the implementations."""

import typing as t

import pytest

from result_types._interface import _Option, _Result
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
            _Result
        )

    def test_err_interface(self) -> None:
        """The Err interface matches Result."""
        assert self._public_method_names(Err) == self._public_method_names(
            _Result
        )

    def test_some_interface(self) -> None:
        """The Some interface matches Option."""
        assert self._public_method_names(Some) == self._public_method_names(
            _Option
        )

    def test_nothing_interface(self) -> None:
        """The Nothing interface matches Option."""
        assert self._public_method_names(Nothing) == self._public_method_names(
            _Option
        )


class TestNoBaseInstantiations:
    """Base types are not instantiable"""

    def test_result_cannot_be_instantiated(self) -> None:
        """Result cannot be instantiated"""
        with pytest.raises(NotImplementedError):
            r: Result[str, str] = Result("a")
            assert r

    def test_option_cannot_be_instantiated(self) -> None:
        """Option cannot be instantiated"""
        with pytest.raises(NotImplementedError):
            Option("a")


class TestNoConcretesInInterfaces:
    """Interfaces contain only abstract methods."""

    @staticmethod
    def assert_not_concrete(kls: t.Type, meth: str) -> None:
        """Assert the method on the class is not concrete."""
        with pytest.raises(NotImplementedError):
            for num_args in range(10):
                try:
                    getattr(kls, meth)(*map(str, range(num_args)))
                except TypeError:
                    continue
                else:
                    break

    @pytest.mark.parametrize(
        "meth",
        filter(lambda attr: callable(getattr(_Result, attr)), _Result.__dict__),
    )
    def test_no_concrete_result_methods(self, meth: str) -> None:
        """The result interface contains no implementations."""
        self.assert_not_concrete(_Result, meth)

    @pytest.mark.parametrize(
        "meth",
        filter(lambda attr: callable(getattr(_Option, attr)), _Option.__dict__),
    )
    def test_no_concrete_option_methods(self, meth: str) -> None:
        """The option interface contains no implementations."""
        self.assert_not_concrete(_Option, meth)


class TestImplementationDetails:
    """Some implementation details need to be tested."""

    def test_nothing_singleton(self) -> None:
        """Ensure Nothing() is a singleton."""
        assert Nothing() is Nothing() is Nothing()

    def test_ok_immutable(self) -> None:
        """Results may not be mutated."""
        with pytest.raises(TypeError):
            Ok("a")._value = "some other value"

    def test_err_immutable(self) -> None:
        """Results may not be mutated."""
        with pytest.raises(TypeError):
            Err("a")._value = "some other value"

    def test_some_immutable(self) -> None:
        """Options may not be mutated."""
        with pytest.raises(TypeError):
            Some("a")._value = "some other value"

    def test_nothing_immutable(self) -> None:
        """Options may not be mutated."""
        with pytest.raises(TypeError):
            Nothing()._value = None
