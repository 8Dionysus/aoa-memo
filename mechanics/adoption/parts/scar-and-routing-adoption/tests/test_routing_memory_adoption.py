from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_ROOT = REPO_ROOT / "scripts" / "memory"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_scar_writeback_contract_is_part_local_and_validates() -> None:
    part_root = (
        REPO_ROOT
        / "mechanics"
        / "adoption"
        / "parts"
        / "scar-and-routing-adoption"
    )
    schema_path = part_root / "schemas" / "adoption_scar_writeback_v1.json"
    example_path = part_root / "examples" / "adoption_scar_writeback.example.json"
    parts = (REPO_ROOT / "mechanics" / "adoption" / "PARTS.md").read_text(
        encoding="utf-8"
    )

    assert schema_path.relative_to(REPO_ROOT).as_posix() in parts
    assert example_path.relative_to(REPO_ROOT).as_posix() in parts

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = json.loads(example_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(example),
        key=lambda error: list(error.path),
    )
    assert errors == []


def test_routing_memory_adoption_doc_keeps_inspect_capsule_expand_rule() -> None:
    doc = (
        REPO_ROOT / "mechanics" / "adoption" / "docs" / "ROUTING_MEMORY_ADOPTION.md"
    ).read_text(encoding="utf-8")
    doc_compact = " ".join(doc.split())

    for fragment in [
        "Inspect first.",
        "Hydrate through capsules second.",
        "Expand only when the capsule step is insufficient.",
        "The inspect id is the join key across all three steps.",
        "routing authority outside the memory layer",
    ]:
        assert fragment in doc_compact


def test_routing_memory_adoption_contracts_keep_additive_router_and_object_flows() -> None:
    router_contracts = [
        load_json("examples/recall/recall_contract.router.semantic.json"),
        load_json("examples/recall/recall_contract.router.lineage.json"),
    ]
    object_contracts = [
        load_json("examples/recall/recall_contract.object.semantic.json"),
        load_json("examples/recall/recall_contract.object.lineage.json"),
        load_json("examples/recall/recall_contract.object.working.return.json"),
    ]

    for payload in router_contracts:
        assert payload["inspect_surface"] == "generated/memory/memory_catalog.min.json"
        assert payload["capsule_surface"] == "generated/memory/memory_capsules.json"
        assert payload["expand_surface"] == "generated/memory/memory_sections.full.json"

    for payload in object_contracts:
        assert payload["inspect_surface"] == "generated/memory-objects/memory_object_catalog.min.json"
        assert payload["capsule_surface"] == "generated/memory-objects/memory_object_capsules.json"
        assert payload["expand_surface"] == "generated/memory-objects/memory_object_sections.full.json"


def test_routing_memory_adoption_surface_stays_discoverable() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    registry = load_json("generated/memory/memo_registry.min.json")

    assert "mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md" in readme
    assert "mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md" in registry["core_docs"]
