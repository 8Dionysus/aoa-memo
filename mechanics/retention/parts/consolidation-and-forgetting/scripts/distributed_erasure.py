from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from typing import Any


ZERO_DIGEST = "sha256:" + ("0" * 64)
DECISION_REF = (
    "docs/decisions/"
    "AOA-MEM-D-0080-distributed-erasure-requires-walkable-owner-closure.md"
)
SURFACE_CLASSES = {
    "ER0": "canonical_object",
    "ER1": "raw_session_attachment",
    "ER2": "local_memo_port",
    "ER3": "projection",
    "ER4": "runtime",
    "ER5": "backup_restore",
    "ER6": "host_local",
    "ER7": "experiment_replay",
    "ER8": "training_unlearning",
    "ER9": "audit_receipt",
}
SURFACE_MATERIALS = {
    "ER0": frozenset(
        {
            "canonical_object",
            "summary",
            "markdown_read_model",
        }
    ),
    "ER1": frozenset({"authorized_raw_evidence"}),
    "ER2": frozenset({"local_memo_port", "lexical_posting"}),
    "ER3": frozenset(
        {
            "embedding",
            "graph_node_edge",
            "kag_projection",
        }
    ),
    "ER4": frozenset({"runtime_store", "cache", "nervous_index"}),
    "ER5": frozenset({"export", "backup_restore_descendant"}),
    "ER6": frozenset({"host_local_surface"}),
    "ER7": frozenset({"experiment_replay_copy"}),
    "ER8": frozenset(
        {
            "training_dataset",
            "model_checkpoint_or_unlearning_obligation",
        }
    ),
    "ER9": frozenset({"content_minimized_tombstone"}),
}
RACE_REBUILD_REQUIRED = frozenset(
    {"ER2", "ER3", "ER4", "ER5", "ER6", "ER7", "ER8"}
)
PROBE_FIELDS = frozenset(
    {
        "schema_version",
        "probe_id",
        "surface_id",
        "worker_owner",
        "work_item_ref",
        "positive_control",
        "negative_recovery",
        "race_rebuild",
        "probe_storage",
        "performed_at",
        "content_digest",
        "evidence_scope",
        "global_completion_authority",
    }
)
OWNER_EXTENSION_FIELDS = frozenset(
    {
        "schema_version",
        "extension_id",
        "parent_owner",
        "worker_owner",
        "surface_id",
        "work_item_ref",
        "material_classes",
        "target_ref_digests",
        "operation_evidence_refs",
        "recovery_probe_ref",
        "result",
        "residue_refs",
        "retention_exceptions",
        "subject_material_included",
        "content_minimized",
        "execution_posture",
        "live_execution",
        "effect_authority",
        "global_completion_authority",
        "content_digest",
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


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: object, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(isinstance(item, str) and bool(item) for item in value)
        and len(value) == len(set(value))
    )


def _shape_issues(
    payload: Mapping[str, Any],
    *,
    required: frozenset[str],
    label: str,
) -> list[str]:
    issues = []
    if missing := sorted(required - set(payload)):
        issues.append(f"{label} missing fields: {', '.join(missing)}")
    if unknown := sorted(set(payload) - required):
        issues.append(f"{label} unknown fields: {', '.join(unknown)}")
    return issues


def build_erasure_recovery_probe(
    *,
    probe_id: str,
    surface_id: str,
    worker_owner: str,
    work_item_ref: str,
    canary_digest: str,
    positive_match_count: int,
    query_classes: Sequence[str],
    race_rebuild_required: bool,
    race_rebuild_attempted: bool,
    performed_at: str,
) -> dict[str, Any]:
    if surface_id not in SURFACE_CLASSES:
        raise ValueError("unknown erasure surface")
    probe = {
        "schema_version": "aoa_memo_erasure_recovery_probe_v0",
        "probe_id": probe_id,
        "surface_id": surface_id,
        "worker_owner": worker_owner,
        "work_item_ref": work_item_ref,
        "positive_control": {
            "canary_digest": canary_digest,
            "detected_before_erasure": True,
            "matched_count": positive_match_count,
        },
        "negative_recovery": {
            "query_classes": list(query_classes),
            "material_recovered": False,
            "matched_count": 0,
        },
        "race_rebuild": {
            "required": race_rebuild_required,
            "attempted": race_rebuild_attempted,
            "material_recovered": False,
        },
        "probe_storage": {
            "subject_material_included": False,
            "canary_digest_only": True,
            "raw_query_logged": False,
        },
        "performed_at": performed_at,
        "content_digest": ZERO_DIGEST,
        "evidence_scope": "reference_lab_only",
        "global_completion_authority": False,
    }
    probe["content_digest"] = normalized_digest(probe)
    issues = validate_erasure_recovery_probe(probe)
    if issues:
        raise ValueError("; ".join(issues))
    return probe


def validate_erasure_recovery_probe(
    probe: Mapping[str, Any],
) -> list[str]:
    issues = _shape_issues(
        probe,
        required=PROBE_FIELDS,
        label="erasure recovery probe",
    )
    expected = {
        "schema_version": "aoa_memo_erasure_recovery_probe_v0",
        "evidence_scope": "reference_lab_only",
        "global_completion_authority": False,
    }
    for field, value in expected.items():
        if probe.get(field) != value:
            issues.append(f"{field} must remain {value!r}")
    surface_id = probe.get("surface_id")
    if surface_id not in SURFACE_CLASSES:
        issues.append("unknown erasure surface")

    positive = _mapping(probe.get("positive_control"))
    if positive.get("detected_before_erasure") is not True:
        issues.append("positive control must be detected before erasure")
    if (
        not isinstance(positive.get("matched_count"), int)
        or positive.get("matched_count", 0) < 1
    ):
        issues.append("positive control matched_count must be positive")

    negative = _mapping(probe.get("negative_recovery"))
    if not _string_list(negative.get("query_classes"), nonempty=True):
        issues.append("negative recovery query_classes must be unique and non-empty")
    if (
        negative.get("material_recovered") is not False
        or negative.get("matched_count") != 0
    ):
        issues.append("negative recovery must find zero subject material")

    race = _mapping(probe.get("race_rebuild"))
    expected_race = surface_id in RACE_REBUILD_REQUIRED
    if race.get("required") is not expected_race:
        issues.append("race/rebuild required flag does not match surface")
    if expected_race and race.get("attempted") is not True:
        issues.append("required race/rebuild probe was not attempted")
    if race.get("material_recovered") is not False:
        issues.append("race/rebuild probe recovered subject material")

    storage = _mapping(probe.get("probe_storage"))
    if storage != {
        "subject_material_included": False,
        "canary_digest_only": True,
        "raw_query_logged": False,
    }:
        issues.append("recovery probe storage must remain content-minimized")
    if _aware_datetime(probe.get("performed_at")) is None:
        issues.append("performed_at must be timezone-aware")
    if probe.get("content_digest") != normalized_digest(probe):
        issues.append("erasure recovery probe digest mismatch")
    return issues


def validate_owner_erasure_extension(
    extension: Mapping[str, Any],
) -> list[str]:
    issues = []
    if missing := sorted(OWNER_EXTENSION_FIELDS - set(extension)):
        issues.append(
            "owner erasure extension missing fields: " + ", ".join(missing)
        )
    if extension.get("schema_version") != "active_organ_owner_erasure_extension_v0":
        issues.append("owner extension schema_version mismatch")
    if extension.get("surface_id") not in SURFACE_CLASSES:
        issues.append("owner extension has unknown surface")
    if extension.get("subject_material_included") is not False:
        issues.append("owner extension cannot include subject material")
    if extension.get("content_minimized") is not True:
        issues.append("owner extension must remain content-minimized")
    if extension.get("execution_posture") != "reference_lab_only":
        issues.append("owner extension must remain reference_lab_only")
    if extension.get("live_execution") is not False:
        issues.append("owner extension cannot claim live execution")
    if extension.get("effect_authority") != "owner_local_erasure_only":
        issues.append("owner extension effect authority widened")
    if extension.get("global_completion_authority") is not False:
        issues.append("owner extension cannot claim global completion")
    if not _string_list(extension.get("material_classes"), nonempty=True):
        issues.append("owner extension material_classes must be unique and non-empty")
    if not _string_list(extension.get("target_ref_digests"), nonempty=True):
        issues.append("owner extension target_ref_digests must be non-empty")
    if not _string_list(
        extension.get("operation_evidence_refs"),
        nonempty=True,
    ):
        issues.append("owner extension operation evidence must be non-empty")
    if not _string_list(extension.get("residue_refs")):
        issues.append("owner extension residue_refs must be unique strings")
    if not isinstance(extension.get("retention_exceptions"), list):
        issues.append("owner extension retention_exceptions must be a list")
    if extension.get("result") == "erased" and (
        extension.get("residue_refs") != []
        or extension.get("retention_exceptions") != []
    ):
        issues.append("erased owner extension cannot retain residue or exceptions")
    if extension.get("result") in {"residue", "partial", "failed"} and not (
        extension.get("residue_refs") or extension.get("retention_exceptions")
    ):
        issues.append("non-erased owner extension must expose residue or exception")
    if extension.get("content_digest") != normalized_digest(extension):
        issues.append("owner erasure extension digest mismatch")
    return issues


def evaluate_distributed_erasure_closure(
    *,
    request: Mapping[str, Any],
    manifest: Mapping[str, Any],
    work_items: Sequence[Mapping[str, Any]],
    receipts: Sequence[Mapping[str, Any]],
    owner_extensions: Mapping[str, Mapping[str, Any]],
    probes: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Evaluate C14-C17 composition without executing any erasure."""

    issues: list[str] = []
    required_surfaces = set(SURFACE_CLASSES)
    request_scope = _mapping(request.get("scope"))
    request_surfaces = request_scope.get("erase_surface_ids")
    if (
        not isinstance(request_surfaces, list)
        or set(request_surfaces) != required_surfaces
        or len(request_surfaces) != len(required_surfaces)
    ):
        issues.append("C14 scope must cover ER0-ER9 exactly once")
    if request.get("recovery_probe_required") is not True:
        issues.append("C14 must require recovery probes")

    manifest_surfaces_raw = manifest.get("erase_surfaces")
    manifest_surfaces = (
        {
            item.get("surface_id"): item
            for item in manifest_surfaces_raw
            if isinstance(item, Mapping)
        }
        if isinstance(manifest_surfaces_raw, list)
        else {}
    )
    if set(manifest_surfaces) != required_surfaces or len(
        manifest_surfaces
    ) != len(required_surfaces):
        issues.append("C15 manifest must expose ER0-ER9 exactly once")
    for surface_id, surface in manifest_surfaces.items():
        if surface.get("surface_class") != SURFACE_CLASSES.get(surface_id):
            issues.append(f"{surface_id} surface class mismatch")

    work_by_ref = {
        item.get("work_item_id"): item
        for item in work_items
        if isinstance(item, Mapping)
    }
    receipt_by_work = {
        item.get("work_item_ref"): item
        for item in receipts
        if isinstance(item, Mapping)
    }
    if len(work_by_ref) != len(work_items):
        issues.append("work items must have unique refs")
    if len(receipt_by_work) != len(receipts):
        issues.append("receipts must cover work items exactly once")
    if set(manifest.get("work_item_refs", [])) != set(work_by_ref):
        issues.append("manifest work refs do not match C16 work items")
    if set(manifest.get("erase_receipt_refs", [])) != {
        receipt.get("receipt_id") for receipt in receipts
    }:
        issues.append("manifest receipt refs do not match C17 receipts")

    covered_materials: dict[str, set[str]] = {
        surface_id: set() for surface_id in required_surfaces
    }
    residue_present = False
    exceptions_present = False
    every_probe_passed = True
    for surface_id in sorted(required_surfaces):
        surface = manifest_surfaces.get(surface_id, {})
        work_ref = surface.get("work_item_ref")
        work = work_by_ref.get(work_ref)
        if not isinstance(work, Mapping):
            issues.append(f"{surface_id} has no walkable C16 work item")
            continue
        if work.get("manifest_ref") != manifest.get("manifest_id"):
            issues.append(f"{surface_id} work item points to another manifest")
        if work.get("erase_surface_id") != surface_id:
            issues.append(f"{surface_id} work item surface mismatch")
        if work.get("target_owner") != surface.get("owner"):
            issues.append(f"{surface_id} parent worker owner mismatch")

        pin = _mapping(work.get("owner_extension"))
        payload_ref = pin.get("payload_ref")
        extension = owner_extensions.get(str(payload_ref))
        if not isinstance(extension, Mapping):
            issues.append(f"{surface_id} owner extension is not resolvable")
            continue
        extension_issues = validate_owner_erasure_extension(extension)
        issues.extend(f"{surface_id}: {issue}" for issue in extension_issues)
        if pin.get("payload_digest") != extension.get("content_digest"):
            issues.append(f"{surface_id} owner extension digest pin mismatch")
        if (
            extension.get("surface_id") != surface_id
            or extension.get("work_item_ref") != work_ref
            or extension.get("worker_owner") != work.get("target_owner")
        ):
            issues.append(f"{surface_id} owner extension binding mismatch")
        covered_materials[surface_id].update(
            extension.get("material_classes", [])
        )
        missing_materials = (
            SURFACE_MATERIALS[surface_id] - covered_materials[surface_id]
        )
        if missing_materials:
            issues.append(
                f"{surface_id} missing material classes: "
                + ", ".join(sorted(missing_materials))
            )

        receipt = receipt_by_work.get(work_ref)
        if not isinstance(receipt, Mapping):
            issues.append(f"{surface_id} has no walkable C17 receipt")
            continue
        if (
            receipt.get("erase_surface_id") != surface_id
            or receipt.get("receipt_owner") != work.get("target_owner")
            or receipt.get("manifest_ref") != manifest.get("manifest_id")
        ):
            issues.append(f"{surface_id} C17 binding mismatch")
        receipt_pin = _mapping(receipt.get("owner_extension"))
        if receipt_pin.get("payload_ref") != payload_ref:
            issues.append(f"{surface_id} C16/C17 owner extension mismatch")
        if receipt.get("result") != extension.get("result"):
            issues.append(f"{surface_id} receipt/extension result mismatch")

        probe_ref = extension.get("recovery_probe_ref")
        probe = probes.get(str(probe_ref))
        if not isinstance(probe, Mapping):
            issues.append(f"{surface_id} recovery probe is not resolvable")
            every_probe_passed = False
        else:
            probe_issues = validate_erasure_recovery_probe(probe)
            issues.extend(f"{surface_id}: {issue}" for issue in probe_issues)
            if (
                probe.get("surface_id") != surface_id
                or probe.get("work_item_ref") != work_ref
                or probe.get("worker_owner") != work.get("target_owner")
                or probe_ref not in receipt.get("recovery_probe_refs", [])
            ):
                issues.append(f"{surface_id} recovery probe binding mismatch")
                every_probe_passed = False
            if probe_issues:
                every_probe_passed = False

        if receipt.get("result") != "erased":
            residue_present = True
        if receipt.get("residue_refs") or surface.get("surface_state") == "residue":
            residue_present = True
        if receipt.get("retention_exceptions") or surface.get(
            "retention_exceptions"
        ):
            exceptions_present = True

        if surface_id == "ER9" and (
            extension.get("material_classes")
            != ["content_minimized_tombstone"]
            or extension.get("subject_material_included") is not False
        ):
            issues.append("ER9 tombstone is not content-minimized")

    completion_state = manifest.get("completion_state")
    if completion_state == "complete":
        if residue_present or exceptions_present:
            issues.append("complete closure cannot contain residue or exceptions")
        if not every_probe_passed:
            issues.append("complete closure requires every recovery probe")
    elif completion_state == "complete_with_approved_exceptions":
        if not exceptions_present:
            issues.append("exception closure requires an explicit exception")
    else:
        residue_present = True

    plain_complete = (
        completion_state == "complete"
        and not residue_present
        and not exceptions_present
        and every_probe_passed
        and not issues
    )
    return {
        "issues": issues,
        "walkable": not any("walkable" in issue for issue in issues),
        "all_surfaces_covered": all(
            SURFACE_MATERIALS[surface_id].issubset(
                covered_materials[surface_id]
            )
            for surface_id in required_surfaces
        ),
        "every_probe_passed": every_probe_passed,
        "plain_complete": plain_complete,
        "residue_present": residue_present,
        "exceptions_present": exceptions_present,
        "private_memory_deployment_allowed": plain_complete,
        "global_completion_authority": "aoa-memo-manifest-review-only",
        "live_execution": False,
    }
