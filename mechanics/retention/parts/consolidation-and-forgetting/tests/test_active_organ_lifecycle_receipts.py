from __future__ import annotations

from copy import deepcopy
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
    build_audit_event,
    build_lifecycle_execution_receipt,
    build_mechanical_lifecycle_plan,
    validate_lifecycle_execution_receipt,
)


RECEIPT_SCHEMA = (
    PART_ROOT
    / "schemas"
    / "active_organ_lifecycle_execution_receipt_v0.schema.json"
)


def plan(operation_class: str) -> dict:
    disposable = operation_class in {
        "projection_invalidation",
        "projection_rebuild",
        "generation_rollover",
    }
    return build_mechanical_lifecycle_plan(
        plan_id=f"lifecycle-plan:phase10:{operation_class}",
        idempotency_key=f"idempotency:phase10:{operation_class}",
        operation_class=operation_class,
        subject_pin={
            "owner_repo": "aoa-memo",
            "object_ref": f"memory:phase10:{operation_class}",
            "object_version": 1,
            "lifecycle_state": "active",
            "semantic_digest": "sha256:" + ("1" * 64),
            "tenant_id": "owner-local",
            "namespace_id": "agent:phase10",
            "source_generation": 7,
            "explicit_ephemeral": operation_class == "explicit_ephemeral_ttl",
            "disposable": disposable,
        },
        policy_pin={
            "policy_id": "policy:active-organ:mechanical-lifecycle",
            "policy_version": "phase10-v0",
            "policy_digest": "sha256:" + ("2" * 64),
            "decision_ref": DECISION_REF,
            "status": "accepted",
            "approved_operation_classes": list(MECHANICAL_SPECS),
        },
        effect_owner_repo="aoa-kag" if disposable else "abyss-stack",
        target_refs=[f"target:phase10:{operation_class}"],
        eligible_at="2026-07-29T12:00:00Z",
        deadline_at="2026-07-29T13:00:00Z",
        max_attempts=3,
        backoff_seconds=[1, 5],
        cancellation_token=f"cancel:phase10:{operation_class}",
        owner_approval_ref=None,
        compensation_strategy="rollback_or_forward_repair",
        compensation_action_class="restore_or_rebuild_exact_predecessor",
        commit_receipt_ref=f"receipt:commit:phase10:{operation_class}",
        audit_receipt_ref=f"receipt:audit:phase10:{operation_class}",
        generated_at="2026-07-29T11:59:00Z",
    )


def receipt(
    operation_class: str,
    *,
    status: str,
    projection_posture: str,
    compensation_state: str,
    event_types: list[str],
) -> tuple[dict, list[dict]]:
    payload = plan(operation_class)
    events = []
    previous = None
    for sequence, event_type in enumerate(event_types):
        event = build_audit_event(
            sequence=sequence,
            event_type=event_type,
            previous_event_digest=previous,
            payload_digest=(
                payload["content_digest"]
                if sequence == 0
                else "sha256:" + (str(sequence + 4) * 64)
            ),
        )
        events.append(event)
        previous = event["event_digest"]
    built = build_lifecycle_execution_receipt(
        receipt_id=f"receipt:phase10:{operation_class}:{status}",
        plan=payload,
        runtime_owner="aoa-evals-reference-lab",
        attempt=1,
        status=status,
        observed_prior_version=1,
        result_version=2,
        belief_commit_id=f"belief-commit:phase10:{operation_class}",
        canonical_commit_applied=True,
        new_effect_applied=True,
        projection_posture=projection_posture,
        compensation_state=compensation_state,
        event_chain=events,
        semantic_digest_after=payload["subject_pin"]["semantic_digest"],
        tenant_after=payload["subject_pin"]["tenant_id"],
        namespace_after=payload["subject_pin"]["namespace_id"],
        produced_at="2026-07-29T12:01:00Z",
    )
    return built, events


def test_execution_receipt_preserves_semantics_scope_and_audit_chain() -> None:
    built, _ = receipt(
        "projection_invalidation",
        status="applied",
        projection_posture="rebuilt_current_generation",
        compensation_state="available",
        event_types=["preconditions_verified", "belief_commit"],
    )
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    assert list(validator.iter_errors(built)) == []
    assert validate_lifecycle_execution_receipt(built) == []
    assert built["commit_receipt_ref"] != built["audit_receipt_ref"]


def test_partial_commit_is_fail_closed_and_not_success() -> None:
    built, _ = receipt(
        "projection_rebuild",
        status="partial_pending_repair",
        projection_posture="invalidated_pending_repair",
        compensation_state="pending_forward_repair",
        event_types=["canonical_commit_projection_pending"],
    )

    assert validate_lifecycle_execution_receipt(built) == []
    assert built["partial_is_success"] is False


def test_reordered_or_tampered_audit_chain_fails_closed() -> None:
    built, events = receipt(
        "queue_cancellation",
        status="applied",
        projection_posture="not_applicable",
        compensation_state="available",
        event_types=["preconditions_verified", "queue_cancelled"],
    )
    reordered = deepcopy(built)
    reordered["event_chain"] = list(reversed(events))

    issues = validate_lifecycle_execution_receipt(reordered)
    assert any("sequence" in issue or "previous digest" in issue for issue in issues)
