#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema


PART_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PART_ROOT / "schemas"
EXAMPLE_ROOT = PART_ROOT / "examples"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def validate_schema(payload: dict[str, Any], schema_path: Path) -> None:
    jsonschema.Draft202012Validator(read_json(schema_path)).validate(payload)


def validate_candidate(payload: dict[str, Any]) -> None:
    validate_schema(
        payload,
        SCHEMA_ROOT / "agent_local_shared_promotion_candidate_v0.schema.json",
    )
    source = payload["source_namespace"]
    target = payload["target"]
    if source["tenant_id"] != target["tenant_id"]:
        raise ValueError("agent-local promotion cannot cross tenant")
    if not payload["outcome_refs"]:
        raise ValueError("agent-local promotion requires outcome evidence")


def expected_result(receipt: dict[str, Any]) -> tuple[str, bool]:
    decision = receipt["operator_decision"]["decision"]
    if decision == "reject":
        return "rejected", False
    if decision == "defer":
        return "deferred", False
    if receipt["duplicate_status"] != "none":
        return "duplicate_no_write", False
    if receipt["conflict_status"] == "unresolved":
        return "conflict_quarantine", False
    return "memo_candidate", True


def validate_receipt(payload: dict[str, Any]) -> None:
    validate_schema(
        payload,
        SCHEMA_ROOT / "agent_local_promotion_admission_receipt_v0.schema.json",
    )
    result, needs_candidate = expected_result(payload)
    if payload["result"] != result:
        raise ValueError(f"result must be {result}")
    if needs_candidate != (payload["memo_candidate_ref"] is not None):
        raise ValueError("memo_candidate_ref does not match admission result")
    if payload["duplicate_status"] == "none" and payload["duplicate_refs"]:
        raise ValueError("duplicate_refs require a duplicate status")
    if payload["duplicate_status"] != "none" and not payload["duplicate_refs"]:
        raise ValueError("duplicate status requires duplicate_refs")
    if payload["conflict_status"] == "none" and payload["conflict_refs"]:
        raise ValueError("conflict_refs require a conflict status")
    if payload["conflict_status"] != "none" and not payload["conflict_refs"]:
        raise ValueError("conflict status requires conflict_refs")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=Path,
        default=EXAMPLE_ROOT / "agent_local_shared_promotion_candidate_v0.example.json",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=EXAMPLE_ROOT / "agent_local_promotion_admission_receipt_v0.example.json",
    )
    args = parser.parse_args()
    validate_candidate(read_json(args.candidate))
    validate_receipt(read_json(args.receipt))
    print("[ok] agent-local promotion remains reviewed candidate admission only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
