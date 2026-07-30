from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from typing import Any


ZERO_DIGEST = "sha256:" + ("0" * 64)
BASE_SCHEMA_ID = (
    "https://raw.githubusercontent.com/8Dionysus/aoa-memo/main/"
    "schemas/support-objects/active_organ_memo_contracts_v1.schema.json"
)
BASE_SCHEMA_DIGEST = (
    "sha256:ecb9b6fb8abe8633d1505b12c396d8e4cfaee6d560ec20617268ce02574ff99d"
)
DECISION_REF = (
    "docs/decisions/"
    "AOA-MEM-D-0079-mechanical-lifecycle-is-allowlisted-and-recoverable.md"
)

MECHANICAL_SPECS = {
    "projection_invalidation": ("projection", "not_forgetting"),
    "projection_rebuild": ("projection", "not_forgetting"),
    "compaction": ("derived_artifact", "compression"),
    "explicit_ephemeral_ttl": ("ephemeral_object", "expiry"),
    "queue_cancellation": ("queue_item", "not_forgetting"),
    "owner_approved_archive_deadline": ("canonical_lifecycle", "archive"),
    "cache_expiry": ("cache", "expiry"),
    "generation_rollover": ("projection", "not_forgetting"),
    "obsolete_derived_artifact_removal": (
        "derived_artifact",
        "ordinary_deletion",
    ),
}
SEMANTIC_SPECS = {
    "conflict": "not_forgetting",
    "merge_split": "merge",
    "narrowed_applicability": "demotion",
    "supersession": "supersession",
    "retraction": "retraction",
    "archive": "archive",
    "temperature_salience_change": "decay",
    "retention_change": "not_forgetting",
}
FORGETTING_CLASSES = frozenset(
    {
        "not_forgetting",
        "decay",
        "demotion",
        "compression",
        "merge",
        "supersession",
        "retraction",
        "quarantine",
        "expiry",
        "archive",
        "ordinary_deletion",
        "privacy_erasure",
        "model_unlearning",
    }
)

PLAN_FIELDS = frozenset(
    {
        "schema_version",
        "contract_id",
        "contract_subtype",
        "plan_id",
        "idempotency_key",
        "owner",
        "decision_ref",
        "base_schema_id",
        "base_schema_digest",
        "operation_class",
        "forgetting_class",
        "subject_pin",
        "policy_pin",
        "preconditions",
        "effect_scope",
        "transaction",
        "compensation",
        "receipt_contract",
        "generated_at",
        "content_digest",
        "execution_posture",
        "live_runtime_authority",
        "semantic_authority",
    }
)
PROPOSAL_FIELDS = frozenset(
    {
        "schema_version",
        "proposal_id",
        "idempotency_key",
        "owner",
        "decision_ref",
        "operation_class",
        "forgetting_class",
        "subject_pin",
        "evidence_refs",
        "proposed_diff",
        "operator_review",
        "attention_budget",
        "proposal_state",
        "generated_at",
        "content_digest",
        "apply_allowed",
        "execution_posture",
        "semantic_authority",
    }
)
RECEIPT_FIELDS = frozenset(
    {
        "schema_version",
        "receipt_id",
        "plan_ref",
        "idempotency_key",
        "runtime_owner",
        "attempt",
        "status",
        "expected_prior_version",
        "observed_prior_version",
        "result_version",
        "belief_commit_id",
        "canonical_commit_applied",
        "new_effect_applied",
        "projection_posture",
        "compensation_state",
        "event_chain",
        "commit_receipt_ref",
        "audit_receipt_ref",
        "semantic_digest_before",
        "semantic_digest_after",
        "tenant_before",
        "tenant_after",
        "namespace_before",
        "namespace_after",
        "partial_is_success",
        "produced_at",
        "content_digest",
        "execution_authority",
    }
)


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def normalized_digest(payload: Mapping[str, Any]) -> str:
    normalized = deepcopy(dict(payload))
    normalized["content_digest"] = ZERO_DIGEST
    return canonical_digest(normalized)


def _aware_datetime(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _shape_issues(
    payload: Mapping[str, Any],
    *,
    required: frozenset[str],
    label: str,
) -> list[str]:
    actual = set(payload)
    issues = []
    if missing := sorted(required - actual):
        issues.append(f"{label} missing fields: {', '.join(missing)}")
    if unknown := sorted(actual - required):
        issues.append(f"{label} unknown fields: {', '.join(unknown)}")
    return issues


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _unique_nonempty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item) for item in value)
        and len(value) == len(set(value))
    )


def build_mechanical_lifecycle_plan(
    *,
    plan_id: str,
    idempotency_key: str,
    operation_class: str,
    subject_pin: Mapping[str, Any],
    policy_pin: Mapping[str, Any],
    effect_owner_repo: str,
    target_refs: Sequence[str],
    eligible_at: str,
    deadline_at: str,
    max_attempts: int,
    backoff_seconds: Sequence[int],
    cancellation_token: str,
    owner_approval_ref: str | None,
    compensation_strategy: str,
    compensation_action_class: str,
    commit_receipt_ref: str,
    audit_receipt_ref: str,
    generated_at: str,
) -> dict[str, Any]:
    """Build one strict C06-compatible reference-lab mechanical plan."""

    if operation_class not in MECHANICAL_SPECS:
        raise ValueError("operation_class is not in the mechanical allowlist")
    surface_class, forgetting_class = MECHANICAL_SPECS[operation_class]
    expected_version = int(subject_pin["object_version"])
    plan = {
        "schema_version": "aoa_memo_mechanical_lifecycle_plan_v0",
        "contract_id": "C06",
        "contract_subtype": "MechanicalLifecyclePlanExtension",
        "plan_id": plan_id,
        "idempotency_key": idempotency_key,
        "owner": "aoa-memo",
        "decision_ref": DECISION_REF,
        "base_schema_id": BASE_SCHEMA_ID,
        "base_schema_digest": BASE_SCHEMA_DIGEST,
        "operation_class": operation_class,
        "forgetting_class": forgetting_class,
        "subject_pin": dict(subject_pin),
        "policy_pin": dict(policy_pin),
        "preconditions": {
            "expected_prior_version": expected_version,
            "expected_state": subject_pin["lifecycle_state"],
            "expected_source_generation": subject_pin["source_generation"],
            "eligible_at": eligible_at,
            "owner_approval_ref": owner_approval_ref,
        },
        "effect_scope": {
            "owner_repo": effect_owner_repo,
            "surface_class": surface_class,
            "target_refs": list(target_refs),
            "canonical_semantic_mutation": False,
            "physical_erasure": False,
            "cross_tenant": False,
            "permission_change": False,
        },
        "transaction": {
            "next_version": expected_version + 1,
            "commit_mode": "recoverable",
            "deadline_at": deadline_at,
            "max_attempts": max_attempts,
            "backoff_seconds": list(backoff_seconds),
            "cancellation_token": cancellation_token,
        },
        "compensation": {
            "strategy": compensation_strategy,
            "target_version": expected_version,
            "target_semantic_digest": subject_pin["semantic_digest"],
            "action_class": compensation_action_class,
        },
        "receipt_contract": {
            "commit_receipt_ref": commit_receipt_ref,
            "audit_receipt_ref": audit_receipt_ref,
            "partial_status": "partial_pending_repair",
            "success_requires_audit": True,
        },
        "generated_at": generated_at,
        "content_digest": ZERO_DIGEST,
        "execution_posture": "reference_lab_only",
        "live_runtime_authority": False,
        "semantic_authority": "none",
    }
    plan["content_digest"] = normalized_digest(plan)
    issues = validate_mechanical_lifecycle_plan(plan)
    if issues:
        raise ValueError("; ".join(issues))
    return plan


def validate_mechanical_lifecycle_plan(
    plan: Mapping[str, Any],
) -> list[str]:
    issues = _shape_issues(plan, required=PLAN_FIELDS, label="mechanical plan")
    expected_literals = {
        "schema_version": "aoa_memo_mechanical_lifecycle_plan_v0",
        "contract_id": "C06",
        "contract_subtype": "MechanicalLifecyclePlanExtension",
        "owner": "aoa-memo",
        "decision_ref": DECISION_REF,
        "base_schema_id": BASE_SCHEMA_ID,
        "base_schema_digest": BASE_SCHEMA_DIGEST,
        "execution_posture": "reference_lab_only",
        "live_runtime_authority": False,
        "semantic_authority": "none",
    }
    for field, expected in expected_literals.items():
        if plan.get(field) != expected:
            issues.append(f"{field} must remain {expected!r}")

    operation_class = plan.get("operation_class")
    spec = MECHANICAL_SPECS.get(str(operation_class))
    if spec is None:
        issues.append("operation_class is not in the exact mechanical allowlist")
    elif plan.get("forgetting_class") != spec[1]:
        issues.append("forgetting_class does not match operation_class")
    if plan.get("forgetting_class") not in FORGETTING_CLASSES:
        issues.append("unknown forgetting_class")

    subject = _mapping(plan.get("subject_pin"))
    policy = _mapping(plan.get("policy_pin"))
    preconditions = _mapping(plan.get("preconditions"))
    effect = _mapping(plan.get("effect_scope"))
    transaction = _mapping(plan.get("transaction"))
    compensation = _mapping(plan.get("compensation"))
    receipt_contract = _mapping(plan.get("receipt_contract"))

    subject_required = {
        "owner_repo",
        "object_ref",
        "object_version",
        "lifecycle_state",
        "semantic_digest",
        "tenant_id",
        "namespace_id",
        "source_generation",
        "explicit_ephemeral",
        "disposable",
    }
    if set(subject) != subject_required:
        issues.append("subject_pin must contain the exact owner/version/scope fields")
    object_version = subject.get("object_version")
    source_generation = subject.get("source_generation")
    if not isinstance(object_version, int) or object_version < 1:
        issues.append("subject object_version must be a positive integer")
    if not isinstance(source_generation, int) or source_generation < 1:
        issues.append("subject source_generation must be a positive integer")

    policy_required = {
        "policy_id",
        "policy_version",
        "policy_digest",
        "decision_ref",
        "status",
        "approved_operation_classes",
    }
    if set(policy) != policy_required:
        issues.append("policy_pin must contain the exact policy fields")
    if policy.get("decision_ref") != DECISION_REF or policy.get("status") != "accepted":
        issues.append("mechanical policy must pin the accepted Phase 10 decision")
    approved = policy.get("approved_operation_classes")
    if not _unique_nonempty_strings(approved):
        issues.append("approved_operation_classes must be non-empty and unique")
    elif operation_class not in approved:
        issues.append("policy does not approve this operation_class")
    elif not set(approved).issubset(MECHANICAL_SPECS):
        issues.append("policy contains an operation outside the mechanical allowlist")

    if set(preconditions) != {
        "expected_prior_version",
        "expected_state",
        "expected_source_generation",
        "eligible_at",
        "owner_approval_ref",
    }:
        issues.append("preconditions must contain the exact comparison fields")
    if preconditions.get("expected_prior_version") != object_version:
        issues.append("expected_prior_version must match subject object_version")
    if preconditions.get("expected_state") != subject.get("lifecycle_state"):
        issues.append("expected_state must match subject lifecycle_state")
    if preconditions.get("expected_source_generation") != source_generation:
        issues.append("expected source generation must match subject pin")

    eligible_at = _aware_datetime(preconditions.get("eligible_at"))
    generated_at = _aware_datetime(plan.get("generated_at"))
    deadline_at = _aware_datetime(transaction.get("deadline_at"))
    if eligible_at is None:
        issues.append("eligible_at must be timezone-aware")
    if generated_at is None:
        issues.append("generated_at must be timezone-aware")
    if deadline_at is None:
        issues.append("deadline_at must be timezone-aware")
    if (
        eligible_at is not None
        and deadline_at is not None
        and deadline_at <= eligible_at
    ):
        issues.append("deadline_at must follow eligible_at")

    if set(effect) != {
        "owner_repo",
        "surface_class",
        "target_refs",
        "canonical_semantic_mutation",
        "physical_erasure",
        "cross_tenant",
        "permission_change",
    }:
        issues.append("effect_scope must contain the exact bounded fields")
    if spec is not None and effect.get("surface_class") != spec[0]:
        issues.append("surface_class does not match operation_class")
    if not _unique_nonempty_strings(effect.get("target_refs")):
        issues.append("effect target_refs must be non-empty and unique")
    for forbidden in (
        "canonical_semantic_mutation",
        "physical_erasure",
        "cross_tenant",
        "permission_change",
    ):
        if effect.get(forbidden) is not False:
            issues.append(f"{forbidden} must remain false")

    if set(transaction) != {
        "next_version",
        "commit_mode",
        "deadline_at",
        "max_attempts",
        "backoff_seconds",
        "cancellation_token",
    }:
        issues.append("transaction must contain exact retry and cancellation fields")
    if isinstance(object_version, int) and transaction.get("next_version") != (
        object_version + 1
    ):
        issues.append("next_version must advance expected version by exactly one")
    if transaction.get("commit_mode") != "recoverable":
        issues.append("Phase 10 reference plan must use recoverable commit")
    max_attempts = transaction.get("max_attempts")
    backoff = transaction.get("backoff_seconds")
    if not isinstance(max_attempts, int) or not 1 <= max_attempts <= 5:
        issues.append("max_attempts must be between one and five")
    elif (
        not isinstance(backoff, list)
        or len(backoff) != max_attempts - 1
        or any(not isinstance(value, int) or value < 0 for value in backoff)
        or backoff != sorted(backoff)
    ):
        issues.append("backoff_seconds must be monotonic and match max_attempts")
    if not isinstance(transaction.get("cancellation_token"), str) or not transaction.get(
        "cancellation_token"
    ):
        issues.append("cancellation_token must be non-empty")

    if set(compensation) != {
        "strategy",
        "target_version",
        "target_semantic_digest",
        "action_class",
    }:
        issues.append("compensation must contain the exact repair fields")
    if compensation.get("strategy") not in {
        "rollback",
        "forward_repair",
        "rollback_or_forward_repair",
    }:
        issues.append("compensation strategy is invalid")
    if compensation.get("target_version") != object_version:
        issues.append("compensation target_version must pin the predecessor")
    if compensation.get("target_semantic_digest") != subject.get("semantic_digest"):
        issues.append("compensation must preserve the semantic digest")

    if set(receipt_contract) != {
        "commit_receipt_ref",
        "audit_receipt_ref",
        "partial_status",
        "success_requires_audit",
    }:
        issues.append("receipt_contract must contain exact commit/audit fields")
    if receipt_contract.get("partial_status") != "partial_pending_repair":
        issues.append("partial work must remain partial_pending_repair")
    if receipt_contract.get("success_requires_audit") is not True:
        issues.append("success must require an audit receipt")
    if receipt_contract.get("commit_receipt_ref") == receipt_contract.get(
        "audit_receipt_ref"
    ):
        issues.append("commit and audit receipt refs must remain distinct")

    if operation_class == "explicit_ephemeral_ttl" and subject.get(
        "explicit_ephemeral"
    ) is not True:
        issues.append("explicit_ephemeral_ttl requires an explicitly ephemeral subject")
    if operation_class in {
        "projection_invalidation",
        "projection_rebuild",
        "generation_rollover",
    } and subject.get("disposable") is not True:
        issues.append("projection maintenance requires a disposable subject")
    approval_ref = preconditions.get("owner_approval_ref")
    if operation_class == "owner_approved_archive_deadline":
        if not isinstance(approval_ref, str) or not approval_ref:
            issues.append("archive deadline requires an exact owner approval ref")
    elif approval_ref is not None:
        issues.append("owner approval ref is reserved for archive deadline")
    if operation_class == "obsolete_derived_artifact_removal" and effect.get(
        "surface_class"
    ) != "derived_artifact":
        issues.append("ordinary deletion may target only an obsolete derived artifact")

    if plan.get("content_digest") != normalized_digest(plan):
        issues.append("mechanical plan normalized digest mismatch")
    return issues


def build_semantic_lifecycle_proposal(
    *,
    proposal_id: str,
    idempotency_key: str,
    operation_class: str,
    subject_pin: Mapping[str, Any],
    evidence_refs: Sequence[str],
    field_paths: Sequence[str],
    before_digest: str,
    proposed_digest: str,
    rationale: str,
    queue_position: int,
    max_open_items: int,
    generated_at: str,
) -> dict[str, Any]:
    if operation_class not in SEMANTIC_SPECS:
        raise ValueError("operation_class is not a semantic proposal class")
    admitted = queue_position <= max_open_items
    proposal = {
        "schema_version": "aoa_memo_semantic_lifecycle_proposal_v0",
        "proposal_id": proposal_id,
        "idempotency_key": idempotency_key,
        "owner": "aoa-memo",
        "decision_ref": DECISION_REF,
        "operation_class": operation_class,
        "forgetting_class": SEMANTIC_SPECS[operation_class],
        "subject_pin": dict(subject_pin),
        "evidence_refs": list(evidence_refs),
        "proposed_diff": {
            "field_paths": list(field_paths),
            "before_digest": before_digest,
            "proposed_digest": proposed_digest,
            "rationale": rationale,
        },
        "operator_review": {
            "required": True,
            "operator_ref": "operator:sole",
            "decision_ref": None,
            "state": "pending",
        },
        "attention_budget": {
            "queue_position": queue_position,
            "max_open_items": max_open_items,
            "admitted": admitted,
        },
        "proposal_state": (
            "pending_operator" if admitted else "deferred_attention_budget"
        ),
        "generated_at": generated_at,
        "content_digest": ZERO_DIGEST,
        "apply_allowed": False,
        "execution_posture": "proposal_only",
        "semantic_authority": "proposal_only",
    }
    proposal["content_digest"] = normalized_digest(proposal)
    issues = validate_semantic_lifecycle_proposal(proposal)
    if issues:
        raise ValueError("; ".join(issues))
    return proposal


def validate_semantic_lifecycle_proposal(
    proposal: Mapping[str, Any],
) -> list[str]:
    issues = _shape_issues(
        proposal,
        required=PROPOSAL_FIELDS,
        label="semantic proposal",
    )
    expected_literals = {
        "schema_version": "aoa_memo_semantic_lifecycle_proposal_v0",
        "owner": "aoa-memo",
        "decision_ref": DECISION_REF,
        "apply_allowed": False,
        "execution_posture": "proposal_only",
        "semantic_authority": "proposal_only",
    }
    for field, expected in expected_literals.items():
        if proposal.get(field) != expected:
            issues.append(f"{field} must remain {expected!r}")
    operation = proposal.get("operation_class")
    expected_forgetting = SEMANTIC_SPECS.get(str(operation))
    if expected_forgetting is None:
        issues.append("operation_class is not in the semantic proposal allowlist")
    elif proposal.get("forgetting_class") != expected_forgetting:
        issues.append("semantic proposal forgetting_class mismatch")
    if proposal.get("operation_class") in {
        "privacy_erasure",
        "ordinary_deletion",
        "model_unlearning",
    }:
        issues.append("deletion, privacy erasure, and unlearning require other owners")

    if not _unique_nonempty_strings(proposal.get("evidence_refs")):
        issues.append("semantic proposal evidence_refs must be non-empty and unique")
    proposed_diff = _mapping(proposal.get("proposed_diff"))
    if set(proposed_diff) != {
        "field_paths",
        "before_digest",
        "proposed_digest",
        "rationale",
    }:
        issues.append("proposed_diff must contain exact bounded diff fields")
    if not _unique_nonempty_strings(proposed_diff.get("field_paths")):
        issues.append("proposed diff field_paths must be non-empty and unique")

    review = _mapping(proposal.get("operator_review"))
    if review != {
        "required": True,
        "operator_ref": "operator:sole",
        "decision_ref": None,
        "state": "pending",
    }:
        issues.append("semantic proposal must remain pending sole-operator review")

    budget = _mapping(proposal.get("attention_budget"))
    queue_position = budget.get("queue_position")
    max_open = budget.get("max_open_items")
    if (
        not isinstance(queue_position, int)
        or queue_position < 1
        or not isinstance(max_open, int)
        or not 1 <= max_open <= 20
    ):
        issues.append("attention budget values are outside the bounded range")
    else:
        admitted = queue_position <= max_open
        if budget.get("admitted") is not admitted:
            issues.append("attention budget admitted flag is inconsistent")
        expected_state = (
            "pending_operator" if admitted else "deferred_attention_budget"
        )
        if proposal.get("proposal_state") != expected_state:
            issues.append("proposal_state must reflect the attention budget")
    if _aware_datetime(proposal.get("generated_at")) is None:
        issues.append("generated_at must be timezone-aware")
    if proposal.get("content_digest") != normalized_digest(proposal):
        issues.append("semantic proposal normalized digest mismatch")
    return issues


def event_digest(event: Mapping[str, Any]) -> str:
    normalized = dict(event)
    normalized.pop("event_digest", None)
    return canonical_digest(normalized)


def build_audit_event(
    *,
    sequence: int,
    event_type: str,
    previous_event_digest: str | None,
    payload_digest: str,
) -> dict[str, Any]:
    event = {
        "sequence": sequence,
        "event_type": event_type,
        "previous_event_digest": previous_event_digest,
        "payload_digest": payload_digest,
        "event_digest": ZERO_DIGEST,
    }
    event["event_digest"] = event_digest(event)
    return event


def build_lifecycle_execution_receipt(
    *,
    receipt_id: str,
    plan: Mapping[str, Any],
    runtime_owner: str,
    attempt: int,
    status: str,
    observed_prior_version: int,
    result_version: int,
    belief_commit_id: str | None,
    canonical_commit_applied: bool,
    new_effect_applied: bool,
    projection_posture: str,
    compensation_state: str,
    event_chain: Sequence[Mapping[str, Any]],
    semantic_digest_after: str,
    tenant_after: str,
    namespace_after: str,
    produced_at: str,
) -> dict[str, Any]:
    subject = _mapping(plan["subject_pin"])
    receipt_contract = _mapping(plan["receipt_contract"])
    receipt = {
        "schema_version": "aoa_memo_lifecycle_execution_receipt_v0",
        "receipt_id": receipt_id,
        "plan_ref": {
            "plan_id": plan["plan_id"],
            "plan_digest": plan["content_digest"],
        },
        "idempotency_key": plan["idempotency_key"],
        "runtime_owner": runtime_owner,
        "attempt": attempt,
        "status": status,
        "expected_prior_version": plan["preconditions"]["expected_prior_version"],
        "observed_prior_version": observed_prior_version,
        "result_version": result_version,
        "belief_commit_id": belief_commit_id,
        "canonical_commit_applied": canonical_commit_applied,
        "new_effect_applied": new_effect_applied,
        "projection_posture": projection_posture,
        "compensation_state": compensation_state,
        "event_chain": [dict(event) for event in event_chain],
        "commit_receipt_ref": receipt_contract["commit_receipt_ref"],
        "audit_receipt_ref": receipt_contract["audit_receipt_ref"],
        "semantic_digest_before": subject["semantic_digest"],
        "semantic_digest_after": semantic_digest_after,
        "tenant_before": subject["tenant_id"],
        "tenant_after": tenant_after,
        "namespace_before": subject["namespace_id"],
        "namespace_after": namespace_after,
        "partial_is_success": False,
        "produced_at": produced_at,
        "content_digest": ZERO_DIGEST,
        "execution_authority": "reference_lab_only",
    }
    receipt["content_digest"] = normalized_digest(receipt)
    issues = validate_lifecycle_execution_receipt(receipt)
    if issues:
        raise ValueError("; ".join(issues))
    return receipt


def validate_lifecycle_execution_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    issues = _shape_issues(
        receipt,
        required=RECEIPT_FIELDS,
        label="lifecycle receipt",
    )
    if receipt.get("schema_version") != "aoa_memo_lifecycle_execution_receipt_v0":
        issues.append("receipt schema_version mismatch")
    if receipt.get("execution_authority") != "reference_lab_only":
        issues.append("execution_authority must remain reference_lab_only")
    if receipt.get("partial_is_success") is not False:
        issues.append("partial_is_success must remain false")
    statuses = {
        "applied",
        "duplicate",
        "rejected_stale",
        "rejected_conflict",
        "rejected_reordered",
        "rejected_idempotency",
        "cancelled",
        "partial_pending_repair",
        "failed_retryable",
        "compensated",
        "forward_repaired",
    }
    status = receipt.get("status")
    if status not in statuses:
        issues.append("unknown lifecycle receipt status")
    if not isinstance(receipt.get("attempt"), int) or receipt.get("attempt", 0) < 1:
        issues.append("attempt must be a positive integer")
    if receipt.get("semantic_digest_before") != receipt.get("semantic_digest_after"):
        issues.append("mechanical receipt changed semantic digest")
    if receipt.get("tenant_before") != receipt.get("tenant_after"):
        issues.append("mechanical receipt changed tenant")
    if receipt.get("namespace_before") != receipt.get("namespace_after"):
        issues.append("mechanical receipt changed namespace")
    if status == "partial_pending_repair":
        if (
            receipt.get("canonical_commit_applied") is not True
            or receipt.get("projection_posture") != "invalidated_pending_repair"
            or receipt.get("compensation_state") != "pending_forward_repair"
        ):
            issues.append("partial receipt must expose committed canonical state and repair")
    if status == "duplicate" and receipt.get("new_effect_applied") is not False:
        issues.append("duplicate receipt cannot claim a new effect")
    if status in {
        "rejected_stale",
        "rejected_conflict",
        "rejected_reordered",
        "rejected_idempotency",
        "cancelled",
        "failed_retryable",
    } and receipt.get("canonical_commit_applied") is not False:
        issues.append("rejected/cancelled/retryable receipt cannot claim commit")
    if status in {"rejected_stale", "rejected_conflict"} and receipt.get(
        "result_version"
    ) != receipt.get("observed_prior_version"):
        issues.append("stale/conflict rejection must preserve observed version")

    events = receipt.get("event_chain")
    if not isinstance(events, list) or not events:
        issues.append("event_chain must be non-empty")
    else:
        previous = None
        for expected_sequence, event in enumerate(events):
            if not isinstance(event, Mapping):
                issues.append("event_chain entries must be objects")
                continue
            if event.get("sequence") != expected_sequence:
                issues.append("event_chain sequence is not contiguous")
            if event.get("previous_event_digest") != previous:
                issues.append("event_chain previous digest mismatch")
            if event.get("event_digest") != event_digest(event):
                issues.append("event_chain event digest mismatch")
            previous = event.get("event_digest")

    if _aware_datetime(receipt.get("produced_at")) is None:
        issues.append("produced_at must be timezone-aware")
    if receipt.get("commit_receipt_ref") == receipt.get("audit_receipt_ref"):
        issues.append("commit and audit receipt refs must remain distinct")
    if receipt.get("content_digest") != normalized_digest(receipt):
        issues.append("lifecycle receipt normalized digest mismatch")
    return issues
