"""Functionality for setting up the build arguments."""
from rich.progress import Progress

from ou_container_builder.state import State


def init(state: State) -> None:
    """Set the default ARGs."""
    state.update(
        {
            "docker_args": [
                {"name": "TARGETPLATFORM", "value": None},
            ]
        }
    )


def generate(state: State, progress: Progress) -> None:
    """Generate the ARG blocks for the two stages."""
    state.update(
        {
            "docker_blocks": {
                "build": [
                    {
                        "block": "\n".join(
                            f'ARG {arg["name"]}="{arg["value"]}"' if arg["value"] is not None else f"ARG {arg['name']}"
                            for arg in state["docker_args"]
                        ),
                        "weight": 21,
                    }
                ],
                "deploy": [
                    {
                        "block": "\n".join(
                            f'ARG {arg["name"]}="{arg["value"]}"' if arg["value"] is not None else f"ARG {arg['name']}"
                            for arg in state["docker_args"]
                        ),
                        "weight": 21,
                    }
                ],
            }
        }
    )
