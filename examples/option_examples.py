"""Examples showing how one might use the Option portion of the library."""

import typing as t
from hashlib import sha256

from safetywrap import Option


# ######################################################################
# One: Dealing with Dicts: Possibly Missing Values
# ######################################################################
# A key that might be missing from a dictionary causes all sorts of
# diversions in your application code. Instead of being able to say,
# try to get this, then do that, then do this, then do that, you have
# to immediately consider: wait, what do I do if the key is absent?
# Option.of() gives us a way to consider what we want to do all in one
# continuous flow, before considering other options.
# ######################################################################


def formatted_payment_amount(payment_details: dict) -> str:
    """Get the formatted payment amount from a dictionary.

    In our dictionary, the payment amount is present as pennies.
    """
    return (
        # Option.of() takes something that might be null and makes an
        # Option out of it: Nothing() if it's null, Some(val) if it's not.
        Option.of(payment_details.get("payment_amount"))
        # If we got the payment amount, we know it's an int of pennies.
        # Let's make it a float of dollars.
        .map(lambda val: val / 100)
        # Then let's format it into a string!
        .map("${:.2f}".format)
        # Now we've got our happy path, so all we need to do is figure
        # out what to show if our value was missing. In that case,
        # let's say we just say $0.00
        .unwrap_or("$0.00")
    )


def test_formatted_payment_amount_present() -> None:
    """It works when it works."""
    assert formatted_payment_amount({"payment_amount": 1000}) == "$10.00"


def test_formatted_payment_amount_absent() -> None:
    """It works when it works."""
    assert formatted_payment_amount({}) == "$0.00"


# ######################################################################
# Two: Functions that May Return None
# ######################################################################
# Lots of times, you might have a function that could potentially return
# None. Typically, in these cases, you have to hope and pray that your
# callers will handle the null case appropriately (typing helps with
# this significantly!). In addition, for conscientious callers, this
# adds the burden of adding a new branch to every bit of code that calls
# your function, interrupting the way the code reads to deal with the
# potential null. Returning an Option gives your callers the ability to
# focus on what they want to do, and to only worry about the nulls later.
# ######################################################################


class UsersDB:
    """It's pretty much a hard-coded database."""

    def __init__(self) -> None:
        """Set up the users."""
        self._users = {
            1: {
                "name": "bob",
                # sha256 hashed PW, no salt
                "password": (
                    "f52ccfb92d96d002c8f933eee1fd80968a1b"
                    "06271ab1a7a414ea563b2e8e1042"
                ),
            },
            2: {
                # this is a schemaless DB, and someone forgot to add
                # a password for this user!
                "name": "webscale McGee",
            },
        }

    def get(self, user_id: int) -> Option[t.Dict[str, str]]:
        """Get a user from the "database"."""
        return Option.of(self._users.get(user_id))


class Users:
    """Interact with users."""

    def authenticate(self, user_id: int, password: str) -> bool:
        """Authenticate a user with their username and password."""
        hasher = sha256()
        hasher.update(password.encode())
        exp_pw = hasher.hexdigest()
        return (
            # First, let's get the user! Since this is an Option, we can
            # ignore the error case and just start chaining!
            UsersDB().get(user_id)
            # If we got the user, we want to check their password.
            # Let's assume we're using MongoDB with no schema, so we don't
            # even know for sure the password field is going to be set.
            # So, we flatmap into another Option-generating function,
            # in this case, we will try to get the password
            .and_then(lambda user: Option.of(user.get("password")))
            # Now we've got the password, so let's check it to get a bool
            .map(lambda hashed_pw: hashed_pw == exp_pw)
            # At this point, our happy path is done! We've gotten a bool
            # representing whether the password matches. All we need to
            # do to finish is unwrap. For any of our Nothing cases (
            # user was not present, password was not present), we can
            # just return False.
            .unwrap_or(False)
        )

    def test_authenticate_user_present(self) -> None:
        """Check that things work when a user is present."""
        assert Users().authenticate(1, "tardigrade") is True

    def test_authenticate_user_absent(self) -> None:
        """If a user is absent, we cannot authenticate."""
        assert Users().authenticate(-1, "tardigrade") is False

    def test_authenticate_password_missing(self) -> None:
        """If a user has no password, we cannot authenticate."""
        assert Users().authenticate(2, "tardigrade") is False

    def test_authenticate_password_mismatch(self) -> None:
        """If the password is wrong, we cannot authenticate."""
        assert Users().authenticate(1, "slime_mold") is False

    # Consider that, using the "normal" approach, to get all of these
    # failure cases handled, we would have needed THREE separate
    # if/else blocks: one for getting None back from the DB, another
    # for if the PW is not present on the user object, and for
    # if the PWs don't match. Here, we were able to handle all of it
    # by defining our expected success case, and then considering
    # a fallback at the very end!


if __name__ == "__main__":
    # Handling absent dict values inline
    test_formatted_payment_amount_present()
    test_formatted_payment_amount_absent()

    # The utility of functions that return Options
    Users().test_authenticate_user_present()
    Users().test_authenticate_user_absent()
    Users().test_authenticate_password_missing()
    Users().test_authenticate_password_mismatch()
