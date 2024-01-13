import itertools
from os.path import join
from typing import Dict, AnyStr, Any
from .loaders import load_definitions, load_root_schema
from .config import get_config
from .utils import get_items


def bundle_schema(cwd: str) -> Dict[AnyStr, Any]:
    """Bundles modularized schema files into a single schema file.

    This function will load all the schema files specified in the
    configuration file and packages specified as includes.

    Args:
        cwd: The current working directory.

    Returns:
        The bundled schema.
    """
    # Get configuration of the package
    config = get_config(cwd)

    # Extract schemas from includes
    schemas = [
        bundle_schema(join(cwd, include)) for include in config.get("includes", [])
    ]

    # Extract definitions from includes schemas
    definitions = [schema["definitions"] for schema in schemas]

    # Load definitions and append it to the list
    definitions.append(load_definitions(cwd))

    # Load root schema
    root_schema = load_root_schema(cwd)

    # Add definitions to root schema
    if "definitions" not in root_schema:
        root_schema["definitions"] = {}
    allow_duplicate_defs = config.get("allow-duplicate-defs", False)
    for defname, definition in itertools.chain(*map(get_items, definitions)):
        if defname in root_schema["definitions"] and not allow_duplicate_defs:
            raise ValueError(f"Duplicate definition: {defname}")
        root_schema["definitions"][defname] = definition

    return root_schema
