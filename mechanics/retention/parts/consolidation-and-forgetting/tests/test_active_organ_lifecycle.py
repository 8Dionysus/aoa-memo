from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker


PART_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PART_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from active_organ_lifecycle import (  # noqa: E402
    DECISION_REF,
    MECHANICAL_SPECS,
    SEMANTIC_SPECS,
    build_mechanical_lifecycle_plan,
    build_semantic_lifecycle_proposal,
    validate_mechanical_lifecycle_plan,
    validate_semantic_lifecycle_proposal,
)


SCHEMAS = {
    "plan": PART_ROOT
    / "schemas"
    / "active_organ_mechanical_lifecycle_plan_v0.schema.json",
    "proposal": PART_ROOT
    / "schemas"
    / "active_organ_semantic_lifecycle_proposal_v0.schema.json",
    "receipt": PART_ROOT
    / "schemas"
    / "active_organ_lifecycle_execution_receipt_v0.schema.json",
}


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def schema_validator(name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS[name])
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def subject(
    operation_class: str,
    *,
    version: int = 1,
) -> dict:
    return {
        "owner_repo": "aoa-memo",
        "object_ref": f"memory:phase10:{operation_class}",
        "object_version": version,
        "lifecycle_state": "active",
        "semantic_digest": "sha256:" + ("1" * 64),
        "tenant_id": "owner-local",
        "namespace_id": "agent:phase10",
        "source_generation": 7,
        "explicit_ephemeral": operation_class == "explicit_ephemeral_ttl",
        "disposable": operation_class
        in {
            "projection_invalidation",
            "projection_rebuild",
            "generation_rollover",
        },
    }


def policy() -> dict:
    return {
        "policy_id": "policy:active-organ:mechanical-lifecycle",
        "policy_version": "phase10-v0",
        "policy_digest": "sha256:" + ("2" * 64),
        "decision_ref": DECISION_REF,
        "status": "accepted",
        "approved_operation_classes": list(MECHANICAL_SPECS),
    }


def plan(operation_class: str, *, version: int = 1) -> dict:
    effect_owner = (
        "aoa-kag"
        if operation_class
        in {
            "projection_invalidation",
            "projection_rebuild",
            "generation_rollover",
        }
        else "abyss-stack"
    )
    return build_mechanical_lifecycle_plan(
        plan_id=f"lifecycle-plan:phase10:{operation_class}:v{version}",
        idempotency_key=f"idempotency:phase10:{operation_class}:v{version}",
        operation_class=operation_class,
        subject_pin=subject(operation_class, version=version),
        policy_pin=policy(),
        effect_owner_repo=effect_owner,
        target_refs=[f"target:phase10:{operation_class}"],
        eligible_at="2026-07-29T12:00:00Z",
        deadline_at="2026-07-29T13:00:00Z",
        max_attempts=3,
        backoff_seconds=[1, 5],
        cancellation_token=f"cancel:phase10:{operation_class}:v{version}",
        owner_approval_ref=(
            "decision:owner:archive-deadline:phase10"
            if operation_class == "owner_approved_archive_deadline"
            else None
        ),
        compensation_strategy="rollback_or_forward_repair",
        compensation_action_class="restore_or_rebuild_exact_predecessor",
        commit_receipt_ref=f"receipt:commit:phase10:{operation_class}:v{version}",
        audit_receipt_ref=f"receipt:audit:phase10:{operation_class}:v{version}",
        generated_at="2026-07-29T11:59:00Z",
    )


def semantic_proposal(
    operation_class: str,
    *,
    queue_position: int = 1,
    max_open_items: int = 3,
) -> dict:
    return build_semantic_lifecycle_proposal(
        proposal_id=f"proposal:phase10:{operation_class}:{queue_position}",
        idempotency_key=f"idempotency:proposal:{operation_class}:{queue_position}",
        operation_class=operation_class,
        subject_pin=subject("queue_cancellation"),
        evidence_refs=["evidence:phase10:source", "evidence:phase10:conflict"],
        field_paths=["lifecycle.state"],
        before_digest="sha256:" + ("3" * 64),
        proposed_digest="sha256:" + ("4" * 64),
        rationale="bounded evidence-linked semantic diff",
        queue_position=queue_position,
        max_open_items=max_open_items,
        generated_at="2026-07-29T12:00:00Z",
    )


def test_all_nine_mechanical_classes_are_strict_and_schema_valid() -> None:
    validator = schema_validator("plan")

    assert len(MECHANICAL_SPECS) == 9
    for operation_class in MECHANICAL_SPECS:
        payload = plan(operation_class)
        assert list(validator.iter_errors(payload)) == []
        assert validate_mechanical_lifecycle_plan(payload) == []
        assert payload["semantic_authority"] == "none"
        assert payload["live_runtime_authority"] is False
        assert payload["effect_scope"]["canonical_semantic_mutation"] is False
        assert payload["effect_scope"]["physical_erasure"] is False


def test_mechanical_allowlist_requires_class_specific_preconditions() -> None:
    ttl = plan("explicit_ephemeral_ttl")
    ttl["subject_pin"]["explicit_ephemeral"] = False
    assert any(
        "explicitly ephemeral" in issue
        for issue in validate_mechanical_lifecycle_plan(ttl)
    )

    archive = plan("owner_approved_archive_deadline")
    archive["preconditions"]["owner_approval_ref"] = None
    assert any(
        "owner approval" in issue
        for issue in validate_mechanical_lifecycle_plan(archive)
    )

    deletion = plan("obsolete_derived_artifact_removal")
    deletion["effect_scope"]["surface_class"] = "canonical_lifecycle"
    assert any(
        "surface_class" in issue or "derived artifact" in issue
        for issue in validate_mechanical_lifecycle_plan(deletion)
    )


def test_unknown_or_semantic_operation_cannot_enter_mechanical_plan() -> None:
    payload = plan("queue_cancellation")
    payload["operation_class"] = "supersession"
    payload["content_digest"] = "sha256:" + ("0" * 64)

    issues = validate_mechanical_lifecycle_plan(payload)
    assert any("mechanical allowlist" in issue for issue in issues)


def test_semantic_classes_stay_proposal_only_and_attention_bounded() -> None:
    validator = schema_validator("proposal")

    assert len(SEMANTIC_SPECS) == 8
    for operation_class in SEMANTIC_SPECS:
        payload = semantic_proposal(operation_class)
        assert list(validator.iter_errors(payload)) == []
        assert validate_semantic_lifecycle_proposal(payload) == []
        assert payload["apply_allowed"] is False
        assert payload["operator_review"]["operator_ref"] == "operator:sole"
        assert payload["proposal_state"] == "pending_operator"

    deferred = semantic_proposal(
        "supersession",
        queue_position=4,
        max_open_items=3,
    )
    assert deferred["attention_budget"]["admitted"] is False
    assert deferred["proposal_state"] == "deferred_attention_budget"


def test_proposal_cannot_self_approve_or_apply() -> None:
    payload = semantic_proposal("retraction")
    payload["apply_allowed"] = True
    payload["operator_review"]["decision_ref"] = "decision:self-approved"
    payload["operator_review"]["state"] = "approved"

    issues = validate_semantic_lifecycle_proposal(payload)
    assert any("apply_allowed" in issue for issue in issues)
    assert any("pending sole-operator" in issue for issue in issues)
