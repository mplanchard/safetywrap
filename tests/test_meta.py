"""Test meta-requirements of the implementations."""

import typing as t

import pytest

from safetywrap._interface import _Option, _Result
from safetywrap import Some, Nothing, Option, Ok, Err, Result


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

    @staticmethod
    def filter_meths(cls: t.Type, meth: str) -> bool:
        if not callable(getattr(cls, meth)):
            return False
        if not meth.startswith("_"):
            return True
        check_magic_methods = ("eq", "init", "iter", "ne", "repr", "str")

        if any(map(lambda m: meth == "__%s__" % m, check_magic_methods)):
            return True

        return False

    @pytest.mark.parametrize(
        "meth",
        filter(
            lambda m: TestNoConcretesInInterfaces.filter_meths(_Result, m),
            _Result.__dict__,
        ),
    )
    def test_no_concrete_result_methods(self, meth: str) -> None:
        """The result interface contains no implementations."""
        self.assert_not_concrete(_Result, meth)

    @pytest.mark.parametrize(
        "meth",
        filter(
            lambda m: TestNoConcretesInInterfaces.filter_meths(_Option, m),
            _Option.__dict__,
        ),
    )
    def test_no_concrete_option_methods(self, meth: str) -> None:
        """The option interface contains no implementations."""
        self.assert_not_concrete(_Option, meth)


class TestImplementationDetails:
    """Some implementation details need to be tested."""

    def test_nothing_singleton(self) -> None:
        """Ensure Nothing() is a singleton."""
        assert Nothing() is Nothing() is Nothing()

    @pytest.mark.parametrize("obj", (Some(1), Nothing(), Ok(1), Err(1)))
    def test_all_slotted(self, obj: t.Any) -> None:
        """All implementations use __slots__."""
        assert not hasattr(obj, "__dict__")
