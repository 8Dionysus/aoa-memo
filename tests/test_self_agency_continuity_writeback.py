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


def memory_object_entries_by_id(relative_path: str) -> dict[str, dict]:
    payload = load_json(relative_path)
    assert isinstance(payload, dict)
    entries = payload["memory_objects"]
    assert isinstance(entries, list)
    return {
        entry["id"]: entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }


def test_self_agency_continuity_example_validates_against_provenance_thread_schema() -> None:
    validator = validate_memo.validator_for("provenance_thread.schema.json")
    example = load_json("examples/provenance_thread.self-agency-continuity.example.json")

    validator.validate(example)


def test_self_agency_continuity_doc_keeps_existing_memo_kind_boundary() -> None:
    doc = (REPO_ROOT / "docs" / "SELF_AGENCY_CONTINUITY_WRITEBACK.md").read_text(
        encoding="utf-8"
    )

    for fragment in [
        "Do not add a new memory object family for continuity or return.",
        "`anchor`",
        "`decision`",
        "`audit_event`",
        "`episode`",
        "`state_capsule`",
        "`provenance_thread`",
        "Memo can help a route return.",
        "Memo cannot decide whether return is legitimate.",
        "Memo cannot replace owner truth, playbook truth, or proof truth.",
    ]:
        assert fragment in doc


def test_self_agency_continuity_surfaces_stay_discoverable_and_non_sovereign() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    example = load_json("examples/provenance_thread.self-agency-continuity.example.json")

    assert "docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md" in readme
    assert "continuity_ref" in example
    assert example["writeback_target"] == "provenance_thread"
    assert example["anchor_artifact_ref"] == "artifact:verification_result:AOA-VERIFY-20260412-0001"
    assert "repo:aoa-playbooks/playbooks/self-agency-continuity-cycle/PLAYBOOK.md" in example[
        "source_refs"
    ]


def test_self_agency_continuity_memory_object_ids_hydrate_through_recall_surfaces() -> None:
    example = load_json("examples/provenance_thread.self-agency-continuity.example.json")
    assert isinstance(example, dict)
    expected_ids = {
        "memo.decision.2026-04-12.self-agency-reanchor-window",
        "memo.state.2026-04-12.self-agency-continuity-relay",
    }
    memory_object_ids = set(example["memory_object_ids"])

    assert expected_ids <= memory_object_ids

    catalog = memory_object_entries_by_id("generated/memory_object_catalog.min.json")
    capsules = memory_object_entries_by_id("generated/memory_object_capsules.json")
    sections = memory_object_entries_by_id("generated/memory_object_sections.full.json")

    for object_id in memory_object_ids:
        assert object_id in catalog
        assert object_id in capsules
        assert object_id in sections
        assert capsules[object_id]["kind"] == catalog[object_id]["kind"]
        assert capsules[object_id]["source_path"] == catalog[object_id]["source_path"]
        assert sections[object_id]["kind"] == catalog[object_id]["kind"]
        assert sections[object_id]["source_path"] == catalog[object_id]["source_path"]
        assert sections[object_id]["sections"]
