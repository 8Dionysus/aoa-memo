from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest


PART_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PART_ROOT / "scripts" / "agent_local_promotion.py"
SPEC = importlib.util.spec_from_file_location("agent_local_promotion", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def load(name: str) -> dict[str, object]:
    return json.loads((PART_ROOT / "examples" / name).read_text(encoding="utf-8"))


def test_candidate_and_admission_examples_are_valid() -> None:
    MODULE.validate_candidate(load("agent_local_shared_promotion_candidate_v0.example.json"))
    receipt = load("agent_local_promotion_admission_receipt_v0.example.json")
    MODULE.validate_receipt(receipt)
    assert receipt["shared_ledger_state"] == "unchanged"
    assert receipt["semantic_transition"] == "not_performed"


def test_cross_tenant_promotion_is_rejected() -> None:
    candidate = load("agent_local_shared_promotion_candidate_v0.example.json")
    candidate["target"]["tenant_id"] = "tenant:other"
    with pytest.raises(ValueError, match="cross tenant"):
        MODULE.validate_candidate(candidate)


@pytest.mark.parametrize(
    ("decision", "duplicate", "conflict", "expected", "has_candidate"),
    [
        ("approve", "none", "none", "memo_candidate", True),
        ("narrow", "none", "resolved", "memo_candidate", True),
        ("approve", "exact_duplicate", "none", "duplicate_no_write", False),
        ("approve", "none", "unresolved", "conflict_quarantine", False),
        ("reject", "none", "none", "rejected", False),
        ("defer", "none", "none", "deferred", False),
    ],
)
def test_review_duplicate_and_conflict_matrix(
    decision: str,
    duplicate: str,
    conflict: str,
    expected: str,
    has_candidate: bool,
) -> None:
    receipt = copy.deepcopy(load("agent_local_promotion_admission_receipt_v0.example.json"))
    receipt["operator_decision"]["decision"] = decision
    receipt["duplicate_status"] = duplicate
    receipt["duplicate_refs"] = [] if duplicate == "none" else ["memory:existing"]
    receipt["conflict_status"] = conflict
    receipt["conflict_refs"] = [] if conflict == "none" else ["memory:conflict"]
    receipt["result"] = expected
    receipt["memo_candidate_ref"] = "candidate:aoa-memo/retry-001" if has_candidate else None
    MODULE.validate_receipt(receipt)


def test_auto_shared_write_and_semantic_transition_are_forbidden() -> None:
    receipt = load("agent_local_promotion_admission_receipt_v0.example.json")
    receipt["shared_ledger_state"] = "written"
    with pytest.raises(Exception):
        MODULE.validate_receipt(receipt)

    receipt = load("agent_local_promotion_admission_receipt_v0.example.json")
    receipt["semantic_transition"] = "performed"
    with pytest.raises(Exception):
        MODULE.validate_receipt(receipt)
