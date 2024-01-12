"""Exceptions."""
from __future__ import annotations

import abc
import builtins


class AIOSlurmException(builtins.Exception, metaclass=abc.ABCMeta):
    """Base aioslurm exception."""

    pass


class ValueError(AIOSlurmException, builtins.ValueError):
    """Base aioslurm value error exception."""

    pass


class ValidationError(AIOSlurmException, builtins.ValueError):
    """Base aioslurm validation error exception."""

    pass
