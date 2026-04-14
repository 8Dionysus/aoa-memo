from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_a2a_child_return_provenance_thread_validates() -> None:
    validator = validate_memo.validator_for("provenance_thread.schema.json")
    example = load_json(
        "examples/provenance_thread.a2a-summon-return-checkpoint.example.json"
    )

    validator.validate(example)


def test_a2a_child_return_writeback_stays_candidate_only() -> None:
    doc = (REPO_ROOT / "docs" / "A2A_CHILD_RETURN_WRITEBACK.md").read_text(
        encoding="utf-8"
    )
    seam = (REPO_ROOT / "docs" / "RUNTIME_WRITEBACK_SEAM.md").read_text(
        encoding="utf-8"
    )
    example = load_json(
        "examples/provenance_thread.a2a-summon-return-checkpoint.example.json"
    )

    assert "repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json" in doc
    assert "A2A-specific memory" in seam
    assert example["writeback_target"] == "provenance_thread"
    assert example["anchor_artifact_ref"].endswith("#reviewed_closeout_request")
    assert "repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json" in example[
        "source_refs"
    ]
    assert "canon" in example["summary"]
