from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def validator() -> Draft202012Validator:
    schema = json.loads((ROOT / "schemas" / "titan_audit_memory_candidate.schema.json").read_text(encoding="utf-8"))
    assert isinstance(schema, dict)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def candidate_payload() -> dict[str, object]:
    return {
        "memory_candidate_id": "memo:titan-audit:example",
        "kind": "titan_swarm_lesson",
        "claim": "A closeout lesson can become a candidate only with source refs and an owner route hint.",
        "source_refs": ["repo:aoa-memo/docs/TITAN_AUDIT_MEMORY_POLICY.md"],
        "owner_route_hint": "repo:aoa-memo/docs/TITAN_AUDIT_MEMORY_POLICY.md",
        "titan_name": "Mneme",
        "authority": "candidate",
        "promotion_status": "candidate",
    }


def test_titan_audit_memory_candidate_accepts_policy_required_owner_route_hint() -> None:
    assert list(validator().iter_errors(candidate_payload())) == []


def test_titan_audit_memory_candidate_requires_owner_route_hint() -> None:
    payload = copy.deepcopy(candidate_payload())
    payload.pop("owner_route_hint")

    assert list(validator().iter_errors(payload))
