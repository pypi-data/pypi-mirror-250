"""Exceptions."""
from __future__ import annotations

import abc
import subprocess  # nosec: B404

from aioslurm import exceptions


class CommandError(exceptions.AIOSlurmException, metaclass=abc.ABCMeta):
    """Base aioslurm command error exception."""

    pass


class CommandFileNotFoundError(CommandError, FileNotFoundError):
    """Raised when a command doesn't exist."""

    pass


class CommandProcessError(CommandError, subprocess.CalledProcessError):
    """Raised when a process returns a non-zero exit status."""

    pass


class CommandTimeoutError(CommandError, subprocess.TimeoutExpired):
    """Raised when a timeout expires while waiting for a child process."""

    pass


class CommandValueError(CommandError, exceptions.ValueError):
    """Raised for value errors when running commands."""

    pass
