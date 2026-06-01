"""Runtime policy and degradation-boundary validation profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403
from .runtime_receipts import validate_live_receipt_log
from .runtime_writeback import (
    validate_growth_refinery_writeback_lanes,
    validate_phase_alpha_writeback_map,
    validate_runtime_writeback_governance,
    validate_runtime_writeback_intake,
    validate_runtime_writeback_targets,
)

def validate_self_agency_continuity_writeback_surface() -> None:
    readme = load_text(ROOT / "README.md")
    thread = load_json(example_path_for(SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE))
    return_contract = load_json(example_path_for("recall_contract.object.working.return.json"))
    catalog = load_json(GENERATED / "memory-objects" / "memory_object_catalog.min.json")
    capsules = load_json(GENERATED / "memory-objects" / "memory_object_capsules.json")
    sections = load_json(GENERATED / "memory-objects" / "memory_object_sections.full.json")
    errors: list[str] = []

    if "mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md" not in readme:
        errors.append("README.md must route mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md")
    if thread.get("writeback_target") != "provenance_thread":
        errors.append(
            f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} must write back as a provenance_thread"
        )
    for key in ("continuity_ref", "revision_window_ref", "reanchor_ref", "anchor_artifact_ref"):
        value = thread.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} must keep non-empty {key}")

    source_refs = thread.get("source_refs")
    if not isinstance(source_refs, list):
        source_refs = []
        errors.append(f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} must keep source_refs as a list")
    missing_source_refs = [
        ref for ref in SELF_AGENCY_CONTINUITY_REQUIRED_SOURCE_REFS if ref not in source_refs
    ]
    if missing_source_refs:
        errors.append(
            f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} is missing required source_refs: "
            + ", ".join(missing_source_refs)
        )

    if return_contract.get("return_ready") is not True:
        errors.append("recall_contract.object.working.return.json must stay return_ready for continuity relaunch")
    preferred_kinds = return_contract.get("preferred_kinds")
    if not isinstance(preferred_kinds, list):
        preferred_kinds = []
        errors.append("recall_contract.object.working.return.json preferred_kinds must be a list")
    for kind in ("state_capsule", "decision"):
        if kind not in preferred_kinds:
            errors.append(f"recall_contract.object.working.return.json must prefer {kind} for continuity relaunch")

    catalog_entries_by_id = {
        item["id"]: item
        for item in catalog.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    capsule_entries_by_id = {
        item["id"]: item
        for item in capsules.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    section_entries_by_id = {
        item["id"]: item
        for item in sections.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    memory_object_ids = thread.get("memory_object_ids")
    if not isinstance(memory_object_ids, list) or not memory_object_ids:
        errors.append(
            f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} must keep non-empty memory_object_ids"
        )
        memory_object_ids = []

    missing_expected_ids = [
        object_id
        for object_id in SELF_AGENCY_CONTINUITY_EXPECTED_OBJECT_PATHS
        if object_id not in memory_object_ids
    ]
    if missing_expected_ids:
        errors.append(
            f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} is missing continuity memory_object_ids: "
            + ", ".join(missing_expected_ids)
        )

    for object_id in memory_object_ids:
        if not isinstance(object_id, str) or not object_id:
            errors.append(
                f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} memory_object_ids must contain non-empty strings"
            )
            continue
        catalog_entry = catalog_entries_by_id.get(object_id)
        capsule_entry = capsule_entries_by_id.get(object_id)
        section_entry = section_entries_by_id.get(object_id)
        if catalog_entry is None:
            errors.append(
                f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} memory_object_id {object_id!r} "
                "is absent from generated/memory-objects/memory_object_catalog.min.json"
            )
            continue
        expected_path = SELF_AGENCY_CONTINUITY_EXPECTED_OBJECT_PATHS.get(object_id)
        if expected_path is not None and catalog_entry.get("source_path") != expected_path:
            errors.append(
                f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} memory_object_id {object_id!r} "
                f"must surface from {expected_path}"
            )
        if capsule_entry is None:
            errors.append(
                f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} memory_object_id {object_id!r} "
                "is absent from generated/memory-objects/memory_object_capsules.json"
            )
        else:
            if capsule_entry.get("kind") != catalog_entry.get("kind"):
                errors.append(
                    f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} capsule kind for {object_id!r} "
                    "must match generated/memory-objects/memory_object_catalog.min.json"
                )
            if capsule_entry.get("source_path") != catalog_entry.get("source_path"):
                errors.append(
                    f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} capsule source_path for {object_id!r} "
                    "must match generated/memory-objects/memory_object_catalog.min.json"
                )
        if section_entry is None:
            errors.append(
                f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} memory_object_id {object_id!r} "
                "is absent from generated/memory-objects/memory_object_sections.full.json"
            )
        else:
            if section_entry.get("kind") != catalog_entry.get("kind"):
                errors.append(
                    f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} section kind for {object_id!r} "
                    "must match generated/memory-objects/memory_object_catalog.min.json"
                )
            if section_entry.get("source_path") != catalog_entry.get("source_path"):
                errors.append(
                    f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} section source_path for {object_id!r} "
                    "must match generated/memory-objects/memory_object_catalog.min.json"
                )
            if not section_entry.get("sections"):
                errors.append(
                    f"{SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE} section entry for {object_id!r} "
                    "must include expanded sections"
                )

    if errors:
        print("[FAIL] self-agency continuity writeback surface")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   self-agency continuity writeback surface")

def run() -> None:
    validate_runtime_writeback_targets()
    validate_runtime_writeback_intake()
    validate_runtime_writeback_governance()
    validate_growth_refinery_writeback_lanes()
    validate_live_receipt_log()
    validate_phase_alpha_writeback_map()
    validate_self_agency_continuity_writeback_surface()
