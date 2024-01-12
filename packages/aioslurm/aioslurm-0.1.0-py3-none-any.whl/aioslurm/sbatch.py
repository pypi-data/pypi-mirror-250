"""sbatch."""
from __future__ import annotations

import logging
import os
import typing

import jinja2
import jinja2.nodes

from aioslurm import settings, utils


__all__ = ["SBatchOutput", "sbatch", "render_to_sbatch"]


logger = logging.getLogger(__name__)


_jinja_environment = jinja2.Environment(
    autoescape=jinja2.select_autoescape(),
    enable_async=True,
    loader=jinja2.FileSystemLoader(searchpath=settings.TEMPLATE_PATHS),
)
_jinja_environment.globals.update(aioslurm=utils.metadata)


class SBatchOutput(typing.NamedTuple):
    """sbatch output properties."""

    job_id: str

    cluster: str | None

    @classmethod
    def from_string(class_, source: str, /) -> SBatchOutput:
        """Constructs SBatchOutput instance from sbatch output content."""
        parts = source.split(";")
        job_id = parts[0]
        cluster = parts[1] if 1 < len(parts) else None
        return SBatchOutput(job_id=job_id, cluster=cluster)


async def sbatch(
    *args: str,
    input: utils.subprocess.RunCommandInput | None = None,
    working_directory: os.PathLike | None = None,
) -> SBatchOutput:
    """Runs sbatch.

    Takes batch script content as input."""

    try:
        output, error, subprocess = await utils.subprocess.run_command(
            "sbatch",
            "--parsable",
            *args,
            input=input,
            working_directory=working_directory,
            timeout=settings.SBATCH_COMMAND_TIMEOUT,
        )
    except utils.exceptions.CommandError as exception:
        logger.error(
            f"sbatch failed: {exception}.",
            extra={"input": input, "working_directory": working_directory},
        )
        raise

    logger.info(
        f"sbatch completed: {output.strip() if output else ''}",
        extra={
            "input": input,
            "output": output,
            "error": error,
            "working_directory": working_directory,
            "subprocess": subprocess,
        },
    )

    if not output:
        raise utils.exceptions.CommandValueError(
            "sbatch command returned no output."
        )

    return SBatchOutput.from_string(output)


async def render_to_sbatch(
    template: str | jinja2.Template | list[str | jinja2.Template],
    context: dict[str, typing.Any] | None = None,
    *,
    working_directory: os.PathLike | None = None,
) -> SBatchOutput:
    """Render a batch script from a template object and context, and pass it to
    sbatch."""
    if context is None:
        context = {}

    selected_template = _jinja_environment.get_or_select_template(template)

    return await sbatch(
        input=selected_template.render_async(**context),
        working_directory=working_directory,
    )


async def _render_from_string_to_sbatch(
    source: str,
    /,
    *,
    context: dict[str, typing.Any] | None = None,
    working_directory: os.PathLike | None = None,
) -> SBatchOutput:
    """Render a batch script from a template string and context, and pass it to
    sbatch."""
    template = _jinja_environment.from_string(source=source.strip())
    return await render_to_sbatch(
        template=template, context=context, working_directory=working_directory
    )


render_to_sbatch.from_string = (  # type: ignore[attr-defined]
    _render_from_string_to_sbatch
)
