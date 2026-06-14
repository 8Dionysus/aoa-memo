from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import validate_memo


def receipt_payload(*, schema: str, result: str, checker_field: str) -> dict:
    return {
        "schema": schema,
        "id": "receipt:example-repo:20260520T171500Z:codex-plane-memory-route",
        "repo": "example-repo",
        "candidate_ref": "candidates/20260520T171200Z.codex-plane-memory-route.candidate.json",
        "result": result,
        "route": "reviewed_intake",
        "checks": ["schema"],
        "errors": [],
        "created_at": "2026-05-20T17:15:00Z",
        checker_field: "test-suite",
    }


def receipt_schema_errors(payload: dict) -> list[str]:
    validator = validate_memo.validator_for("local_memo_receipt.schema.json")
    return [error.message for error in validator.iter_errors(payload)]


def test_local_memo_receipt_schema_accepts_legacy_v1_reviewed_by() -> None:
    payload = receipt_payload(
        schema="aoa_local_memo_receipt_v1",
        result="reviewed",
        checker_field="reviewed_by",
    )

    assert receipt_schema_errors(payload) == []


def test_local_memo_receipt_schema_accepts_v2_checked_by() -> None:
    payload = receipt_payload(
        schema="aoa_local_memo_receipt_v2",
        result="forwarded",
        checker_field="checked_by",
    )

    assert receipt_schema_errors(payload) == []


def test_local_memo_receipt_schema_rejects_v1_checked_by_mix() -> None:
    payload = receipt_payload(
        schema="aoa_local_memo_receipt_v1",
        result="forwarded",
        checker_field="checked_by",
    )

    assert receipt_schema_errors(payload)


def test_local_memo_receipt_schema_rejects_v2_reviewed_by_mix() -> None:
    payload = receipt_payload(
        schema="aoa_local_memo_receipt_v2",
        result="reviewed",
        checker_field="reviewed_by",
    )

    assert receipt_schema_errors(payload)
