from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_recovery_pattern_adjunct_example_validates_against_schema() -> None:
    schema = load_json("schemas/recovery_pattern_memory_v1.json")
    example = load_json("examples/recovery_pattern_memory.example.json")

    Draft202012Validator(schema).validate(example)


def test_recovery_pattern_lineage_example_validates_against_schema() -> None:
    schema = load_json("schemas/recovery_pattern_memory_v1.json")
    example = load_json("examples/recovery_pattern_memory.lineage.example.json")

    Draft202012Validator(schema).validate(example)


def test_recovery_pattern_rollout_example_validates_against_schema() -> None:
    schema = load_json("schemas/recovery_pattern_memory_v1.json")
    example = load_json("examples/recovery_pattern_memory.rollout.example.json")

    Draft202012Validator(schema).validate(example)


def test_recovery_pattern_rollback_followthrough_example_validates_against_schema() -> None:
    schema = load_json("schemas/recovery_pattern_memory_v1.json")
    example = load_json("examples/recovery_pattern_memory.rollback_followthrough.example.json")

    Draft202012Validator(schema).validate(example)


def test_native_recovery_pattern_integrates_into_object_family() -> None:
    pattern_example = load_json("examples/pattern.antifragility-stress-recovery-window.example.json")
    validator = validate_memo.validator_for("pattern.schema.json")
    validator.validate(pattern_example)

    expected_id = "memo.pattern.2026-04-07.antifragility-stress-recovery-window"
    expected_source_path = "examples/pattern.antifragility-stress-recovery-window.example.json"

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
    memory_doc = (REPO_ROOT / "docs" / "RECOVERY_PATTERN_MEMORY.md").read_text(encoding="utf-8")
    recall_doc = (REPO_ROOT / "docs" / "RECOVERY_PATTERN_RECALL.md").read_text(encoding="utf-8")

    for fragment in [
        "docs/RECOVERY_PATTERN_MEMORY.md",
        "docs/RECOVERY_PATTERN_RECALL.md",
        "docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md",
        "docs/GROWTH_REFINERY_WRITEBACK.md",
        "schemas/recovery_pattern_memory_v1.json",
        "examples/recovery_pattern_memory.example.json",
        "examples/recovery_pattern_memory.lineage.example.json",
        "examples/recovery_pattern_memory.rollout.example.json",
        "examples/recovery_pattern_memory.rollback_followthrough.example.json",
        "examples/pattern.antifragility-stress-recovery-window.example.json",
    ]:
        assert fragment in readme

    assert "It remains memory, not proof." in memory_doc
    assert "docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md" in memory_doc
    assert "lineage_refs" in memory_doc
    assert "Memo may shape recall and routing review." in recall_doc
    assert "It does not overrule source-owned receipts, eval proof, or derived stats" in recall_doc
