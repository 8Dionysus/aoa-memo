from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


PART_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PART_ROOT / "schemas" / "memory_write_path_guard_v1.json"
EXAMPLES = sorted((PART_ROOT / "examples").glob("memory_write_path_guard.*.example.json"))
HIGH_RISK_MARKERS = {
    "indirect_prompt_injection",
    "sleeper_memory",
    "poisoned_experience",
    "source_spoofing",
    "private_data_bleed",
    "instruction_as_content",
}


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_write_path_guard_examples_validate() -> None:
    validator = Draft202012Validator(load_json(SCHEMA_PATH))

    for example in EXAMPLES:
        errors = sorted(validator.iter_errors(load_json(example)), key=lambda error: list(error.path))
        assert errors == []


def test_high_risk_inputs_cannot_skip_review() -> None:
    for example in EXAMPLES:
        payload = load_json(example)
        risks = set(payload["ingestion_risks"])
        decision = payload["review_route"]["decision_state"]
        result = payload["allowed_write_result"]
        lifecycle = payload["proposed_lifecycle"]

        if risks & HIGH_RISK_MARKERS:
            assert result in {"reject", "quarantine", "candidate_only", "archive_only"}
            assert decision in {"pending_review", "rejected", "quarantined", "approved_candidate"}
            assert lifecycle != "frozen"


def test_derived_or_untrusted_writes_keep_lineage() -> None:
    for example in EXAMPLES:
        payload = load_json(example)
        lineage = payload["derivation_lineage"]
        if payload["source_trust"] in {"untrusted", "unknown"} or lineage["method"] != "direct_owner_write":
            assert lineage["derived_from_refs"]
            assert lineage["reviewed_by"]


def test_action_text_is_not_executable_by_memo() -> None:
    for example in EXAMPLES:
        payload = load_json(example)
        action = payload["action_safety_separation"]

        assert action["action_text_is_data"] is True
        if payload["source_trust"] in {"untrusted", "unknown"}:
            assert action["execution_owner"] == "none"
