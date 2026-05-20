from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


PART_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PART_ROOT / "schemas" / "memory_consolidation_forgetting_operation_v1.json"
EXAMPLES = sorted((PART_ROOT / "examples").glob("memory_consolidation_forgetting.*.example.json"))


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_consolidation_forgetting_examples_validate() -> None:
    validator = Draft202012Validator(load_json(SCHEMA_PATH))

    for example in EXAMPLES:
        errors = sorted(validator.iter_errors(load_json(example)), key=lambda error: list(error.path))
        assert errors == []


def test_lifecycle_changes_are_reviewed_and_audited() -> None:
    for example in EXAMPLES:
        payload = load_json(example)

        assert payload["review_route"]["decision_state"] in {"pending", "approved", "rejected"}
        assert payload["audit_event_ref"]
        assert payload["lifecycle_transition"]["from"] != payload["lifecycle_transition"]["to"]


def test_supersession_names_replacement() -> None:
    payload = load_json(PART_ROOT / "examples" / "memory_consolidation_forgetting.supersede.example.json")

    assert payload["operation_type"] == "supersede"
    assert payload["lifecycle_transition"]["replacement_memory_id"]
