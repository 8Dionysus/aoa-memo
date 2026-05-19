from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_recovery_pattern_adjunct_example_validates_against_schema() -> None:
    schema = load_json("mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json")
    example = load_json("mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.example.json")

    Draft202012Validator(schema).validate(example)


def test_recovery_pattern_lineage_example_validates_against_schema() -> None:
    schema = load_json("mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json")
    example = load_json("mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.lineage.example.json")

    Draft202012Validator(schema).validate(example)


def test_recovery_pattern_rollout_example_validates_against_schema() -> None:
    schema = load_json("mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json")
    example = load_json("mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.rollout.example.json")

    Draft202012Validator(schema).validate(example)


def test_recovery_pattern_rollback_followthrough_example_validates_against_schema() -> None:
    schema = load_json("mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json")
    example = load_json("mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.rollback_followthrough.example.json")

    Draft202012Validator(schema).validate(example)


def test_recovery_pattern_component_refresh_example_validates_against_schema() -> None:
    schema = load_json("mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json")
    example = load_json("mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.component_refresh.example.json")

    Draft202012Validator(schema).validate(example)


def test_component_refresh_recovery_pattern_stays_draft_and_owner_bounded() -> None:
    example = load_json("mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.component_refresh.example.json")

    assert example["review_status"] == "draft"
    assert example["trust_posture"]["status"] == "provisional"
    assert "aoa-playbooks:playbook_registry_v1#AOA-P-0030" in example["route_hint_refs"]
    assert "aoa-stats:generated/component_refresh_summary.min.json" in example["stats_summary_refs"]
    assert "reviewed followthrough decision" in example["recall_posture"]
    assert "scheduler authority" in example["notes"]


def test_native_recovery_pattern_integrates_into_object_family() -> None:
    pattern_example = load_json("mechanics/antifragility/parts/recovery-pattern-memory/examples/pattern.antifragility-stress-recovery-window.example.json")
    validator = validate_memo.validator_for("pattern.schema.json")
    validator.validate(pattern_example)

    expected_id = "memo.pattern.2026-04-07.antifragility-stress-recovery-window"
    expected_source_path = "mechanics/antifragility/parts/recovery-pattern-memory/examples/pattern.antifragility-stress-recovery-window.example.json"

    full_catalog = load_json("generated/memory_object_catalog.json")
    min_catalog = load_json("generated/memory_object_catalog.min.json")
    capsules = load_json("generated/memory_object_capsules.json")
    sections = load_json("generated/memory_object_sections.full.json")

    assert any(
        item["id"] == expected_id and item["source_path"] == expected_source_path
        for item in full_catalog["memory_objects"]
    )
    assert any(
        item["id"] == expected_id
        and item["source_path"] == expected_source_path
        and item["current_recall_status"] == "allowed"
        for item in min_catalog["memory_objects"]
    )
    assert any(
        item["id"] == expected_id and item["source_path"] == expected_source_path
        for item in capsules["memory_objects"]
    )
    assert any(
        item["id"] == expected_id and item["source_path"] == expected_source_path
        for item in sections["memory_objects"]
    )


def test_recovery_pattern_surfaces_stay_discoverable_and_non_proof() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    package_parts = (
        REPO_ROOT / "mechanics" / "antifragility" / "PARTS.md"
    ).read_text(encoding="utf-8")
    docs_index = (
        REPO_ROOT / "mechanics" / "antifragility" / "docs" / "README.md"
    ).read_text(encoding="utf-8")
    part_readme = (
        REPO_ROOT / "mechanics" / "antifragility" / "parts" / "recovery-pattern-memory" / "README.md"
    ).read_text(encoding="utf-8")
    part_contract = (
        REPO_ROOT / "mechanics" / "antifragility" / "parts" / "recovery-pattern-memory" / "CONTRACT.md"
    ).read_text(encoding="utf-8")
    memory_doc = (
        REPO_ROOT / "mechanics" / "antifragility" / "docs" / "RECOVERY_PATTERN_MEMORY.md"
    ).read_text(encoding="utf-8")
    recall_doc = (
        REPO_ROOT / "mechanics" / "antifragility" / "docs" / "RECOVERY_PATTERN_RECALL.md"
    ).read_text(encoding="utf-8")

    for fragment in [
        "mechanics/antifragility/docs/RECOVERY_PATTERN_MEMORY.md",
        "mechanics/antifragility/docs/RECOVERY_PATTERN_RECALL.md",
        "mechanics/antifragility/docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md",
        "mechanics/writeback/docs/GROWTH_REFINERY_WRITEBACK.md",
        "mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json",
        "mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.example.json",
        "mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.lineage.example.json",
        "mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.rollout.example.json",
        "mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.rollback_followthrough.example.json",
        "mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.component_refresh.example.json",
        "mechanics/antifragility/parts/recovery-pattern-memory/examples/pattern.antifragility-stress-recovery-window.example.json",
    ]:
        assert (REPO_ROOT / fragment).exists()

    assert "[antifragility](mechanics/antifragility/README.md)" in readme
    local_route_text = "\n".join([package_parts, docs_index, part_readme, part_contract, memory_doc])
    for fragment in [
        "RECOVERY_PATTERN_MEMORY",
        "RECOVERY_PATTERN_RECALL",
        "ROLLBACK_FOLLOWTHROUGH_PATTERN",
        "recovery_pattern_memory_v1.json",
        "recovery_pattern_memory.example.json",
        "recovery_pattern_memory.lineage.example.json",
        "recovery_pattern_memory.rollout.example.json",
        "recovery_pattern_memory.rollback_followthrough.example.json",
        "recovery_pattern_memory.component_refresh.example.json",
        "pattern.antifragility-stress-recovery-window.example.json",
    ]:
        assert fragment in local_route_text

    assert "It remains memory, not proof." in memory_doc
    assert "mechanics/antifragility/docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md" in memory_doc
    assert "component_refresh.example.json" in memory_doc
    assert "lineage_refs" in memory_doc
    assert "Memo may shape recall and routing review." in recall_doc
    assert "It does not overrule source-owned receipts, eval proof, or derived stats" in recall_doc
