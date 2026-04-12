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
