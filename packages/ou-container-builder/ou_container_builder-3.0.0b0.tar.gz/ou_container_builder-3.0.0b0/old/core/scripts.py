"""Pack to handle scripts."""
import os
from hashlib import sha256

from jinja2 import Environment

from ou_container_builder.utils import merge_settings


def process_settings(settings: dict) -> dict:
    """Process the env core settings.

    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :return: The updated settings
    :rtype: dict
    """
    if "startup" in settings["scripts"]:
        settings = merge_settings(settings, {"flags": {"ou_container_content": True}})
        new_settings = {}
        for script in settings["scripts"]["startup"]:
            if len(script["commands"]) > 1:
                hash = sha256("\n".join(script["commands"]).encode())
                script_name = f"startup-script-{hash.hexdigest()}"
                new_settings = merge_settings(
                    new_settings,
                    {
                        "content": [
                            {
                                "source": os.path.join("ou-builder-build", script_name),
                                "target": f"/usr/bin/{script_name}",
                                "overwrite": "always",
                            }
                        ],
                        "scripts": {"build": [{"commands": [f"chmod a+x /usr/bin/{script_name}"]}]},
                    },
                )
                script["commands"] = [f"/usr/bin/{script_name}"]
        settings = merge_settings(settings, new_settings)
    if "shutdown" in settings["scripts"]:
        settings = merge_settings(settings, {"flags": {"ou_container_content": True}})
        new_settings = {}
        for script in settings["scripts"]["shutdown"]:
            if len(script["commands"]) > 1:
                hash = sha256("\n".join(script["commands"]).encode())
                script_name = f"shutdown-script-{hash.hexdigest()}"
                new_settings = merge_settings(
                    new_settings,
                    {
                        "content": [
                            {
                                "source": os.path.join("ou-builder-build", script_name),
                                "target": f"/usr/bin/{script_name}",
                                "overwrite": "always",
                            }
                        ],
                        "scripts": {"build": [{"commands": [f"chmod a+x /usr/bin/{script_name}"]}]},
                    },
                )
                script["commands"] = [f"/usr/bin/{script_name}"]
        settings = merge_settings(settings, new_settings)

    return settings


def generate_files(context: str, env: Environment, settings: dict) -> dict:
    """Generate the build files for the scripts core.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The validated settings
    :type settings: dict
    """
    if "startup" in settings["scripts"]:
        for script in settings["scripts"]["startup"]:
            if len(script["commands"]) > 1:
                hash = sha256("\n".join(script["commands"]).encode())
                script_name = f"startup-script-{hash.hexdigest()}"
                with open(os.path.join(context, "ou-builder-build", script_name), "w") as out_f:
                    out_f.write("\n".join(script["commands"]))
    if "shutdown" in settings["scripts"]:
        for script in settings["scripts"]["shutdown"]:
            if len(script["commands"]) > 1:
                hash = sha256("\n".join(script["commands"]).encode())
                script_name = f"shutdown-script-{hash.hexdigest()}"
                with open(os.path.join(context, "ou-builder-build", script_name), "w") as out_f:
                    out_f.write("\n".join(script["commands"]))
