from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from post_release_boundary_datetime import *  # noqa: F401,F403


ROOT = Path(__file__).resolve().parents[5]
ESCAPE_VALUE = "__post_release_boundary_not_allowed__"

POST_RELEASE_BOUNDARY_CONTRACTS = (
    ('first_office_retention_marker_v1', 'first_office_retention_marker_v1.json'),
    ('installation_memory_entry_v1', 'installation_memory_entry_v1.json'),
    ('office_retention_marker_v1', 'office_retention_marker_v1.json'),
    ('release_revision_ledger_entry_v1', 'release_revision_ledger_entry_v1.json'),
    ('rollback_memory_entry_v1', 'rollback_memory_entry_v1.json'),
    ('service_incident_memory_entry_v1', 'service_incident_memory_entry_v1.json'),
    ('service_revision_ledger_entry_v1', 'service_revision_ledger_entry_v1.json'),
    ('train_release_memory_entry_v1', 'train_release_memory_entry_v1.json'),
)
CONTRACT_BASE_BY_STEM = {
    "first_office_retention_marker_v1": "mechanics/retention/parts/office-markers",
    "installation_memory_entry_v1": "mechanics/governance/parts/install-and-certification-boundary",
    "office_retention_marker_v1": "mechanics/retention/parts/office-markers",
    "release_revision_ledger_entry_v1": "mechanics/writeback/parts/revision-ledgers",
    "rollback_memory_entry_v1": "mechanics/writeback/parts/rollback-and-recovery",
    "service_incident_memory_entry_v1": "mechanics/operational-gate/parts/office-incident-gate",
    "service_revision_ledger_entry_v1": "mechanics/operational-gate/parts/service-revision-ledger",
    "train_release_memory_entry_v1": "mechanics/operational-gate/parts/post-release-boundaries",
}


def contract_paths(stem: str, schema_file: str) -> tuple[Path, Path]:
    base = ROOT / CONTRACT_BASE_BY_STEM[stem]
    return base / "schemas" / schema_file, base / "examples" / f"{stem}.example.json"


def load_contract(stem: str, schema_file: str) -> tuple[dict[str, object], dict[str, object]]:
    schema_path, example_path = contract_paths(stem, schema_file)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))
    return schema, example


def validation_errors(schema: dict[str, object], value: object) -> list[object]:
    return sorted(
        Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(value),
        key=lambda error: list(error.path),
    )


def effective_schema(schema: object, value: object) -> object:
    if not isinstance(schema, dict):
        return schema
    variants = schema.get("oneOf")
    if isinstance(variants, list):
        for variant in variants:
            if isinstance(variant, dict) and not validation_errors(variant, value):
                return variant
    return schema


def schema_properties(schema: object, value: object | None = None) -> dict[str, object]:
    if value is not None:
        schema = effective_schema(schema, value)
    if not isinstance(schema, dict):
        return {}
    props = schema.get("properties")
    return props if isinstance(props, dict) else {}


def child_schema(schema: object, value: object, key: object) -> object:
    schema = effective_schema(schema, value)
    if isinstance(key, str) and isinstance(value, dict):
        return schema_properties(schema, value).get(key, {})
    if isinstance(key, int) and isinstance(value, list) and isinstance(schema, dict):
        return effective_schema(schema.get("items", {}), value[key])
    return {}


def wrong_type_value(value: object) -> object:
    if isinstance(value, bool):
        return "not-a-boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "not-an-integer"
    if isinstance(value, float):
        return "not-a-number"
    if isinstance(value, str):
        return 12345
    if isinstance(value, list):
        return {"not": "an array"}
    if isinstance(value, dict):
        return "not-an-object"
    return "not-null"


def escape_value(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int) and not isinstance(value, bool):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return f"{value}{ESCAPE_VALUE}"
    return ESCAPE_VALUE


def get_path(value: object, path: tuple[object, ...]) -> object:
    cursor = value
    for part in path:
        if isinstance(part, int):
            assert isinstance(cursor, list)
            cursor = cursor[part]
        else:
            assert isinstance(cursor, dict)
            cursor = cursor[part]
    return cursor


def set_path(value: object, path: tuple[object, ...], replacement: object) -> None:
    cursor = value
    for part in path[:-1]:
        if isinstance(part, int):
            assert isinstance(cursor, list)
            cursor = cursor[part]
        else:
            assert isinstance(cursor, dict)
            cursor = cursor[part]
    last = path[-1]
    if isinstance(last, int):
        assert isinstance(cursor, list)
        cursor[last] = replacement
    else:
        assert isinstance(cursor, dict)
        cursor[last] = replacement


def delete_path(value: object, path: tuple[object, ...]) -> None:
    cursor = value
    for part in path[:-1]:
        if isinstance(part, int):
            assert isinstance(cursor, list)
            cursor = cursor[part]
        else:
            assert isinstance(cursor, dict)
            cursor = cursor[part]
    last = path[-1]
    if isinstance(last, int):
        assert isinstance(cursor, list)
        del cursor[last]
    else:
        assert isinstance(cursor, dict)
        del cursor[last]


def walk_values(value: object, path: tuple[object, ...] = ()) -> list[tuple[tuple[object, ...], object]]:
    found: list[tuple[tuple[object, ...], object]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = (*path, key)
            found.append((child_path, child))
            found.extend(walk_values(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = (*path, index)
            found.append((child_path, child))
            found.extend(walk_values(child, child_path))
    return found


def object_paths(value: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    found: list[tuple[object, ...]] = []
    if isinstance(value, dict):
        found.append(path)
        for key, child in value.items():
            found.extend(object_paths(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(object_paths(child, (*path, index)))
    return found


def array_paths(value: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    found: list[tuple[object, ...]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found.extend(array_paths(child, (*path, key)))
    elif isinstance(value, list):
        found.append(path)
        for index, child in enumerate(value):
            found.extend(array_paths(child, (*path, index)))
    return found


def string_paths(value: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    found: list[tuple[object, ...]] = []
    if isinstance(value, str):
        found.append(path)
    elif isinstance(value, dict):
        for key, child in value.items():
            found.extend(string_paths(child, (*path, key)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(string_paths(child, (*path, index)))
    return found


def schema_for_path(schema: object, example: object, path: tuple[object, ...]) -> object:
    cursor_schema = schema
    cursor_value = example
    for part in path:
        cursor_schema = child_schema(cursor_schema, cursor_value, part)
        if isinstance(part, int):
            assert isinstance(cursor_value, list)
            cursor_value = cursor_value[part]
        else:
            assert isinstance(cursor_value, dict)
            cursor_value = cursor_value[part]
    return effective_schema(cursor_schema, cursor_value)


def required_paths(schema: object, example: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    schema = effective_schema(schema, example)
    found: list[tuple[object, ...]] = []
    if isinstance(schema, dict) and schema.get("type") == "object" and isinstance(example, dict):
        required = schema.get("required")
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key in example:
                    found.append((*path, key))
        for key, prop in schema_properties(schema, example).items():
            if key in example:
                found.extend(required_paths(prop, example[key], (*path, key)))
    if isinstance(schema, dict) and schema.get("type") == "array" and isinstance(example, list) and example:
        found.extend(required_paths(schema.get("items"), example[0], (*path, 0)))
    return found


def constrained_paths(schema: object, example: object, keyword: str, path: tuple[object, ...] = ()) -> list[tuple[tuple[object, ...], object]]:
    schema = effective_schema(schema, example)
    found: list[tuple[tuple[object, ...], object]] = []
    if not isinstance(schema, dict):
        return found
    if keyword in schema:
        found.append((path, schema[keyword]))
    if schema.get("type") == "object" and isinstance(example, dict):
        for key, prop in schema_properties(schema, example).items():
            if key in example:
                found.extend(constrained_paths(prop, example[key], keyword, (*path, key)))
    if schema.get("type") == "array" and isinstance(example, list) and example:
        found.extend(constrained_paths(schema.get("items"), example[0], keyword, (*path, 0)))
    return found
