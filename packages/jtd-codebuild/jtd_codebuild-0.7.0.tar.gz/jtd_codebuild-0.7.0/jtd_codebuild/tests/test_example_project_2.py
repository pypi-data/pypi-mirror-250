import os
import subprocess

# Get current working directory
cwd = os.path.dirname(__file__)


def _root_path(file_path: str) -> str:
    return os.path.join(cwd, "fixtures/example_project_2", file_path)


def test_example_project_2():
    # Run the command
    subprocess.check_call(
        "jtd-codebuild fixtures/example_project_2",
        shell=True,
        cwd=cwd,
    )

    # Check the output

    # Intermediate schema file
    assert os.path.exists(_root_path("gen/schema.jtd.json"))

    # Python code
    assert os.path.exists(_root_path("gen/python/__init__.py"))
    assert os.path.exists(_root_path("gen/python_pydantic/__init__.py"))
    assert os.path.exists(_root_path("gen/python_typeddict/__init__.py"))

    # TypeScript code
    assert os.path.exists(_root_path("gen/typescript/index.ts"))

    # More tests ...
