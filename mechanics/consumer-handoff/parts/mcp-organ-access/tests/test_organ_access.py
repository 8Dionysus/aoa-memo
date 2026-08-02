from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


PART_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PART_ROOT / "config/organ-access.v1.json"
SCHEMA_PATH = PART_ROOT / "schemas/organ-access.schema.json"


def _payload() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_organ_access_manifest_is_schema_valid_and_owner_bounded() -> None:
    payload = _payload()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)

    assert payload["contains_secrets"] is False
    assert payload["admission_asserted"] is False
    assert payload["owner_acceptance_asserted"] is False
    assert payload["proof_asserted"] is False
    assert payload["effect_activation_authorized"] is False
    assert all(value is False for value in payload["guardrails"].values())


def test_read_and_candidate_contours_are_exact_and_disjoint() -> None:
    capabilities = {
        item["capability_id"]: item
        for item in _payload()["capabilities"]
    }
    assert set(capabilities) == {
        "durable-memory-read",
        "memory-candidate-prepare",
    }
    read = capabilities["durable-memory-read"]
    candidate = capabilities["memory-candidate-prepare"]
    assert read["credential_class"] == "memo-read"
    assert candidate["credential_class"] == "memo-candidate"
    read_names = {item["mcp_name"] for item in read["primitives"]}
    candidate_names = {item["mcp_name"] for item in candidate["primitives"]}
    assert read_names == {
        "aoa_memo_recall_brief",
        "aoa_memo_recall_reviewed",
        "aoa_memo_read_object",
        "aoa-memo://memory/object/{object_id}",
    }
    assert candidate_names == {
        "aoa_memo_create_candidate",
        "aoa_memo_prepare_intake_packet",
        "aoa_memo_prepare_forwarding_receipt",
    }
    assert read_names.isdisjoint(candidate_names)
    assert all(item["idempotency"] == "read_only" for item in read["primitives"])
    assert all(item["effect_class"] == "prepare_candidate" for item in candidate["primitives"])
