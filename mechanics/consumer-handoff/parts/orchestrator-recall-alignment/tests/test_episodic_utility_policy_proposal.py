from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[5]
PART = (
    ROOT
    / "mechanics"
    / "consumer-handoff"
    / "parts"
    / "orchestrator-recall-alignment"
)
SCRIPTS = PART / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from episodic_utility import (  # noqa: E402
    ZERO_DIGEST,
    build_episodic_utility_policy_proposal,
    canonical_digest,
    validate_episodic_utility_policy_proposal,
)


SCHEMA_PATH = (
    PART
    / "schemas"
    / "outcome_qualified_episodic_utility_policy_proposal_v0.schema.json"
)


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def provenance(owner: str, ref: str, digit: str) -> dict[str, str]:
    return {
        "owner_repo": owner,
        "artifact_ref": ref,
        "artifact_version": "1",
        "artifact_digest": "sha256:" + (digit * 64),
    }


def item(criticality: str = "ordinary") -> dict:
    ref = provenance("aoa-memo", f"memory:episode:{criticality}", "1")
    return {
        "item_ref": ref,
        "memory_class": "episodic",
        "criticality": criticality,
        "semantic_digest": "sha256:" + ("2" * 64),
    }


def aggregate(
    item_payload: dict,
    *,
    qualified: int = 3,
    signed_mean: float = 1.0,
    pending: int = 0,
    accidental: int = 0,
    critical: int = 0,
) -> dict:
    payload = {
        "schema_version": "aoa_stats_episodic_utility_aggregate_v0",
        "aggregate_id": "aggregate:test",
        "aggregate_version": 1,
        "stats_owner": "aoa-stats",
        "item_ref": item_payload["item_ref"],
        "qualified_observation_count": qualified,
        "pending_or_overdue_delayed_count": pending,
        "accidental_success_count": accidental,
        "critical_event_count": critical,
        "measurement": {
            "qualified_signed_outcome_mean": signed_mean,
        },
        "access_count_used_as_utility": False,
        "proof_verdict": "forbidden",
        "semantic_authority": "none",
        "effect_authority": "none",
        "content_digest": ZERO_DIGEST,
    }
    payload["content_digest"] = canonical_digest(payload)
    return payload


def base_policy() -> dict:
    payload = {
        "owner": "aoa-memo",
        "policy_id": "policy:episodic-utility:test",
        "version": "v0",
        "ranking_weight": 0.5,
        "ranking_weight_min": 0.25,
        "ranking_weight_max": 0.75,
        "critical_weight_floor": 0.6,
        "cooldown_seconds": 300,
        "projection_choice": "default",
        "abstraction_level": "exact",
        "cadence_seconds": 3600,
        "budget_tokens": 512,
    }
    payload["content_digest"] = canonical_digest(payload)
    return payload


def verdict(*, supported: bool = True, reward_hacking: bool = True) -> dict:
    return {
        "owner_repo": "aoa-evals",
        "verdict_id": "verdict:phase9:test",
        "verdict": "supported_bounded_adjustment" if supported else "freeze",
        "holdout_checked": True,
        "delayed_effects_checked": True,
        "accidental_success_checked": True,
        "reward_hacking_passed": reward_hacking,
        "evidence_ref": provenance("aoa-evals", "report:phase9:test", "3"),
    }


def proposal(
    item_payload: dict,
    aggregate_payload: dict,
    verdict_payload: dict,
) -> dict:
    return build_episodic_utility_policy_proposal(
        proposal_id="proposal:phase9:test",
        candidate_version="v1",
        aggregate=aggregate_payload,
        item=item_payload,
        base_policy=base_policy(),
        eval_verdict=verdict_payload,
        decision_ref=(
            "docs/decisions/"
            "AOA-MEM-D-0078-outcome-qualified-utility-stays-proposal-only.md"
        ),
        produced_at="2026-07-29T12:00:00Z",
    )


def test_positive_outcome_supports_only_a_bounded_proposal() -> None:
    item_payload = item()
    result = proposal(item_payload, aggregate(item_payload), verdict())

    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    errors = list(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(result)
    )
    assert errors == []
    assert validate_episodic_utility_policy_proposal(result) == []
    assert result["proposal_state"] == "bounded_adjustment_proposed"
    assert result["policy_candidate"]["ranking_weight"] == 0.6
    assert result["apply_allowed"] is False
    assert result["semantic_state"]["changed"] is False


def test_pending_delayed_outcome_freezes_positive_adjustment() -> None:
    item_payload = item()
    result = proposal(
        item_payload,
        aggregate(item_payload, pending=1),
        verdict(),
    )

    assert result["proposal_state"] == "frozen"
    assert result["policy_candidate"]["ranking_weight"] == 0.5
    assert validate_episodic_utility_policy_proposal(result) == []


def test_reward_hacking_or_accidental_success_cannot_gain_weight() -> None:
    item_payload = item()
    reward_hack = proposal(
        item_payload,
        aggregate(item_payload),
        verdict(reward_hacking=False),
    )
    accidental = proposal(
        item_payload,
        aggregate(item_payload, accidental=1),
        verdict(),
    )

    assert reward_hack["proposal_state"] == "frozen"
    assert accidental["proposal_state"] == "frozen"
    assert reward_hack["policy_candidate"]["ranking_weight"] == 0.5
    assert accidental["policy_candidate"]["ranking_weight"] == 0.5


def test_rare_critical_item_preserves_floor_without_semantic_mutation() -> None:
    item_payload = item("safety_critical")
    result = proposal(
        item_payload,
        aggregate(
            item_payload,
            qualified=1,
            signed_mean=-1.0,
            critical=1,
        ),
        verdict(),
    )

    assert result["proposal_state"] == "preserve_critical"
    assert result["policy_candidate"]["ranking_weight"] == 0.6
    assert result["policy_candidate"]["projection_choice"] == "source_first"
    assert result["semantic_state"]["before_digest"] == (
        result["semantic_state"]["after_digest"]
    )
    assert validate_episodic_utility_policy_proposal(result) == []


def test_access_count_is_not_an_input_and_cannot_change_proposal() -> None:
    item_payload = item()
    aggregate_payload = aggregate(item_payload)
    low_access_metadata = {"access_count": 0}
    high_access_metadata = {"access_count": 1000000}

    low = proposal(item_payload, aggregate_payload, verdict())
    high = proposal(item_payload, deepcopy(aggregate_payload), verdict())

    assert low_access_metadata != high_access_metadata
    assert low == high
