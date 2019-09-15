"""Ensure decorator return types are accurate."""

import typing as t


# pylint: disable=no-name-in-module

from mypy.plugin import FunctionContext, Plugin
from mypy.types import CallableType


DECORATORS = frozenset(
    ("wrap of Result", "wrap_for of Result", "wrap of Option")
)


def update_decorator(function_ctx: FunctionContext) -> CallableType:
    """Return the updated decorator."""
    decorated_fn_ctx: CallableType = (  # type: ignore
        function_ctx.arg_types[0][0]
    )
    function_ctx.default_return_type.arg_types = (  # type: ignore
        decorated_fn_ctx.arg_types
    )
    function_ctx.default_return_type.arg_kinds = (  # type: ignore
        decorated_fn_ctx.arg_kinds
    )
    function_ctx.default_return_type.arg_names = (  # type: ignore
        decorated_fn_ctx.arg_names
    )
    return function_ctx.default_return_type  # type: ignore


class TypedDecorators(Plugin):
    """Provide a typed decorator plugin."""

    def get_function_hook(  # type: ignore
        self, fullname: str
    ) -> t.Optional[t.Callable[[FunctionContext], t.Type]]:
        """Get the function hook."""
        # print(fullname)
        if fullname in DECORATORS:
            return update_decorator  # type: ignore
        return None


def plugin(_: str) -> t.Type[Plugin]:
    """Entrypoint."""
    return TypedDecorators
