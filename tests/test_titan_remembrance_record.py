from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict[str, object]:
    payload = json.loads((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def validator() -> Draft202012Validator:
    schema = load_json("schemas/titan_remembrance_record.schema.json")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_titan_remembrance_candidate_example_validates() -> None:
    errors = list(
        validator().iter_errors(
            load_json("examples/titan_remembrance_record.example.json")
        )
    )

    assert errors == []


def test_titan_remembrance_candidate_requires_provenance_anchor() -> None:
    payload = load_json("examples/titan_remembrance_record.example.json")
    payload.pop("source_refs")

    errors = list(validator().iter_errors(payload))

    assert errors


def test_legacy_titan_remembrance_record_shape_still_validates() -> None:
    payload = {
        "record_id": "remember:titan:atlas:legacy-example",
        "titan_name": "Atlas",
        "bearer_id": "titan:atlas:founder",
        "role_key": "architect",
        "memory_kind": "remembrance",
        "source_ref": "docs/TITAN_MEMORY_LOOM_POSTURE.md",
        "summary": "Legacy remembrance records remain source-anchored memory.",
        "confidence": 0.75,
        "redaction_state": "clear",
    }

    assert list(validator().iter_errors(payload)) == []


def test_legacy_titan_remembrance_record_rejects_escape_hatches() -> None:
    payload = {
        "record_id": "remember:titan:atlas:legacy-example",
        "titan_name": "Atlas",
        "bearer_id": "titan:atlas:founder",
        "role_key": "architect",
        "memory_kind": "remembrance",
        "source_ref": "docs/TITAN_MEMORY_LOOM_POSTURE.md",
        "summary": "Legacy remembrance records remain source-anchored memory.",
    }
    mutated = copy.deepcopy(payload)
    mutated["runtime_authority"] = True

    errors = list(validator().iter_errors(mutated))

    assert errors
