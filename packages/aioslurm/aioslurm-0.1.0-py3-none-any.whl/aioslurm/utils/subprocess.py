"""Subprocess."""
from __future__ import annotations

import asyncio
import datetime
import inspect
import logging
import os
import typing

import six

from . import exceptions


try:
    from typing import TypeAlias  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import TypeAlias


logger = logging.getLogger(__name__)


RunCommandInput: TypeAlias = typing.Union[
    bytes, str, typing.Awaitable[bytes], typing.Awaitable[str]
]


class RunCommandResult(typing.NamedTuple):
    """Structured result of run_command."""

    output: str | None

    error: str | None

    subprocess: asyncio.subprocess.Process


async def run_command(
    *command: os.PathLike | str,
    input: RunCommandInput | None = None,
    working_directory: os.PathLike | None = None,
    timeout: datetime.timedelta | None = None,
) -> RunCommandResult:
    """Wrapper for running async subprocess with timeout."""
    if not command:
        raise exceptions.CommandValueError("No command arguments provided.")

    if inspect.isawaitable(input):
        awaited_input = await input
    else:
        awaited_input = input

    bytes_input = (
        six.ensure_binary(awaited_input, encoding="utf-8")
        if awaited_input
        else None
    )

    printable_command = " ".join(str(part) for part in command)
    timeout_seconds = timeout.total_seconds() if timeout is not None else None

    logger.info(f'Running subprocess "{printable_command}"...')

    try:
        subprocess = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_directory,
        )
    except FileNotFoundError as exception:
        logger.exception(f'Command "{printable_command}" was not found.')
        raise exceptions.CommandFileNotFoundError(
            exception.errno,
            exception.strerror,
            exception.filename,
        ) from exception

    # await asyncio.wait(
    #     [
    #         self._read_stream(subprocess.stdout),
    #         self._read_stream(subprocess.stderr),
    #     ]
    # )

    try:
        stdout, stderr = await asyncio.wait_for(
            subprocess.communicate(input=bytes_input), timeout=timeout_seconds
        )
    except asyncio.TimeoutError as exception:
        subprocess.terminate()
        raise exceptions.CommandTimeoutError(
            cmd=command, timeout=timeout_seconds or 0
        ) from exception

    logger.debug(
        f'Subprocess finished with return code "{subprocess.returncode}".'
    )

    output = six.ensure_str(stdout, encoding="utf-8") if stdout else None
    error = six.ensure_str(stderr, encoding="utf-8") if stderr else None

    if subprocess.returncode:
        logger.warning(
            f'Subprocess "{printable_command}" returned error '
            f'"{subprocess.returncode}": "{error}".',
            extra={
                "code": subprocess.returncode,
                "command": command,
                "error": error,
                "output": output,
                "subprocess": subprocess,
            },
        )
        raise exceptions.CommandProcessError(
            returncode=subprocess.returncode,
            cmd=command,
            output=output,
            stderr=error,
        )
    else:
        logger.debug(
            f'Subprocess "{printable_command}" completed.',
            extra={"subprocess": subprocess},
        )

    return RunCommandResult(output=output, error=error, subprocess=subprocess)
