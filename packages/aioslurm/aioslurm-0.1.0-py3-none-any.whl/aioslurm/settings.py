"""Settings."""
from __future__ import annotations

import datetime
import logging
import os


def str_to_bool(value: str) -> bool:
    """Convert a string representation of truth to a boolean.

    True values are 'y', 'yes', 't', 'true', 'on', '1', and 'enabled'.
    Everything else is False.
    """

    return value.lower() in {"y", "yes", "t", "true", "on", "1", "enabled"}


DEFAULT_LOG_LEVEL = logging.INFO


SBATCH_COMMAND_TIMEOUT = datetime.timedelta(
    seconds=int(os.environ.get("AIOSLURM_SBATCH_COMMAND_TIMEOUT", "30"))
)


TEMPLATE_PATHS = os.environ.get("AIOSLURM_TEMPLATE_PATH", "templates").split(
    ":"
)


USE_UVLOOP = str_to_bool(os.environ.get("AIOSLURM_USE_UVLOOP", "True"))
