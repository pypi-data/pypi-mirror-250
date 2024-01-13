import os
import json
import yaml
import itertools
from os.path import join
from typing import Dict, AnyStr, Any
from .config import get_config
from .utils import file_is_yaml, file_is_json


def load_definitions(cwd: str) -> Dict[AnyStr, Any]:
    """Load definition files from its directory given by the configuration file.

    Args:
        cwd: The current working directory.

    Returns:
        A dictionary of all definitions.
        Key is the definition name, value is the definition.
    """
    config = get_config(cwd)
    definition_paths = (
        config.get("definitions-path", None)
        or config.get("definitions-paths", None)
        or []
    )
    definition_paths = (
        definition_paths if isinstance(definition_paths, list) else [definition_paths]
    )
    definition_paths = map(lambda path: join(cwd, path), definition_paths)

    definitions = {}

    # Recursively load all definitions
    for root, dirs, files in itertools.chain(*map(os.walk, definition_paths)):
        for file in files:
            if file_is_yaml(file) or file_is_json(file):
                filepath = join(root, file)
                with open(filepath, "r") as f:
                    definition_parts = (
                        yaml.load(f, Loader=yaml.FullLoader)
                        if file_is_yaml(file)
                        else json.load(f)
                    )
                    for definition_name, definition in definition_parts.items():
                        if definition_name in definitions:
                            raise ValueError(
                                f"Definition name {definition_name} already exists."
                            )
                        definitions[definition_name] = definition

    return definitions


def load_root_schema(cwd: str) -> Dict[AnyStr, Any]:
    """Load the root schema from the schema file given by the configuration file.

    Args:
        cwd: The current working directory.

    Returns:
        The root schema.
    """
    config = get_config(cwd)
    schema_path = os.path.join(cwd, config["root-schema-path"])

    with open(schema_path, "r") as f:
        return (
            yaml.load(f, Loader=yaml.FullLoader)
            if file_is_yaml(schema_path)
            else json.load(f)
        )
