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


def test_playbook_memory_scopes_doc_keeps_bounded_scope_rule() -> None:
    doc = (REPO_ROOT / "docs" / "PLAYBOOK_MEMORY_SCOPES.md").read_text(encoding="utf-8")
    doc_compact = " ".join(doc.split())

    for fragment in [
        "Playbooks should ask memo for bounded recall modes and explicit scopes.",
        "They should not assume a blank check to the whole memory layer.",
        "Return-oriented relaunch should prefer working recall plus explicit checkpoint continuity over widening the whole memo scope.",
        "When a playbook requests return, it should ask for checkpoint anchors and exported state surfaces, not a new memory family.",
    ]:
        assert fragment in doc_compact


def test_playbook_memory_scope_surfaces_keep_return_ready_chain() -> None:
    working = load_json("examples/recall_contract.working.json")
    return_ready = load_json("examples/recall_contract.object.working.return.json")
    inquiry_return = load_json("examples/inquiry_checkpoint.return.example.json")

    assert working["allowed_scopes"] == ["thread", "session", "project"]
    assert working["preferred_kinds"] == ["state_capsule", "decision", "episode", "audit_event"]
    assert return_ready["checkpoint_continuity_supported"] is True
    assert return_ready["return_ready"] is True
    assert inquiry_return["return_pack"]["reentry_refs"] == [
        "examples/recall_contract.object.working.return.json",
        "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
    ]


def test_playbook_memory_scopes_surface_stays_discoverable() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    registry = load_json("generated/memo_registry.min.json")

    assert "docs/PLAYBOOK_MEMORY_SCOPES.md" in readme
    assert "docs/PLAYBOOK_MEMORY_SCOPES.md" in registry["core_docs"]

