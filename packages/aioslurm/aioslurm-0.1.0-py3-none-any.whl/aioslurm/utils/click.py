"""Custom click utils."""
from __future__ import annotations

import asyncio
import functools
import logging
import typing

import click

from aioslurm import settings


try:
    import uvloop
except ImportError:  # pragma: no cover
    uvloop = None  # type: ignore[assignment]


def coroutine(function_: typing.Callable) -> typing.Callable:
    """Decorator to allow use of coroutine as click command."""

    @functools.wraps(function_)
    def wrapper(
        context: click.Context, *args: typing.Any, **kwargs: typing.Any
    ) -> typing.Any:
        """Wraps coroutine with asyncio run."""
        context.ensure_object(dict)

        if uvloop is not None and settings.USE_UVLOOP:  # pragma: no cover
            run = uvloop.run
        else:
            run = asyncio.run  # type: ignore[assignment]

        return run(
            function_(context, *args, **kwargs),
            debug=context.obj.get("log_level") == logging.DEBUG,
        )

    return wrapper
