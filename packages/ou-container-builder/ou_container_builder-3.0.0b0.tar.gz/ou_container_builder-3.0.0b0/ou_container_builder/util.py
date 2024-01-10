"""Utility functions for working with Docker."""


def docker_run_cmd(commands: list[str]) -> str:
    """Generate a docker run command."""
    command_string = " && \\\n    ".join(commands)
    return f'RUN {command_string}'


def docker_copy_cmd(src: str, target: str, from_stage: str | None = None, chmod: str | None = None) -> str:
    """Generate a docker copy command."""
    options = ""
    if from_stage is not None:
        options = f"--from={from_stage}"
    if chmod is not None:
        options = f"{options} --chmod={chmod}"
    return f'COPY {options} ["{src}", "{target}"]'
