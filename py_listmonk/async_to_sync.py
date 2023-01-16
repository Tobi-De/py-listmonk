"""
shamelessly copied from https://github.com/procrastinate-org/procrastinate/blob/main/procrastinate/utils.py#L115
"""

import asyncio
import functools
import types
from typing import (
    Any,
    Awaitable,
    Type,
    TypeVar,
)

T = TypeVar("T")
U = TypeVar("U")

SYNC_ADDENDUM = """

        This method is the synchronous counterpart of `{}`.
"""

ASYNC_ADDENDUM = """

        This method is the asynchronous counterpart of `{}`.
"""


def add_sync_api(cls: Type) -> Type:
    """
    Applying this decorator to a class with async methods named "<name>_async"
    will create a sync version named "<name>" of these methods that performs the same
    thing but synchronously.
    """
    # Iterate on all class attributes
    for attribute_name in dir(cls):
        add_method_sync_api(cls=cls, method_name=attribute_name)

    return cls


def add_method_sync_api(*, cls: Type, method_name: str, suffix: str = "_async"):
    if method_name.startswith("_") or not method_name.endswith(suffix):
        return

    attribute, function = get_raw_method(cls=cls, method_name=method_name)

    # Keep only async def methods
    if not asyncio.iscoroutinefunction(function):
        return

    if isinstance(attribute, types.FunctionType):  # classic method
        method_type = "method"
    elif isinstance(attribute, classmethod):
        method_type = "classmethod"
    elif isinstance(attribute, staticmethod):
        method_type = "staticmethod"
    else:
        raise ValueError(f"Invalid object of type {type(attribute)}")

    attribute.__doc__ = attribute.__doc__ or ""

    # Create a wrapper that will call the method in a run_until_complete
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if method_type == "method":
            final_class = type(args[0])
        elif method_type == "classmethod":
            final_class = args[0]
        else:
            final_class = cls

        _, function = get_raw_method(cls=final_class, method_name=method_name)

        awaitable = function(*args, **kwargs)
        return sync_await(awaitable=awaitable)

    sync_name = method_name[: -len(suffix)]
    attribute.__doc__ += ASYNC_ADDENDUM.format(sync_name)

    final_wrapper: Any
    if method_type == "method":
        final_wrapper = wrapper
    elif method_type == "classmethod":
        final_wrapper = classmethod(wrapper)
    else:
        final_wrapper = staticmethod(wrapper)

    # Save this new method on the class
    wrapper.__name__ = sync_name
    final_wrapper.__doc__ = final_wrapper.__doc__ or ""
    final_wrapper.__doc__ += SYNC_ADDENDUM.format(method_name)
    setattr(cls, sync_name, final_wrapper)


def get_raw_method(cls: Type, method_name: str):
    """
    Extract a method from the class, without triggering the descriptor.
    Return 2 objects:

    - the method itself stored on the class (which may be a function, a classmethod or
      a staticmethod)
    - The real function underneath (the same function as above for a normal method,
      and the wrapped function for static and class methods).

    """
    # Methods are descriptors so using getattr here will not give us the real method
    cls_vars = vars(cls)
    method = cls_vars[method_name]

    # If method is a classmethod or staticmethod, its real function, that may be
    # async, is stored in __func__.
    wrapped = getattr(method, "__func__", method)

    return method, wrapped


def sync_await(awaitable: Awaitable[T]) -> T:
    """
    Given an awaitable, awaits it synchronously. Returns the result after it's done.
    """

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(awaitable)
