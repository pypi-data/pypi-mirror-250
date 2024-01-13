import os
import subprocess


# Get current working directory
cwd = os.path.dirname(__file__)


def _root_path(file_path: str) -> str:
    return os.path.join(cwd, "fixtures/example_project_1", file_path)


def test_example_project_1():
    # Run the command
    subprocess.check_call(
        "jtd-codebuild fixtures/example_project_1",
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

    # Test python pydantic code with `Book` class
    from .fixtures.example_project_1.gen.python_pydantic import Book

    book = Book(
        id="1",
        name="Harry Potter",
        table_of_contents=["Chapter 1", "Chapter 2"],
    )
    assert book.id == "1"

    book.id = "2"
    assert book.id == "2"
    assert book["id"] == "2"

    book["id"] = "3"
    assert book.id == "3"
    assert book.get("id") == "3"

    # Test python typeddict code with `Book` class
    from .fixtures.example_project_1.gen.python_typeddict import Book

    book = Book(
        id="1",
        name="Harry Potter",
        tableOfContents=["Chapter 1", "Chapter 2"],
    )
    assert book["id"] == "1"
    assert book["name"] == "Harry Potter"
    assert book["tableOfContents"] == ["Chapter 1", "Chapter 2"]
