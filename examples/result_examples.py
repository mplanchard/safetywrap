"""Examples showing how one might use the Result portion of this library."""

import typing as t

import requests

from safetywrap import Result, Ok, Err


# ######################################################################
# One: Validation Pipeline
# ######################################################################
# Sometimes you've got a bunch of validation functions that you would
# like to run on some data, and you want to bail early if any of them
# fails. Particularly when you want to send back some information about
# what failed to validate, you're forced to e.g. return a 2-tuple of
# validation status and a string with info, or to raise a custom
# exception with that data ensconced inside. In either case, you wind
# up having to do a lot of if/else or try/except logic in the calling
# context. The Result type allows you to get rid of all that extra
# boilerplate and get down to what matters: defining a pipeline of
# validation errors with early exiting.
# ######################################################################


class Validator:
    """A validator for validating hopefully valid things.

    In this case, let's say we've got a a string we want to validate.
    We want the string to be at least X characters long, to not contain
    any disallowed characters, to start with a capital letter, to end
    with a period, and to contain the substring "shabazz".
    """

    MIN_LEN = 10
    DISALLOWED_CHARS = ("^", "_", "O")
    MUST_CONTAIN = "shabazz"

    def validated(self, string: str) -> Result[str, str]:
        """Return the validated string or any validation error.

        We return a Result, where the Ok value is the validated string,
        and the Err value is a descriptive string.
        """
        # Because all of our validation methods return Results, we can
        # easily chain them.
        return (
            self._validate_length(string)
            .and_then(self._validate_chars)  # and_then == flatmap
            .and_then(self._validate_capitalized)
            .and_then(self._validate_end_char)
            .and_then(self._validate_substring)
            # Because we're returning a Result, this is all we need to
            # to! We don't even have to figure out if there was an error
            # here, because any error would have short-circuited the
            # pipeline and will get returned by this method.
        )
        # Because we're returning a Result, we are _forcing_ the caller
        # to deal with the fact that validation might fail. They only
        # way they can get the result back is by calling `.unwrap()`
        # or a similar method, checking `is_ok()` first, or otherwise
        # continuing to pipeline on it and pass the  Result on up the
        # chain.

    def _validate_length(self, string: str) -> Result[str, str]:
        """Check that all the strings are of the proper length."""
        if len(string) < self.MIN_LEN:
            return Err("String is too short")
        return Ok(string)

    def _validate_chars(self, string: str) -> Result[str, str]:
        """Check that none of the strings have disallowed chars."""
        if set(string).intersection(set(self.DISALLOWED_CHARS)):
            return Err("String has disallowed chars")
        return Ok(string)

    def _validate_capitalized(self, string: str) -> Result[str, str]:
        """Check that the starting character is a capital."""
        if len(string) > 0 and not string[0].isupper():
            return Err("Starting character is not uppercase.")
        return Ok(string)

    def _validate_end_char(self, string: str) -> Result[str, str]:
        """Check the string ends with a period."""
        if len(string) > 0 and string[-1] != ".":
            return Err("String does not end with a period")
        return Ok(string)

    def _validate_substring(self, string: str) -> Result[str, str]:
        """Check the string has the required substring."""
        if self.MUST_CONTAIN not in string:
            return Err(f"String did not contain '{self.MUST_CONTAIN}'")
        return Ok(string)

    def test_self(self) -> None:
        """Quick test to make sure we're not crazy."""
        goods = ("AshabazzB.", "Abshabazz.")
        bads = ("shabazz", "Ab.", "Ashabazz^B.")
        assert all(map(lambda g: self.validated(g).is_ok(), goods))
        assert all(map(lambda g: self.validated(g).is_err(), bads))
        print("Validator.test_self: everything as expected!")


# ######################################################################
# Two: Wrangling Exceptions
# ######################################################################
# It's common in FP-related tutorials to hear exceptions described as
# children throwing tantrums, but it's really worse than that. Calling
# a method that might throw involves either figuring out in detail any
# exception that might be thrown or catching every exception all
# william-nilliam and then dealing with them generically. Doing either
# of the two means that you've got to litter your code with try/except
# blocks, forcing you to consider what the _implementation_ of the thing
# you're using is than what _interface_ you're trying to create.
# Using Result.of can make life easier.
# ######################################################################


class CatFactGetter:
    """Do something fraught with error.

    Let's forget them all the possible errors and just care about what
    we're trying to do, which is to get a cat fact.

    NOTE: this requires the `requests` library to be installed
    """

    def get_fact(self) -> str:
        """Get a cat fact!"""
        return (
            # Create a Result from making our GET request.
            # Now we can start chaining!
            Result.of(
                requests.get, "https://cat-fact.herokuapp.com/facts/random"
            )
            # Let's first consider the success path.
            # If we got a response, it should be JSON, so let's try to parse
            .and_then(lambda resp: Result.of(resp.json))
            # If we successfully parsed JSON, we must have a dict, so let's
            # grab our cat fact, or a useful message.
            .map(
                lambda parsed: t.cast(
                    str, parsed.get("text", "Unexpected cat fact format!")
                )
            )
            # From here, all we need to do to consider the error case is
            # convert our Err type (which for Result.of() is any exception
            # that was raised) into the expected return type, which we
            # do by passing the error to `str()`
            .unwrap_or_else(str)
        )

        # Note it would also be totally reasonable to return something like
        # Result[str, Exception] here! In which case you drop the final
        # `.unwrap_or_else()`, and then the caller can decide what to
        # do with any errors.

    def get_fact_result(self) -> Result[str, Exception]:
        """Return a Result for a cat fact."""
        return (
            Result.of(
                requests.get,
                "https://cat-fact.herokuapp.com/facts/random",
                # this is the default, but sometimes the type checker wants us
                # to make it explicit. See python/mypy#3737 for deets.
                catch=Exception,
            )
            .and_then(lambda resp: Result.of(resp.json))
            .map(
                lambda parsed: t.cast(
                    str, parsed.get("text", "Unexpected cat fact format!")
                )
            )
        )

    def test_get_fact(self) -> None:
        """Test getting a cat fact."""
        fact = self.get_fact()
        assert isinstance(fact, str)
        print(fact)

    def test_get_fact_result(self) -> None:
        """Test getting a cat fact as a result!

        Note that here, the caller has to decide what to do with any
        potential error in order to get to the cat fact.
        """
        fact_res = self.get_fact_result()
        fact_str = fact_res.unwrap_or_else(lambda exc: f"ERROR: {str(exc)}")
        assert isinstance(fact_str, str)
        if fact_res.is_err():
            assert "ERROR" in fact_str
        print(fact_str)


if __name__ == "__main__":
    Validator().test_self()
    CatFactGetter().test_get_fact()
    CatFactGetter().test_get_fact_result()
