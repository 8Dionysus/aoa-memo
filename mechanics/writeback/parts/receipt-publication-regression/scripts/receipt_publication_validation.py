from __future__ import annotations

from typing import Any

from receipt_publication_common import (
    ALLOWED_EVENT_KINDS,
    EXPECTED_ACTOR_BY_EVENT_KIND,
    GROWTH_LANE_REF_PREFIX,
    RECALL_SURFACE_PREFIX,
    ReceiptPublishError,
)


def validate_memo_writeback_receipt(
    *,
    location: str,
    object_id: str,
    payload: dict[str, Any],
    evidence_ref_values: list[str],
    memory_objects_by_id: dict[str, dict[str, Any]],
    runtime_targets_by_surface: dict[str, dict[str, Any]],
) -> None:
    catalog_entry = memory_objects_by_id.get(object_id)
    if catalog_entry is None:
        raise ReceiptPublishError(
            f"{location}.object_ref.id: {object_id!r} does not resolve in generated memory-object recall catalog"
        )

    recall_ref = f"{RECALL_SURFACE_PREFIX}{object_id}"
    if recall_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: must include adopted recall surface ref {recall_ref!r}"
        )

    for field in ("target_kind", "writeback_class", "review_state"):
        if not isinstance(payload.get(field), str) or not payload[field]:
            raise ReceiptPublishError(f"{location}.payload.{field}: must be a non-empty string")

    memory_object_ref = payload.get("memory_object_ref")
    if memory_object_ref is not None:
        if not isinstance(memory_object_ref, str) or not memory_object_ref:
            raise ReceiptPublishError(f"{location}.payload.memory_object_ref: must be a non-empty string")
        if memory_object_ref != catalog_entry.get("source_path"):
            raise ReceiptPublishError(
                f"{location}.payload.memory_object_ref: must match adopted memory object source_path "
                f"{catalog_entry.get('source_path')!r}"
            )
    if payload["target_kind"] != catalog_entry.get("kind"):
        raise ReceiptPublishError(
            f"{location}.payload.target_kind: must match adopted memory object kind "
            f"{catalog_entry.get('kind')!r}"
        )
    if payload["review_state"] != catalog_entry.get("review_state"):
        raise ReceiptPublishError(
            f"{location}.payload.review_state: must match adopted memory object review_state "
            f"{catalog_entry.get('review_state')!r}"
        )

    if payload["writeback_class"] != "reviewed_candidate":
        return

    runtime_surface = payload.get("runtime_surface")
    if not isinstance(runtime_surface, str) or not runtime_surface:
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: reviewed_candidate receipts must include a non-empty runtime_surface"
        )
    runtime_target = runtime_targets_by_surface.get(runtime_surface)
    if runtime_target is None:
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: unknown runtime writeback surface {runtime_surface!r}"
        )
    if runtime_target.get("writeback_class") != "reviewed_candidate":
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: {runtime_surface!r} must resolve to a reviewed_candidate mapping"
        )
    if runtime_target.get("target_kind") != payload["target_kind"]:
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: {runtime_surface!r} must resolve to target_kind "
            f"{payload['target_kind']!r}"
        )
    writeback_anchor_ref = payload.get("writeback_anchor_ref")
    if not isinstance(writeback_anchor_ref, str) or not writeback_anchor_ref:
        raise ReceiptPublishError(
            f"{location}.payload.writeback_anchor_ref: reviewed_candidate receipts must include a non-empty writeback_anchor_ref"
        )
    if writeback_anchor_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: reviewed_candidate receipts must include writeback anchor ref {writeback_anchor_ref!r}"
        )
    if memory_object_ref is None:
        raise ReceiptPublishError(
            f"{location}.payload.memory_object_ref: reviewed_candidate receipts must include adopted memory object source_path"
        )


def validate_growth_writeback_receipt(
    *,
    location: str,
    object_id: str,
    payload: dict[str, Any],
    evidence_ref_values: list[str],
    growth_lanes_by_ref: dict[str, dict[str, Any]],
) -> None:
    for field in ("growth_lane_ref", "target_kind", "writeback_class", "review_status", "source_example_ref"):
        if not isinstance(payload.get(field), str) or not payload[field]:
            raise ReceiptPublishError(f"{location}.payload.{field}: must be a non-empty string")

    lane_ref = payload["growth_lane_ref"]
    lane = growth_lanes_by_ref.get(lane_ref)
    if lane is None:
        raise ReceiptPublishError(
            f"{location}.payload.growth_lane_ref: unknown growth refinery writeback lane {lane_ref!r}"
        )
    if object_id != lane.get("memory_id"):
        raise ReceiptPublishError(
            f"{location}.object_ref.id: must match lane memory_id {lane.get('memory_id')!r}"
        )
    if payload["target_kind"] != lane.get("target_kind"):
        raise ReceiptPublishError(
            f"{location}.payload.target_kind: must match lane target_kind {lane.get('target_kind')!r}"
        )
    if payload["writeback_class"] != lane.get("writeback_class"):
        raise ReceiptPublishError(
            f"{location}.payload.writeback_class: must match lane writeback_class {lane.get('writeback_class')!r}"
        )
    if payload["review_status"] != lane.get("review_status"):
        raise ReceiptPublishError(
            f"{location}.payload.review_status: must match lane review_status {lane.get('review_status')!r}"
        )
    if payload["source_example_ref"] != lane.get("source_path"):
        raise ReceiptPublishError(
            f"{location}.payload.source_example_ref: must match lane source_path {lane.get('source_path')!r}"
        )

    primary_ref = lane.get("primary_ref")
    if not isinstance(primary_ref, str) or primary_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: must include primary support ref {primary_ref!r}"
        )
    expected_lane_ref = f"{GROWTH_LANE_REF_PREFIX}{lane_ref}"
    if expected_lane_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: must include growth lane ref {expected_lane_ref!r}"
        )

    required_evidence_refs = lane.get("required_evidence_refs")
    if not isinstance(required_evidence_refs, list):
        raise ReceiptPublishError(
            f"{location}.payload.growth_lane_ref: lane {lane_ref!r} must expose required_evidence_refs"
        )
    for required_ref in required_evidence_refs:
        if required_ref not in evidence_ref_values:
            raise ReceiptPublishError(
                f"{location}.evidence_refs: must include required growth-refinery evidence ref {required_ref!r}"
            )


def validate_receipt(
    receipt: dict[str, Any],
    *,
    location: str,
    memory_objects_by_id: dict[str, dict[str, Any]],
    runtime_targets_by_surface: dict[str, dict[str, Any]],
    growth_lanes_by_ref: dict[str, dict[str, Any]],
) -> None:
    required_fields = (
        "event_kind",
        "event_id",
        "observed_at",
        "run_ref",
        "session_ref",
        "actor_ref",
        "object_ref",
        "evidence_refs",
        "payload",
    )
    for field in required_fields:
        if field not in receipt:
            raise ReceiptPublishError(f"{location}: missing field {field!r}")

    event_kind = receipt["event_kind"]
    if event_kind not in ALLOWED_EVENT_KINDS:
        raise ReceiptPublishError(
            f"{location}.event_kind: unsupported memo receipt kind {event_kind!r}"
        )
    actor_ref = receipt["actor_ref"]
    if not isinstance(actor_ref, str) or not actor_ref:
        raise ReceiptPublishError(f"{location}.actor_ref: must be a non-empty string")
    expected_actor_ref = EXPECTED_ACTOR_BY_EVENT_KIND[event_kind]
    if actor_ref != expected_actor_ref:
        raise ReceiptPublishError(
            f"{location}.actor_ref: {event_kind!r} receipts must use actor_ref {expected_actor_ref!r}"
        )
    if not isinstance(receipt["event_id"], str) or not receipt["event_id"]:
        raise ReceiptPublishError(f"{location}.event_id: must be a non-empty string")

    object_ref = receipt["object_ref"]
    if not isinstance(object_ref, dict):
        raise ReceiptPublishError(f"{location}.object_ref: must be an object")
    if object_ref.get("repo") != "aoa-memo":
        raise ReceiptPublishError(f"{location}.object_ref.repo: must equal 'aoa-memo'")
    object_id = object_ref.get("id")
    if not isinstance(object_id, str) or not object_id:
        raise ReceiptPublishError(f"{location}.object_ref.id: must be a non-empty string")

    evidence_refs = receipt["evidence_refs"]
    if not isinstance(evidence_refs, list) or not evidence_refs:
        raise ReceiptPublishError(f"{location}.evidence_refs: must be a list")
    evidence_ref_values: list[str] = []
    for index, evidence_ref in enumerate(evidence_refs):
        if not isinstance(evidence_ref, dict):
            raise ReceiptPublishError(f"{location}.evidence_refs[{index}]: must be an object")
        ref = evidence_ref.get("ref")
        if not isinstance(ref, str) or not ref:
            raise ReceiptPublishError(f"{location}.evidence_refs[{index}].ref: must be a non-empty string")
        evidence_ref_values.append(ref)

    payload = receipt["payload"]
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{location}.payload: must be an object")

    object_kind = object_ref.get("kind")
    if event_kind == "memo_writeback_receipt":
        if object_kind != "memory_object":
            raise ReceiptPublishError(f"{location}.object_ref.kind: must equal 'memory_object'")
        validate_memo_writeback_receipt(
            location=location,
            object_id=object_id,
            payload=payload,
            evidence_ref_values=evidence_ref_values,
            memory_objects_by_id=memory_objects_by_id,
            runtime_targets_by_surface=runtime_targets_by_surface,
        )
        return

    if object_kind != "support_memory":
        raise ReceiptPublishError(f"{location}.object_ref.kind: must equal 'support_memory'")
    validate_growth_writeback_receipt(
        location=location,
        object_id=object_id,
        payload=payload,
        evidence_ref_values=evidence_ref_values,
        growth_lanes_by_ref=growth_lanes_by_ref,
    )
