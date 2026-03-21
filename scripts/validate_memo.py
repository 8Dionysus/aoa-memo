#!/usr/bin/env python3
"""Validate bootstrap aoa-memo artifacts.

This script is intentionally small and honest. It validates the current example
objects against the local JSON schemas and performs a light structural check on
`generated/memo_registry.min.json`.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema")
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS / schema_name)
    return Draft202012Validator(schema)


def validate_example(validator: Draft202012Validator, example_name: str) -> None:
    data = load_json(EXAMPLES / example_name)
    errors = sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    if errors:
        print(f"[FAIL] {example_name}")
        for err in errors:
            path = ".".join(str(part) for part in err.absolute_path) or "<root>"
            print(f"  - {path}: {err.message}")
        raise SystemExit(1)
    print(f"[OK]   {example_name}")


def validate_registry() -> None:
    data = load_json(GENERATED / "memo_registry.min.json")
    required = [
        "layer",
        "version",
        "status",
        "memory_object_kinds",
        "supporting_objects",
        "recall_modes",
        "temperature_scale",
        "core_docs",
        "schemas",
    ]
    missing = [key for key in required if key not in data]
    if missing:
        print("[FAIL] generated/memo_registry.min.json")
        for key in missing:
            print(f"  - missing key: {key}")
        raise SystemExit(1)
    print("[OK]   generated/memo_registry.min.json")


def main() -> int:
    validate_example(validator_for("memory_object.schema.json"), "episode.example.json")
    validate_example(validator_for("memory_object.schema.json"), "claim.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "provenance_thread.example.json")
    validate_example(validator_for("recall_contract.schema.json"), "recall_contract.semantic.json")
    validate_registry()
    print("\nValidation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
