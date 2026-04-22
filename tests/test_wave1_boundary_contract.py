from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "memory_readiness_boundary_contract.schema.json"
EXAMPLE_PATH = REPO_ROOT / "examples" / "memory_readiness_boundary_contract.example.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def test_memory_readiness_boundary_contract_example_validates() -> None:
    schema = load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)

    assert isinstance(schema, dict)
    assert isinstance(example, dict)

    validator = Draft202012Validator(schema)
    errors = [error.message for error in validator.iter_errors(example)]

    assert errors == []
    assert example["retention_boundary"]["owned_by"] == "abyss-stack"
    assert "docs/RUNTIME_WRITEBACK_SEAM.md" in example["writeback_boundary"]["export_surfaces"]
