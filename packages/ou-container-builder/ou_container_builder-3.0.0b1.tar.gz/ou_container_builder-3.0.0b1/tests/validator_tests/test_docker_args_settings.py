"""Test the docker args settings validation."""
from ou_container_builder.settings import DockerArg


def test_valid_docker_args_settings():
    """Test that a valid docker args configuration passes."""
    DockerArg(name="TARGETPLATFORM")
    DockerArg(name="TARGETPLATFORM", value="linux/amd64")
