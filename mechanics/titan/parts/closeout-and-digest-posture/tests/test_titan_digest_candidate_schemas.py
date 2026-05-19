from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = REPO_ROOT / "mechanics" / "titan" / "parts" / "closeout-and-digest-posture"


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def validator(schema_name: str) -> Draft202012Validator:
    schema = load_json(PART_ROOT / "schemas" / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def example(example_name: str) -> dict:
    return load_json(PART_ROOT / "examples" / example_name)


def error_messages(schema_name: str, payload: dict) -> list[str]:
    return [error.message for error in validator(schema_name).iter_errors(payload)]


def test_titan_bridge_memory_candidate_constrains_field_types() -> None:
    payload = example("titan_bridge_memory_candidate.example.json")
    assert error_messages("titan_bridge_memory_candidate.schema.json", payload) == []

    payload["session_id"] = {"not": "a-string"}
    assert any(
        "is not of type 'string'" in message
        for message in error_messages("titan_bridge_memory_candidate.schema.json", payload)
    )


def test_titan_closeout_candidate_example_matches_schema() -> None:
    payload = example("titan_closeout_candidate.example.json")
    assert error_messages("titan_closeout_candidate.schema.json", payload) == []

    payload.pop("source_receipt")
    assert any(
        "source_receipt" in message
        for message in error_messages("titan_closeout_candidate.schema.json", payload)
    )


def test_titan_console_memory_digest_example_matches_schema() -> None:
    payload = example("titan_console_memory_digest.example.json")
    assert error_messages("titan_console_memory_digest.schema.json", payload) == []

    payload.pop("writeback_candidates")
    assert any(
        "writeback_candidates" in message
        for message in error_messages("titan_console_memory_digest.schema.json", payload)
    )


def test_titan_memory_digest_example_matches_schema() -> None:
    payload = example("titan_memory_digest.example.json")
    assert error_messages("titan_memory_digest.schema.json", payload) == []

    payload.pop("record_count")
    assert any(
        "record_count" in message
        for message in error_messages("titan_memory_digest.schema.json", payload)
    )
