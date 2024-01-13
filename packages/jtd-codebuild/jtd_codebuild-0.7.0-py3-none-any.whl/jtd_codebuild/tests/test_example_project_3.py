import os
import subprocess

# Get current working directory
cwd = os.path.dirname(__file__)


def _root_path(file_path: str) -> str:
    return os.path.join(cwd, "fixtures/example_project_3", file_path)


def test_example_project_3():
    # Run the command
    subprocess.check_call(
        "jtd-codebuild fixtures/example_project_3",
        shell=True,
        cwd=cwd,
    )

    # Check the output

    # Intermediate schema file
    assert os.path.exists(_root_path("gen/schema.jtd.json"))

    # More tests ...
