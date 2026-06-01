from __future__ import annotations

from ._shared import *  # noqa: F403


def validate_evidence_refs(
    *,
    receipt: dict,
    line_number: int,
    event_kind: object,
    object_id: object,
    payload: object,
    growth_lane_ref: str | None,
    growth_lane: dict | None,
    context: dict[str, object],
    errors: list[str],
) -> None:
    catalog_ids = context["catalog_ids"]
    growth_lanes_by_ref = context["growth_lanes_by_ref"]
    assert isinstance(catalog_ids, set)
    assert isinstance(growth_lanes_by_ref, dict)

    evidence_refs = receipt.get("evidence_refs")
    if not isinstance(evidence_refs, list):
        errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs must be a list")
        return
    evidence_ref_values: list[str] = []
    for evidence_index, evidence in enumerate(evidence_refs):
        if not isinstance(evidence, dict):
            errors.append(
                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}] must be an object"
            )
            continue
        ref = evidence.get("ref")
        if not isinstance(ref, str) or not ref:
            errors.append(
                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref must be a non-empty string"
            )
            continue
        evidence_ref_values.append(ref)
        validate_local_evidence_ref(
            ref=ref,
            evidence_index=evidence_index,
            line_number=line_number,
            object_id=object_id,
            growth_lane_ref=growth_lane_ref,
            catalog_ids=catalog_ids,
            growth_lanes_by_ref=growth_lanes_by_ref,
            errors=errors,
        )
    validate_required_evidence_refs(
        line_number=line_number,
        event_kind=event_kind,
        object_id=object_id,
        payload=payload,
        growth_lane_ref=growth_lane_ref,
        growth_lane=growth_lane,
        catalog_ids=catalog_ids,
        evidence_ref_values=evidence_ref_values,
        errors=errors,
    )


def validate_local_evidence_ref(
    *,
    ref: str,
    evidence_index: int,
    line_number: int,
    object_id: object,
    growth_lane_ref: str | None,
    catalog_ids: set[str],
    growth_lanes_by_ref: dict[str, dict],
    errors: list[str],
) -> None:
    if not ref.startswith("repo:aoa-memo/"):
        return
    path_text, _, anchor = ref.removeprefix("repo:aoa-memo/").partition("#")
    if any(part in {"", ".", ".."} for part in path_text.split("/")):
        errors.append(
            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref "
            f"must use a normalized repo-relative path: {path_text!r}"
        )
        return
    local_path = (ROOT / path_text).resolve()
    try:
        local_path.relative_to(ROOT_RESOLVED)
    except ValueError:
        errors.append(
            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref "
            f"escapes the repository root: {path_text!r}"
        )
        return
    if not local_path.exists():
        errors.append(
            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref "
            f"points to missing local path {path_text!r}"
        )
        return
    if path_text == "generated/memory-objects/memory_object_catalog.min.json":
        validate_catalog_evidence_anchor(line_number, object_id, anchor, catalog_ids, errors)
    if path_text == "mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json":
        validate_growth_lane_evidence_anchor(line_number, growth_lane_ref, anchor, growth_lanes_by_ref, errors)


def validate_catalog_evidence_anchor(
    line_number: int,
    object_id: object,
    anchor: str,
    catalog_ids: set[str],
    errors: list[str],
) -> None:
    if not anchor:
        errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: catalog evidence ref must include a memory object id anchor")
    elif anchor not in catalog_ids:
        errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: catalog evidence ref points to uncataloged id {anchor!r}")
    elif isinstance(object_id, str) and anchor != object_id:
        errors.append(
            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: catalog evidence id {anchor!r} "
            f"must match object_ref.id {object_id!r}"
        )


def validate_growth_lane_evidence_anchor(
    line_number: int,
    growth_lane_ref: str | None,
    anchor: str,
    growth_lanes_by_ref: dict[str, dict],
    errors: list[str],
) -> None:
    if not anchor:
        errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth lane evidence ref must include a lane anchor")
    elif anchor not in growth_lanes_by_ref:
        errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth lane evidence ref points to unknown lane {anchor!r}")
    elif growth_lane_ref is not None and anchor != growth_lane_ref:
        errors.append(
            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth lane evidence ref {anchor!r} "
            f"must match payload.growth_lane_ref {growth_lane_ref!r}"
        )


def validate_required_evidence_refs(
    *,
    line_number: int,
    event_kind: object,
    object_id: object,
    payload: object,
    growth_lane_ref: str | None,
    growth_lane: dict | None,
    catalog_ids: set[str],
    evidence_ref_values: list[str],
    errors: list[str],
) -> None:
    if event_kind == "memo_writeback_receipt" and isinstance(object_id, str) and object_id in catalog_ids:
        expected_recall_ref = f"{RECALL_SURFACE_PREFIX}{object_id}"
        if expected_recall_ref not in evidence_ref_values:
            errors.append(
                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs must include adopted recall surface ref "
                f"{expected_recall_ref!r}"
            )
        if (
            isinstance(payload, dict)
            and payload.get("writeback_class") == "reviewed_candidate"
            and isinstance(payload.get("writeback_anchor_ref"), str)
            and payload["writeback_anchor_ref"] not in evidence_ref_values
        ):
            errors.append(
                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: reviewed_candidate receipts must include writeback anchor ref "
                f"{payload['writeback_anchor_ref']!r} in evidence_refs"
            )
    if event_kind == "memo_growth_writeback_receipt" and isinstance(growth_lane, dict) and growth_lane_ref is not None:
        primary_ref = growth_lane.get("primary_ref")
        if isinstance(primary_ref, str) and primary_ref not in evidence_ref_values:
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth receipts must include primary support ref {primary_ref!r}")
        expected_lane_ref = f"{GROWTH_LANE_REF_PREFIX}{growth_lane_ref}"
        if expected_lane_ref not in evidence_ref_values:
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth receipts must include lane ref {expected_lane_ref!r}")
        required_refs = growth_lane.get("required_evidence_refs")
        if isinstance(required_refs, list):
            for required_ref in required_refs:
                if required_ref not in evidence_ref_values:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth receipts must include required evidence ref "
                        f"{required_ref!r}"
                    )
