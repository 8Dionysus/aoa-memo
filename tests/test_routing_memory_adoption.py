from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_routing_memory_adoption_doc_keeps_inspect_capsule_expand_rule() -> None:
    doc = (REPO_ROOT / "docs" / "ROUTING_MEMORY_ADOPTION.md").read_text(encoding="utf-8")
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
        load_json("examples/recall_contract.router.semantic.json"),
        load_json("examples/recall_contract.router.lineage.json"),
    ]
    object_contracts = [
        load_json("examples/recall_contract.object.semantic.json"),
        load_json("examples/recall_contract.object.lineage.json"),
        load_json("examples/recall_contract.object.working.return.json"),
    ]

    for payload in router_contracts:
        assert payload["inspect_surface"] == "generated/memory_catalog.min.json"
        assert payload["capsule_surface"] == "generated/memory_capsules.json"
        assert payload["expand_surface"] == "generated/memory_sections.full.json"

    for payload in object_contracts:
        assert payload["inspect_surface"] == "generated/memory_object_catalog.min.json"
        assert payload["capsule_surface"] == "generated/memory_object_capsules.json"
        assert payload["expand_surface"] == "generated/memory_object_sections.full.json"


def test_routing_memory_adoption_surface_stays_discoverable() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    registry = load_json("generated/memo_registry.min.json")

    assert "docs/ROUTING_MEMORY_ADOPTION.md" in readme
    assert "docs/ROUTING_MEMORY_ADOPTION.md" in registry["core_docs"]
