from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[5]
ENUM_ESCAPE_VALUE = "__governance_boundary_not_allowed__"

GOVERNANCE_BOUNDARY_CONTRACTS = (
    ('governance_memory_writeback', 'governance_memory_writeback_v1.json'),
    ('governance_retention_check', 'governance_retention_check_v1.json'),
    ('policy_precedent_memory', 'policy_precedent_memory_v1.json'),
    ('revocation_ledger_entry', 'revocation_ledger_entry_v1.json'),
    ('governance_decision_memory_v1', 'governance_decision_memory_v1.json'),
)
CONTRACT_BASE_BY_STEM = {
    "governance_memory_writeback": "mechanics/governance/parts/governance-boundary",
    "governance_retention_check": "mechanics/retention/parts/cross-repo-and-governance-retention",
    "policy_precedent_memory": "mechanics/governance/parts/precedent-and-stay-order",
    "revocation_ledger_entry": "mechanics/writeback/parts/revision-ledgers",
    "governance_decision_memory_v1": "mechanics/governance/parts/governance-boundary",
}


def contract_paths(stem: str, schema_file: str) -> tuple[Path, Path]:
    base = ROOT / CONTRACT_BASE_BY_STEM[stem]
    return base / "schemas" / schema_file, base / "examples" / f"{stem}.example.json"

def load_contract(stem: str, schema_file: str) -> tuple[dict[str, object], dict[str, object]]:
    schema_path, example_path = contract_paths(stem, schema_file)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))
    return schema, example


def validation_errors(schema: dict[str, object], value: dict[str, object]) -> list[object]:
    return sorted(Draft202012Validator(schema).iter_errors(value), key=lambda error: list(error.path))


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


def const_escape_value(value: object) -> object:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int) and not isinstance(value, bool):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return f"{value}{ENUM_ESCAPE_VALUE}"
    return ENUM_ESCAPE_VALUE


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


def schema_type(schema: object) -> object:
    return schema.get("type") if isinstance(schema, dict) else None


def schema_properties(schema: object) -> dict[str, object]:
    if not isinstance(schema, dict):
        return {}
    props = schema.get("properties")
    return props if isinstance(props, dict) else {}


def required_paths(schema: object, example: object, path: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    found: list[tuple[object, ...]] = []
    if not isinstance(schema, dict):
        return found
    if schema_type(schema) == "object" and isinstance(example, dict):
        required = schema.get("required")
        properties = schema_properties(schema)
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key in example:
                    found.append((*path, key))
        for key, prop in properties.items():
            if key in example:
                found.extend(required_paths(prop, example[key], (*path, key)))
    if schema_type(schema) == "array" and isinstance(example, list) and example:
        found.extend(required_paths(schema.get("items"), example[0], (*path, 0)))
    return found


def constrained_paths(schema: object, example: object, keyword: str, path: tuple[object, ...] = ()) -> list[tuple[tuple[object, ...], object]]:
    found: list[tuple[tuple[object, ...], object]] = []
    if not isinstance(schema, dict):
        return found
    if keyword in schema:
        found.append((path, schema[keyword]))
    if schema_type(schema) == "object" and isinstance(example, dict):
        for key, prop in schema_properties(schema).items():
            if key in example:
                found.extend(constrained_paths(prop, example[key], keyword, (*path, key)))
    if schema_type(schema) == "array" and isinstance(example, list) and example:
        found.extend(constrained_paths(schema.get("items"), example[0], keyword, (*path, 0)))
    return found
