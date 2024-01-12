"""Utility functions."""
from __future__ import annotations

import logging
import os
import socket

import rich.console
import rich.logging
import rich.text

import aioslurm
from aioslurm import settings

from . import click, exceptions, subprocess  # nosec: B404


__all__ = ["banner", "click", "exceptions", "get_log_level", "subprocess"]


logger = logging.getLogger(__name__)


metadata = {
    "author": aioslurm.__author__,
    "copyright": aioslurm.__copyright__,
    "hostname": socket.getfqdn(),
    "license": aioslurm.__license__,
    "title": aioslurm.__title__,
    "url": aioslurm.__url__,
    "version": aioslurm.__version__,
}


def banner(*, console: rich.console.Console) -> None:
    """Prints banner to console."""
    ascii_art = r"""
      _        _
 __ _(_)___ __| |_  _ _ _ _ __
/ _` | / _ (_-< | || | '_| '  \
\__,_|_\___/__/_|\_,_|_| |_|_|_|

"""

    text = rich.text.Text()
    for line, position in zip(ascii_art.splitlines(), [0, 11, 11, 11, 12, 0]):
        text.append(line[:position], style="bold magenta")
        text.append(line[position:], style="bold yellow")
        text.append("\n")

    console.print(
        text,
        crop=True,
        highlight=False,
        no_wrap=True,
        overflow="crop",
        width=32,
    )

    logger.info(
        f"{aioslurm.__title__}, "
        f"version {aioslurm.__version__}. "
        f"{aioslurm.__copyright__}.",
        extra=metadata,
    )


def get_log_level(
    log_level: int | None = None, debug: bool | None = None
) -> int:
    """Determines log level based on environment log level and debug flags."""
    env_log_level = logging._nameToLevel.get(
        os.environ.get("AIOSLURM_LOG_LEVEL", "").upper(),
    )

    env_debug = settings.str_to_bool(os.environ.get("AIOSLURM_DEBUG", "False"))

    is_debug = bool(
        debug
        or env_debug
        or log_level == logging.DEBUG
        or env_log_level == logging.DEBUG
    )

    if is_debug:
        return logging.DEBUG
    elif log_level:
        return log_level
    elif env_log_level:
        return env_log_level
    else:
        return settings.DEFAULT_LOG_LEVEL
