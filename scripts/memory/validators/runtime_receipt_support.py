from __future__ import annotations

from ._shared import *  # noqa: F403


def load_receipt_context() -> dict[str, object]:
    catalog = load_json(GENERATED / "memory-objects" / "memory_object_catalog.min.json")
    capsules = load_json(GENERATED / "memory-objects" / "memory_object_capsules.json")
    sections = load_json(GENERATED / "memory-objects" / "memory_object_sections.full.json")
    runtime_targets = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)
    growth_lanes = load_json(GROWTH_REFINERY_WRITEBACK_LANES_PATH)
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
    runtime_targets_by_surface = {
        item["runtime_surface"]: item
        for item in runtime_targets.get("targets", [])
        if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
    }
    growth_lanes_by_ref = {
        item["lane_ref"]: item
        for item in growth_lanes.get("lanes", [])
        if isinstance(item, dict) and isinstance(item.get("lane_ref"), str)
    }
    return {
        "catalog_entries_by_id": catalog_entries_by_id,
        "capsule_entries_by_id": capsule_entries_by_id,
        "section_entries_by_id": section_entries_by_id,
        "runtime_targets_by_surface": runtime_targets_by_surface,
        "growth_lanes_by_ref": growth_lanes_by_ref,
        "catalog_ids": set(catalog_entries_by_id),
        "reviewed_object_cache": {},
    }


def reviewed_corpus_object(context: dict[str, object], catalog_entry: dict) -> dict | None:
    source_path = catalog_entry.get("source_path")
    if catalog_entry.get("source_kind") != "reviewed_corpus" or not isinstance(source_path, str):
        return None
    reviewed_object_cache = context["reviewed_object_cache"]
    assert isinstance(reviewed_object_cache, dict)
    if source_path in reviewed_object_cache:
        return reviewed_object_cache[source_path]
    object_path = ROOT / source_path
    if not object_path.exists():
        return None
    data = load_json(object_path)
    if not isinstance(data, dict):
        return None
    reviewed_object_cache[source_path] = data
    return data


def source_ref_payload(ref: str) -> dict | None:
    ref_path = ref.removeprefix("repo:aoa-memo/") if ref.startswith("repo:aoa-memo/") else ref
    ref_path, _, _ = ref_path.partition("#")
    target = ROOT / ref_path
    if not target.exists() or target.suffix.lower() != ".json":
        return None
    data = load_json(target)
    return data if isinstance(data, dict) else None


def is_reviewed_corpus_source_ref(context: dict[str, object], catalog_entry: dict, ref: object) -> bool:
    if not isinstance(ref, str) or not ref:
        return False
    reviewed_object = reviewed_corpus_object(context, catalog_entry)
    if reviewed_object is None:
        return False
    source_refs = reviewed_object.get("provenance", {}).get("source_refs", [])
    return isinstance(source_refs, list) and ref in source_refs
