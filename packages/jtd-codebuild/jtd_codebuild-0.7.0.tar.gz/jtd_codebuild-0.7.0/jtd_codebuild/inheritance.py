from functools import reduce
from typing import Dict, AnyStr, Any
from .utils import deep_merge


def _resolve_inheritance_recursively(
    schema: Dict[AnyStr, Any],
    defname: AnyStr,
    definition: Dict[AnyStr, Any],
) -> Dict[AnyStr, Any]:
    """Resolve inheritance recursively.

    Args:
        schema: The schema to resolve inheritance for.
        defname: The name of the definition to resolve inheritance for.
        definition: The definition to resolve inheritance for.

    Returns:
        The definition with inheritance resolved.
    """
    if "extends" not in definition:
        return definition

    # We reverse the order of the inherited defnames
    # as we want to follow python like module resolution order
    inherited_defnames = reversed(
        definition["extends"]
        if isinstance(definition["extends"], list)
        else [definition["extends"]]
    )

    # Resolve inheritance for each inherited definition
    inherited_definitions = [
        _resolve_inheritance_recursively(
            schema,
            inherited_defname,
            schema["definitions"][inherited_defname],
        )
        for inherited_defname in inherited_defnames
    ]

    # Merge the inherited definitions into the definition
    merged_definition = reduce(deep_merge, inherited_definitions, definition)

    # Update the definition in the schema
    schema["definitions"][defname] = merged_definition

    # Delete extends key from the definition
    schema["definitions"][defname].pop("extends", None)

    # Return the merged definition
    return merged_definition


def resolve_inheritance(schema: Dict[AnyStr, Any]) -> Dict[AnyStr, Any]:
    """Resolve inheritance in the schema.

    Args:
        schema: The schema to resolve inheritance for.

    Returns:
        The schema with inheritance resolved.
    """
    for defname, definition in schema["definitions"].items():
        if "extends" in definition:
            _resolve_inheritance_recursively(schema, defname, definition)

    return schema
