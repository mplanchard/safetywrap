"""A benchmark to be run externally.

Executes a program that might make heavy use of Result/Option types
in one of two ways: classically, with exceptions, or using result types.

The program checks several data stores (in memory to minimize interference
from slow IO &c.) in order for a key. If it finds it, it gets the value,
adds something to it, and then overwrites the value.
"""

import sys
import typing as t

from timeit import timeit

from result_types import Some, Nothing, Ok, Err, Option, Result


T = t.TypeVar("T")


class ClassicalDataStore:
    def __init__(self, values: dict = None) -> None:
        self._values = values or {}

    def connect(self, fail: bool = False) -> "ClassicalDataStore":
        """'Connect' to the store."""
        if fail:
            raise RuntimeError("Failed to connect")
        return self

    def get(self, key: str) -> t.Any:
        """Return a value from the store."""
        return self._values.get(key)

    def insert(self, key: str, val: T, overwrite: bool = False) -> T:
        """Insert the value and return it."""
        if key in self._values and not overwrite:
            raise KeyError("Key already exists")
        self._values[key] = val
        return val


class MonadicDataStore:
    """Using the monadic types."""

    def __init__(self, values: dict = None) -> None:
        self._values = values or {}

    def connect(self, fail: bool = False) -> Result["MonadicDataStore", str]:
        if fail:
            return Err("failed to connect")
        return Ok(self)

    def get(self, key: str) -> Option[t.Any]:
        """Return a value from the store."""
        if key in self._values:
            return Some(self._values[key])
        return Nothing()

    def insert(
        self, key: str, val: T, overwrite: bool = False
    ) -> Result[T, str]:
        """Insert the value and return it."""
        if key in self._values and not overwrite:
            return Err("Key already exists")
        self._values[key] = val
        return Ok(val)


class Classical:
    """Run the program in the classical way."""

    def __init__(self) -> None:
        self._stores = {
            0: ClassicalDataStore(),
            1: ClassicalDataStore(),
            2: ClassicalDataStore(),
            3: ClassicalDataStore({"you": "me"}),
        }

    def run(self) -> None:
        """Run the program."""
        for store in self._stores.values():
            try:
                store = store.connect()
            except RuntimeError:
                continue
            val = store.get("you")
            if val is not None:
                new_val = val + "et"
                try:
                    inserted = store.insert("you", new_val)
                except KeyError:
                    # oops, need to specify overwrite
                    inserted = store.insert("you", new_val, overwrite=True)
                assert inserted == "meet"
                break
        else:
            raise RuntimeError("Could not get value anywhere.")


class Monadic:
    """Use the monadic types."""

    def __init__(self) -> None:
        self._stores = {
            0: MonadicDataStore(),
            1: MonadicDataStore(),
            2: MonadicDataStore(),
            3: MonadicDataStore({"you": "me"}),
        }

    def run(self) -> None:
        """Run the program."""
        for unconnected in self._stores.values():
            connected = unconnected.connect()
            if connected.is_err():
                continue
            store = connected.unwrap()
            inserted = (
                store.get("you")
                .ok_or("no such val")
                .map(lambda val: str(val + "et"))
                .and_then(
                    lambda val: store.insert("you", val).or_else(
                        lambda _: store.insert("you", val, overwrite=True)
                    )
                )
            )
            if inserted.is_ok():
                assert inserted.unwrap() == "meet"
                break
        else:
            raise RuntimeError("Could not get value anywhere")


if __name__ == "__main__":
    to_run = sys.argv[1].lower()

    switch: t.Dict[str, t.Callable[[], None]] = {
        "classical": lambda: Classical().run(),
        "monadic": lambda: Monadic().run(),
    }

    if to_run not in switch:
        raise RuntimeError("No such method: {}".format(to_run))

    if len(sys.argv) > 2 and sys.argv[2] == "timeit":
        # run internal timings
        NUMBER = int(1e6)
        taken = timeit("switch[to_run]()", globals=globals(), number=NUMBER)
        print(taken / NUMBER)
    else:
        switch[to_run]()
