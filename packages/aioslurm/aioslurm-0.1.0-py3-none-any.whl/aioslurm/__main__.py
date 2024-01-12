"""CLI commands."""
from __future__ import annotations

import getpass
import logging
import os
import sys
import typing

import click
import rich.console
import rich.logging
import sentry_sdk

import aioslurm

from . import utils


logger = logging.getLogger(__name__)


sentry_sdk.init(release=f"{aioslurm.__title__}@{aioslurm.__version__}")
sentry_sdk.set_user({"id": os.getuid(), "username": getpass.getuser()})


@click.group()
@click.option("--debug", "debug", is_flag=True, default=False)
@click.option(
    "--log-level",
    "log_level",
    type=click.Choice(list(logging._nameToLevel.keys()), case_sensitive=False),
    callback=lambda context, parameter, value: logging.getLevelName(  # pragma: no cover  # noqa: E501
        value
    )
    if value
    else None,
    default=None,
)
@click.version_option(aioslurm.__version__)
@click.pass_context
def main(
    context: click.Context,
    debug: typing.Literal[True] | None,
    log_level: int | None,
) -> None:
    """Main entry point. Configures logging."""
    context.ensure_object(dict)
    context.obj["log_level"] = utils.get_log_level(
        log_level=log_level, debug=debug
    )
    context.obj["stderr_console"] = rich.console.Console(stderr=True)
    context.obj["stdout_console"] = rich.console.Console()

    console_handler = rich.logging.RichHandler(
        console=context.obj["stderr_console"],
        rich_tracebacks=True,
        show_time=context.obj["stderr_console"].is_terminal,
        show_path=context.obj["log_level"] == logging.DEBUG,
    )
    console_handler.setFormatter(
        logging.Formatter(
            fmt="{name} - {message}",
            datefmt=f"[{logging.Formatter.default_time_format}]",
            style="{",
        )
    )

    logging.basicConfig(
        format="{asctime} {levelname} - {name} - {message}",
        handlers=[console_handler],
        level=context.obj["log_level"],
        style="{",
    )
    logging.getLogger(name="aioslurm").setLevel(context.obj["log_level"])


@main.command(short_help="Run.")
@click.pass_context
@utils.click.coroutine
async def run(context: click.Context) -> None:
    """Placeholder run command."""
    if context.obj["stderr_console"].is_terminal:
        utils.banner(console=context.obj["stderr_console"])

    # TODO


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(prog_name=aioslurm.__title__))
