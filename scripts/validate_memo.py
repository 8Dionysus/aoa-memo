#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "generated" / "memo_registry.min.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "memo-registry.schema.json"

ALLOWED_KIND = {"episodic_memory", "semantic_memory", "provenance_thread", "recall_surface"}
ALLOWED_STATUS = {"active", "planned", "experimental", "deprecated"}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(REPO_ROOT).as_posix()}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(REPO_ROOT).as_posix()}: {exc}")


def validate_schema_surface() -> None:
    schema = read_json(SCHEMA_PATH)
    if not isinstance(schema, dict):
        fail("schema file must contain a JSON object")
    required_top_level = {"$schema", "$id", "title", "type", "properties", "required"}
    missing = sorted(required_top_level - set(schema))
    if missing:
        fail(f"schema is missing required top-level keys: {', '.join(missing)}")


def validate_registry() -> None:
    payload = read_json(REGISTRY_PATH)
    if not isinstance(payload, dict):
        fail("memo registry must be a JSON object")

    for key in ("version", "layer", "objects"):
        if key not in payload:
            fail(f"memo registry is missing required key '{key}'")

    if not isinstance(payload["version"], int) or payload["version"] < 1:
        fail("registry 'version' must be an integer >= 1")
    if payload["layer"] != "aoa-memo":
        fail("registry 'layer' must equal 'aoa-memo'")

    objects = payload["objects"]
    if not isinstance(objects, list) or not objects:
        fail("registry 'objects' must be a non-empty list")

    seen_ids: set[str] = set()
    for index, obj in enumerate(objects):
        location = f"objects[{index}]"
        if not isinstance(obj, dict):
            fail(f"{location} must be an object")

        for key in ("id", "kind", "status", "summary"):
            if key not in obj:
                fail(f"{location} is missing required key '{key}'")

        memory_id = obj["id"]
        kind = obj["kind"]
        status = obj["status"]
        summary = obj["summary"]

        if not isinstance(memory_id, str) or len(memory_id) < 3:
            fail(f"{location}.id must be a string of length >= 3")
        if memory_id in seen_ids:
            fail(f"duplicate memory object id in registry: '{memory_id}'")
        seen_ids.add(memory_id)

        if kind not in ALLOWED_KIND:
            fail(f"{location}.kind '{kind}' is not allowed")
        if status not in ALLOWED_STATUS:
            fail(f"{location}.status '{status}' is not allowed")
        if not isinstance(summary, str) or len(summary) < 10:
            fail(f"{location}.summary must be a string of length >= 10")


def main() -> int:
    try:
        validate_schema_surface()
        validate_registry()
    except ValidationError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[ok] validated memo registry schema surface")
    print("[ok] validated generated/memo_registry.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
