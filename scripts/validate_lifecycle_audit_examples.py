#!/usr/bin/env python3
"""Validate lifecycle and audit examples for aoa-memo."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
SCHEMAS = ROOT / "schemas"

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema")
    raise SystemExit(2) from exc


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate(path: Path, validator: Draft202012Validator) -> dict:
    data = load_json(path)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    if errors:
        print(f"[FAIL] {path.name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {path.name}")
    return data


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    memory_validator = validator_for("memory_object.schema.json")
    thread_validator = validator_for("provenance_thread.schema.json")

    superseded_claim = validate(EXAMPLES / "claim.superseded.example.json", memory_validator)
    retracted_claim = validate(EXAMPLES / "claim.retracted.example.json", memory_validator)
    supersession_event = validate(EXAMPLES / "audit_event.supersession.example.json", memory_validator)
    retraction_event = validate(EXAMPLES / "audit_event.retraction.example.json", memory_validator)
    lifecycle_thread = validate(EXAMPLES / "provenance_thread.lifecycle.example.json", thread_validator)

    ensure(
        superseded_claim["kind"] == "claim" and superseded_claim["lifecycle"]["review_state"] == "superseded",
        "claim.superseded.example.json must be a superseded claim",
    )
    ensure(
        retracted_claim["kind"] == "claim" and retracted_claim["lifecycle"]["review_state"] == "retracted",
        "claim.retracted.example.json must be a retracted claim",
    )
    ensure(
        supersession_event["kind"] == "audit_event",
        "audit_event.supersession.example.json must be an audit_event",
    )
    ensure(
        retraction_event["kind"] == "audit_event",
        "audit_event.retraction.example.json must be an audit_event",
    )

    thread_ids = set(lifecycle_thread["memory_object_ids"])
    for required_id in (
        superseded_claim["id"],
        retracted_claim["id"],
        supersession_event["id"],
        retraction_event["id"],
    ):
        ensure(required_id in thread_ids, f"provenance_thread.lifecycle.example.json missing {required_id}")

    ensure(
        superseded_claim["provenance"]["provenance_thread_id"] == lifecycle_thread["id"],
        "superseded claim must point to lifecycle provenance thread",
    )
    ensure(
        retracted_claim["provenance"]["provenance_thread_id"] == lifecycle_thread["id"],
        "retracted claim must point to lifecycle provenance thread",
    )
    ensure(
        supersession_event["provenance"]["provenance_thread_id"] == lifecycle_thread["id"],
        "supersession audit event must point to lifecycle provenance thread",
    )
    ensure(
        retraction_event["provenance"]["provenance_thread_id"] == lifecycle_thread["id"],
        "retraction audit event must point to lifecycle provenance thread",
    )

    print("Lifecycle and audit examples validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
