from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    payload = json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def validator(schema_name: str) -> Draft202012Validator:
    schema = load_json(f"schemas/{schema_name}")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def error_messages(schema_name: str, payload: dict) -> list[str]:
    return [error.message for error in validator(schema_name).iter_errors(payload)]


def test_titan_memory_candidate_requires_time_boundary_and_risk_pair() -> None:
    payload = load_json("examples/titan_memory_candidate.example.json")
    assert error_messages("titan_memory_candidate.schema.json", payload) == []

    missing_time_boundary = dict(payload)
    missing_time_boundary.pop("time_boundary")
    assert any("time_boundary" in message for message in error_messages(
        "titan_memory_candidate.schema.json",
        missing_time_boundary,
    ))

    missing_risk = dict(payload)
    missing_risk["risks"] = {"if_stored": "Stored risk only."}
    assert any("if_not_stored" in message for message in error_messages(
        "titan_memory_candidate.schema.json",
        missing_risk,
    ))


def test_titan_writeback_candidate_requires_owner_surface_and_retention_risk() -> None:
    payload = {
        "candidate_id": "titan-writeback-candidate:example",
        "source_records": ["repo:aoa-memo/mechanics/titan/docs/TITAN_MEMORY_LOOM_POSTURE.md"],
        "reason": "Example candidate for schema regression.",
        "owner_surface": "mechanics/titan/docs/TITAN_MEMORY_LOOM_POSTURE.md",
        "retention_risk": "May preserve an early wave too strongly.",
        "operator_approval": "pending",
    }
    assert error_messages("titan_memory_writeback_candidate.schema.json", payload) == []

    payload.pop("owner_surface")
    assert any("owner_surface" in message for message in error_messages(
        "titan_memory_writeback_candidate.schema.json",
        payload,
    ))


def test_titan_bridge_memory_candidate_constrains_field_types() -> None:
    payload = load_json("examples/titan_bridge_memory_candidate.example.json")
    assert error_messages("titan_bridge_memory_candidate.schema.json", payload) == []

    payload["session_id"] = {"not": "a-string"}
    assert any("is not of type 'string'" in message for message in error_messages(
        "titan_bridge_memory_candidate.schema.json",
        payload,
    ))
