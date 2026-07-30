from __future__ import annotations

from collections.abc import Mapping
import hashlib
import json
from typing import Any


ZERO_DIGEST = "sha256:" + ("0" * 64)
ALLOWED_ADJUSTMENTS = (
    "ranking_weight",
    "cooldown",
    "projection_choice",
    "abstraction_level",
    "cadence",
    "budget",
)
FORBIDDEN_EFFECTS = (
    "semantic_promotion",
    "semantic_deletion",
    "semantic_retraction",
    "owner_change",
    "tenant_expansion",
    "permission_expansion",
    "automatic_policy_self_approval",
)
CRITICALITY_CLASSES = frozenset(
    {"safety_critical", "constitutional", "privacy", "audit"}
)


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def normalized_proposal_digest(proposal: Mapping[str, Any]) -> str:
    normalized = dict(proposal)
    normalized["content_digest"] = ZERO_DIGEST
    return canonical_digest(normalized)


def _bounded(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _validate_inputs(
    aggregate: Mapping[str, Any],
    item: Mapping[str, Any],
    base_policy: Mapping[str, Any],
    eval_verdict: Mapping[str, Any],
) -> None:
    if aggregate.get("schema_version") != "aoa_stats_episodic_utility_aggregate_v0":
        raise ValueError("utility proposal requires the exact stats aggregate v0")
    if (
        aggregate.get("stats_owner") != "aoa-stats"
        or aggregate.get("proof_verdict") != "forbidden"
        or aggregate.get("semantic_authority") != "none"
        or aggregate.get("effect_authority") != "none"
    ):
        raise ValueError("stats aggregate crossed its authority ceiling")
    if aggregate.get("access_count_used_as_utility") is not False:
        raise ValueError("access count cannot enter episodic utility")
    normalized_aggregate = dict(aggregate)
    normalized_aggregate["content_digest"] = ZERO_DIGEST
    if aggregate.get("content_digest") != canonical_digest(normalized_aggregate):
        raise ValueError("stats utility aggregate digest mismatch")
    if dict(aggregate.get("item_ref", {})) != dict(item.get("item_ref", {})):
        raise ValueError("stats aggregate item ref does not match memo item")
    if item.get("memory_class") != "episodic":
        raise ValueError("utility proposal v0 is episodic-only")
    if eval_verdict.get("owner_repo") != "aoa-evals":
        raise ValueError("utility proposal requires an aoa-evals verdict")
    if base_policy.get("owner") != "aoa-memo":
        raise ValueError("base episodic utility policy must be memo-owned")
    lower = base_policy.get("ranking_weight_min")
    upper = base_policy.get("ranking_weight_max")
    weight = base_policy.get("ranking_weight")
    if not all(isinstance(value, (int, float)) for value in (lower, upper, weight)):
        raise ValueError("ranking weights must be numeric")
    if not float(lower) <= float(weight) <= float(upper):
        raise ValueError("base ranking weight is outside its bounded range")


def build_episodic_utility_policy_proposal(
    *,
    proposal_id: str,
    candidate_version: str,
    aggregate: Mapping[str, Any],
    item: Mapping[str, Any],
    base_policy: Mapping[str, Any],
    eval_verdict: Mapping[str, Any],
    decision_ref: str,
    produced_at: str,
) -> dict[str, Any]:
    """Build one memo-owned proposal; never apply a policy or mutate memory."""

    _validate_inputs(aggregate, item, base_policy, eval_verdict)

    before = {
        key: base_policy[key]
        for key in (
            "policy_id",
            "version",
            "ranking_weight",
            "ranking_weight_min",
            "ranking_weight_max",
            "cooldown_seconds",
            "projection_choice",
            "abstraction_level",
            "cadence_seconds",
            "budget_tokens",
            "content_digest",
        )
    }
    candidate = dict(before)
    candidate["version"] = candidate_version

    measurement = aggregate["measurement"]
    qualified_count = int(aggregate["qualified_observation_count"])
    pending_delayed = int(aggregate["pending_or_overdue_delayed_count"])
    accidental_success = int(aggregate["accidental_success_count"])
    criticality = item["criticality"]
    eval_checks_pass = all(
        eval_verdict.get(field) is True
        for field in (
            "holdout_checked",
            "delayed_effects_checked",
            "accidental_success_checked",
            "reward_hacking_passed",
        )
    )
    critical = (
        criticality in CRITICALITY_CLASSES
        or int(aggregate["critical_event_count"]) > 0
    )

    proposal_state = "frozen"
    rationale = "insufficient outcome-qualified evidence"
    if critical:
        proposal_state = "preserve_critical"
        rationale = "rare critical evidence keeps a preservation floor"
        floor = float(base_policy["critical_weight_floor"])
        candidate["ranking_weight"] = _bounded(
            max(float(before["ranking_weight"]), floor),
            float(before["ranking_weight_min"]),
            float(before["ranking_weight_max"]),
        )
        candidate["projection_choice"] = "source_first"
    elif (
        pending_delayed
        or accidental_success
        or not eval_checks_pass
        or eval_verdict.get("verdict") != "supported_bounded_adjustment"
    ):
        proposal_state = "frozen"
        if pending_delayed:
            rationale = "positive utility frozen until delayed outcomes close"
        elif accidental_success:
            rationale = "accidental success cannot reinforce episodic utility"
        elif not eval_verdict.get("reward_hacking_passed"):
            rationale = "reward-hacking check did not pass"
    elif qualified_count > 0:
        signed_mean = float(measurement["qualified_signed_outcome_mean"])
        if signed_mean > 0:
            proposal_state = "bounded_adjustment_proposed"
            rationale = "qualified positive outcome supports bounded ranking lift"
            candidate["ranking_weight"] = _bounded(
                float(before["ranking_weight"]) + min(0.1, signed_mean * 0.1),
                float(before["ranking_weight_min"]),
                float(before["ranking_weight_max"]),
            )
        elif signed_mean < 0:
            proposal_state = "bounded_adjustment_proposed"
            rationale = "qualified adverse outcome supports bounded ranking reduction"
            candidate["ranking_weight"] = _bounded(
                float(before["ranking_weight"]) - min(0.1, abs(signed_mean) * 0.1),
                float(before["ranking_weight_min"]),
                float(before["ranking_weight_max"]),
            )
            candidate["cooldown_seconds"] = int(before["cooldown_seconds"]) + 60

    candidate["content_digest"] = canonical_digest(
        {
            key: value
            for key, value in candidate.items()
            if key != "content_digest"
        }
    )
    proposal = {
        "schema_version": "aoa_memo_episodic_utility_policy_proposal_v0",
        "proposal_id": proposal_id,
        "proposal_version": 1,
        "idempotency_key": f"{proposal_id}:{candidate_version}",
        "semantic_owner": "aoa-memo",
        "item": dict(item),
        "stats_aggregate_ref": {
            "owner_repo": "aoa-stats",
            "artifact_ref": str(aggregate["aggregate_id"]),
            "artifact_version": str(aggregate["aggregate_version"]),
            "artifact_digest": str(aggregate["content_digest"]),
        },
        "eval_verdict": dict(eval_verdict),
        "decision_ref": decision_ref,
        "allowed_adjustments": list(ALLOWED_ADJUSTMENTS),
        "proposal_state": proposal_state,
        "rationale": rationale,
        "policy_before": before,
        "policy_candidate": candidate,
        "semantic_state": {
            "before_digest": item["semantic_digest"],
            "after_digest": item["semantic_digest"],
            "changed": False,
        },
        "rollback": {
            "target_policy_id": before["policy_id"],
            "target_version": before["version"],
            "target_policy_digest": before["content_digest"],
            "target_ranking_weight": before["ranking_weight"],
            "target_cooldown_seconds": before["cooldown_seconds"],
            "target_projection_choice": before["projection_choice"],
            "rebuild_disposable_projection": True,
        },
        "forbidden_effects": list(FORBIDDEN_EFFECTS),
        "approval_state": "operator_required",
        "apply_allowed": False,
        "live_effect": False,
        "semantic_authority": "none",
        "effect_authority": "none",
        "produced_at": produced_at,
        "content_digest": ZERO_DIGEST,
    }
    proposal["content_digest"] = normalized_proposal_digest(proposal)
    return proposal


def validate_episodic_utility_policy_proposal(
    proposal: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    if proposal.get("schema_version") != (
        "aoa_memo_episodic_utility_policy_proposal_v0"
    ):
        issues.append("unknown episodic utility proposal version")
    if tuple(proposal.get("allowed_adjustments", ())) != ALLOWED_ADJUSTMENTS:
        issues.append("utility proposal allowed-adjustment set drifted")
    if tuple(proposal.get("forbidden_effects", ())) != FORBIDDEN_EFFECTS:
        issues.append("utility proposal forbidden-effect set drifted")
    if proposal.get("approval_state") != "operator_required":
        issues.append("utility proposal requires operator approval")
    if proposal.get("apply_allowed") is not False:
        issues.append("utility proposal cannot apply itself")
    if proposal.get("live_effect") is not False:
        issues.append("utility proposal cannot have a live effect")
    if proposal.get("semantic_authority") != "none":
        issues.append("utility proposal cannot carry semantic authority")
    if proposal.get("effect_authority") != "none":
        issues.append("utility proposal cannot carry effect authority")

    semantic_state = proposal.get("semantic_state")
    if not isinstance(semantic_state, Mapping) or (
        semantic_state.get("changed") is not False
        or semantic_state.get("before_digest") != semantic_state.get("after_digest")
    ):
        issues.append("utility proposal cannot mutate semantic state")

    before = proposal.get("policy_before")
    candidate = proposal.get("policy_candidate")
    if isinstance(before, Mapping) and isinstance(candidate, Mapping):
        delta = abs(
            float(candidate["ranking_weight"]) - float(before["ranking_weight"])
        )
        if delta > 0.100000001:
            issues.append("ranking weight adjustment exceeds bounded delta")
        if not (
            float(candidate["ranking_weight_min"])
            <= float(candidate["ranking_weight"])
            <= float(candidate["ranking_weight_max"])
        ):
            issues.append("candidate ranking weight is outside its bounds")
        if proposal.get("proposal_state") == "frozen":
            comparable = (
                "ranking_weight",
                "cooldown_seconds",
                "projection_choice",
                "abstraction_level",
                "cadence_seconds",
                "budget_tokens",
            )
            if any(before[key] != candidate[key] for key in comparable):
                issues.append("frozen proposal cannot change policy behavior")
        if proposal.get("proposal_state") == "preserve_critical" and (
            float(candidate["ranking_weight"]) < float(before["ranking_weight"])
        ):
            issues.append("critical preservation cannot reduce ranking weight")

    if proposal.get("content_digest") != normalized_proposal_digest(proposal):
        issues.append("utility proposal normalized digest mismatch")
    return issues
