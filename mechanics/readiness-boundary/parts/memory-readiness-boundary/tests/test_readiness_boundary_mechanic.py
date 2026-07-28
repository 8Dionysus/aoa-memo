from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
DOC_PATH = REPO_ROOT / "mechanics" / "readiness-boundary" / "docs" / "MEMORY_READINESS_BOUNDARY.md"
SCHEMA_PATH = (
    REPO_ROOT
    / "mechanics"
    / "readiness-boundary"
    / "parts"
    / "memory-readiness-boundary"
    / "schemas"
    / "memory_readiness_boundary_contract.schema.json"
)
EXAMPLE_PATH = (
    REPO_ROOT
    / "mechanics"
    / "readiness-boundary"
    / "parts"
    / "memory-readiness-boundary"
    / "examples"
    / "memory_readiness_boundary_contract.example.json"
)


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
    assert "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md" in example["writeback_boundary"]["export_surfaces"]


def test_memory_readiness_boundary_routes_to_existing_objects_and_stronger_owners() -> None:
    doc = DOC_PATH.read_text(encoding="utf-8")

    for phrase in (
        "memory is not proof",
        "durable reviewed consequence",
        "memory delta",
        "canon delta reference",
        "retention check",
        "unresolved contradiction",
        "survivor or bridge candidate",
        "civil/service assistant trace",
        "aoa-evals",
        "aoa-kag",
        "aoa-sdk",
        "abyss-stack",
    ):
        assert phrase in doc


def test_registry_routes_readiness_boundary_docs_and_schema() -> None:
    registry = load_json(REPO_ROOT / "generated" / "memory" / "memo_registry.min.json")
    assert isinstance(registry, dict)
    assert "mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md" in registry["core_docs"]
    assert (
        "mechanics/readiness-boundary/parts/memory-readiness-boundary/schemas/memory_readiness_boundary_contract.schema.json"
        in registry["schemas"]
    )
