"""Examples showing how one might use the Option portion of the library."""

import typing as t

from safetywrap import Option, Some, Nothing


# ######################################################################
# Example One: Dealing with Dicts Pt 1: Possibly Missing Values
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
