"""Compare execution speed with exceptions."""

import typing as t
from math import sqrt
from timeit import timeit


from result_types import Ok, Err, Result, Some, Option, Nothing


def sqrt_exception(val: int) -> float:
    """Return the square root or raise an exception."""
    if val < 0:
        raise ValueError("No imagination here.")
    return sqrt(val)


def sqrt_result(val: int) -> Result[float, int]:
    """Return a Result instead of raising."""
    if val < 0:
        return Err(val)
    return Ok(sqrt(val))


def _do_more_math(val: float) -> float:
    """Do more math on the float."""
    return val ** 2 / 15 + 7


def map_from_exception_ok() -> float:
    """Check exception raising code in the OK case."""
    return _do_more_math(sqrt_exception(4))


def map_from_exception_err() -> float:
    """Check exception raising code in the error case."""
    try:
        return _do_more_math(sqrt_exception(-4))
    except ValueError:
        return -1


def map_from_result_ok() -> float:
    """Check result returning code in the OK case."""
    val = sqrt_result(4).map(_do_more_math).unwrap()
    return val


def map_from_result_err() -> float:
    """Check result returning code in the Err case."""
    val = sqrt_result(4).map(_do_more_math).unwrap_or(-1)
    return val


def from_dict_optional(dictionary: t.Dict[str, int], key: str) -> Option[int]:
    """Return an Option from a dictionary."""
    val = dictionary.get(key)
    if val is not None:
        return Some(val)
    return Nothing()


def from_dict_regular(dictionary: dict, key: str) -> t.Optional[int]:
    """Optionally return from a dictionary."""
    return dictionary.get(key)


def operate_on_optional_dict_value() -> int:
    """Operate on an optional dict value."""
    return from_dict_optional({"a": 1}, "a").map(lambda i: i + 1).unwrap()


def operate_on_normal_dict_value() -> int:
    """Operate on a normal dict value."""
    val = from_dict_regular({"a": 1}, "a")
    if val is not None:
        val1 = val + 1
    else:
        raise RuntimeError
    reveal_type(val1)
    return val1


@Result.wrap
def foo(a: int, b: t.Optional[str]) -> int:
    pass


print(Result.wrap.__name__)
print(Result.wrap.__qualname__)

reveal_type(foo)


if __name__ == "__main__":

    NUM = int(1e6)

    exc_happy_path = timeit("map_from_exception_ok()", globals=globals())
    print(f"Exception, happy path: {exc_happy_path/NUM}")

    exc_sad_path = timeit("map_from_exception_err()", globals=globals())
    print(f"Exception, sad path: {exc_sad_path/NUM}")

    res_happy_path = timeit("map_from_result_ok()", globals=globals())
    print(f"Result, happy path: {res_happy_path/NUM}")

    res_sad_path = timeit("map_from_result_err()", globals=globals())
    print(f"Result, sad path: {res_sad_path/NUM}")

    dict_opt = timeit("operate_on_optional_dict_value()", globals=globals())
    print(f"Result, option dict: {dict_opt/NUM}")

    dict_reg = timeit("operate_on_normal_dict_value()", globals=globals())
    print(f"Result, regular dict: {dict_reg/NUM}")
