from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_failure_lesson_example_validates_against_schema() -> None:
    validator = validate_memo.validator_for("failure_lesson_memory_v1.json")
    example = load_json("examples/failure_lesson_memory.example.json")

    validator.validate(example)


def test_failure_lesson_example_rejects_invalid_expiry_format() -> None:
    validator = validate_memo.validator_for("failure_lesson_memory_v1.json")
    example = load_json("examples/failure_lesson_memory.example.json")
    assert isinstance(example, dict)
    example["expires_at_utc"] = "not-a-date-time"

    errors = [error.message for error in validator.iter_errors(example)]

    assert errors
    assert any("valid under any of the given schemas" in message for message in errors)


def test_failure_lesson_lineage_example_validates_against_schema() -> None:
    validator = validate_memo.validator_for("failure_lesson_memory_v1.json")
    example = load_json("examples/failure_lesson_memory.lineage.example.json")

    validator.validate(example)


def test_failure_lesson_lineage_ref_validation_handles_malformed_objects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    example = load_json("examples/failure_lesson_memory.lineage.example.json")
    assert isinstance(example, dict)
    example["lineage_refs"] = "not-an-object"
    example["lineage_context"] = "not-an-object"
    (tmp_path / "failure_lesson_memory.lineage.example.json").write_text(
        json.dumps(example, indent=2) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_memo, "EXAMPLES", tmp_path)

    with pytest.raises(SystemExit):
        validate_memo.validate_example(
            validate_memo.validator_for("failure_lesson_memory_v1.json"),
            "failure_lesson_memory.lineage.example.json",
        )


def test_failure_lesson_surfaces_stay_discoverable_and_non_proof() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    memory_doc = (REPO_ROOT / "docs" / "FAILURE_LESSON_MEMORY.md").read_text(encoding="utf-8")
    recall_doc = (REPO_ROOT / "docs" / "FAILURE_LESSON_RECALL.md").read_text(encoding="utf-8")

    for fragment in [
        "docs/FAILURE_LESSON_MEMORY.md",
        "docs/FAILURE_LESSON_RECALL.md",
        "docs/GROWTH_REFINERY_WRITEBACK.md",
        "schemas/failure_lesson_memory_v1.json",
        "examples/failure_lesson_memory.example.json",
        "examples/failure_lesson_memory.lineage.example.json",
    ]:
        assert fragment in readme

    assert "It remains memory, not proof." in memory_doc
    assert "lineage_refs" in memory_doc
    assert "Memo may shape attention." in recall_doc
    assert "It does not overrule source-owned evidence." in recall_doc
