#!/usr/bin/env python3
"""Validate object-facing aoa-memo generated surfaces and recall contracts."""

from __future__ import annotations

from pathlib import Path
import sys

from generate_memory_object_surfaces import (
    EXPORTABLE_RECALL_STATUSES,
    FULL_CATALOG_PATH,
    MIN_CATALOG_PATH,
    CAPSULES_PATH,
    SECTIONS_PATH,
    MANIFEST_PATH,
    SECTION_SPECS,
    build_surface_family,
    load_json,
)
from validate_memo import local_ref_error, validator_for

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def validate_schema(path: Path, schema_name: str) -> dict:
    validator = validator_for(schema_name)
    data = load_json(path)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    if errors:
        raise SystemExit(f"{path}: " + "; ".join(errors))
    return data


def ensure_exists(path_text: str, label: str) -> None:
    if not isinstance(path_text, str) or not path_text:
        raise SystemExit(f"{label}: invalid path")
    if not (ROOT / path_text).exists():
        raise SystemExit(f"{label}: missing path {path_text}")


def validate_full_catalog(data: dict, curated_ids: set[str]) -> None:
    seen_ids: set[str] = set()
    for item in data["memory_objects"]:
        if item["id"] in seen_ids:
            raise SystemExit(f"{FULL_CATALOG_PATH}: duplicate id {item['id']}")
        seen_ids.add(item["id"])
        ensure_exists(item["source_path"], f"{FULL_CATALOG_PATH}:{item['id']}:source_path")
        if item["inspect_key"] != item["id"] or item["expand_key"] != item["id"]:
            raise SystemExit(f"{FULL_CATALOG_PATH}: {item['id']} inspect_key and expand_key must match the object id")
        for ref in item.get("strongest_next_sources", []):
            error = local_ref_error(ref, f"{FULL_CATALOG_PATH}:{item['id']}:strongest_next_sources")
            if error:
                raise SystemExit(error)
        for ref in item.get("related_object_ids", []):
            if ref not in curated_ids:
                raise SystemExit(f"{FULL_CATALOG_PATH}: {item['id']} related_object_ids must stay inside the curated set")

    if seen_ids != curated_ids:
        missing = sorted(curated_ids - seen_ids)
        extra = sorted(seen_ids - curated_ids)
        raise SystemExit(f"{FULL_CATALOG_PATH}: curated set mismatch (missing={missing}, extra={extra})")


def validate_min_catalog(data: dict, expected_ids: set[str]) -> None:
    seen_ids: set[str] = set()
    for item in data["memory_objects"]:
        if item["id"] in seen_ids:
            raise SystemExit(f"{MIN_CATALOG_PATH}: duplicate id {item['id']}")
        seen_ids.add(item["id"])
        ensure_exists(item["source_path"], f"{MIN_CATALOG_PATH}:{item['id']}:source_path")
        if item["current_recall_status"] not in EXPORTABLE_RECALL_STATUSES:
            raise SystemExit(f"{MIN_CATALOG_PATH}: {item['id']} must not appear with current_recall_status={item['current_recall_status']}")
    if seen_ids != expected_ids:
        missing = sorted(expected_ids - seen_ids)
        extra = sorted(seen_ids - expected_ids)
        raise SystemExit(f"{MIN_CATALOG_PATH}: current-facing set mismatch (missing={missing}, extra={extra})")


def validate_capsules(data: dict, curated_ids: set[str]) -> None:
    ids = set()
    for item in data["memory_objects"]:
        ids.add(item["id"])
        ensure_exists(item["source_path"], f"{CAPSULES_PATH}:{item['id']}:source_path")
        error = local_ref_error(item["strongest_next_source"], f"{CAPSULES_PATH}:{item['id']}:strongest_next_source")
        if error:
            raise SystemExit(error)
    if ids != curated_ids:
        missing = sorted(curated_ids - ids)
        extra = sorted(ids - curated_ids)
        raise SystemExit(f"{CAPSULES_PATH}: curated set mismatch (missing={missing}, extra={extra})")


def validate_sections(data: dict, curated_ids: set[str]) -> None:
    ids = set()
    expected_section_keys = [key for key, _ in SECTION_SPECS]
    expected_headings = [heading for _, heading in SECTION_SPECS]
    for item in data["memory_objects"]:
        ids.add(item["id"])
        ensure_exists(item["source_path"], f"{SECTIONS_PATH}:{item['id']}:source_path")
        section_ids = [section["section_id"] for section in item["sections"]]
        headings = [section["heading"] for section in item["sections"]]
        ordinals = [section["ordinal"] for section in item["sections"]]
        if ordinals != [1, 2, 3, 4]:
            raise SystemExit(f"{SECTIONS_PATH}: {item['id']} must keep deterministic ordinals 1..4")
        if headings != expected_headings:
            raise SystemExit(f"{SECTIONS_PATH}: {item['id']} headings must stay {expected_headings}")
        expected_ids = [f"{item['id']}#{section_key}" for section_key in expected_section_keys]
        if section_ids != expected_ids:
            raise SystemExit(f"{SECTIONS_PATH}: {item['id']} section ids must stay {expected_ids}")
    if ids != curated_ids:
        missing = sorted(curated_ids - ids)
        extra = sorted(ids - curated_ids)
        raise SystemExit(f"{SECTIONS_PATH}: curated set mismatch (missing={missing}, extra={extra})")


def validate_contradictions_and_replacements(manifest_data: dict) -> tuple[set[str], set[str]]:
    curated_ids: set[str] = set()
    current_ids: set[str] = set()
    contradiction_pairs: set[tuple[str, str]] = set()
    memory_validator = validator_for("memory_object.schema.json")

    for entry in manifest_data["entries"]:
        source_path = entry["example_path"]
        data = load_json(ROOT / source_path)
        errors = [
            f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
            for err in sorted(memory_validator.iter_errors(data), key=lambda err: list(err.absolute_path))
        ]
        if errors:
            raise SystemExit(f"{source_path}: " + "; ".join(errors))

        curated_ids.add(data["id"])
        lifecycle = data["lifecycle"]
        current_recall = lifecycle["current_recall"]
        if current_recall["status"] in EXPORTABLE_RECALL_STATUSES:
            current_ids.add(data["id"])
        if lifecycle["review_state"] == "superseded" and not current_recall.get("replacement_ref"):
            raise SystemExit(f"{source_path}: superseded object must keep lifecycle.current_recall.replacement_ref")
        for ref in current_recall.get("contradiction_refs", []):
            contradiction_pairs.add((data["id"], ref))

    for left, right in contradiction_pairs:
        if (right, left) not in contradiction_pairs:
            raise SystemExit(f"contradiction links must be symmetric: {left} -> {right} is missing the reverse link")

    return curated_ids, current_ids


def validate_recall_contract(
    path: Path,
    *,
    expected_mode: str,
    expected_allowed_scopes: list[str],
    expected_preferred_kinds: list[str],
    expected_temperature_order: list[str],
    expected_source_route_required: bool,
    expected_capsule_surface: str | None = None,
) -> None:
    validator = validator_for("recall_contract.schema.json")
    data = load_json(path)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    for label in ("inspect_surface", "capsule_surface", "expand_surface"):
        error = local_ref_error(data.get(label), label)
        if error:
            errors.append(error)
    if data.get("mode") != expected_mode:
        errors.append(f"mode must stay '{expected_mode}'")
    if data.get("allowed_scopes") != expected_allowed_scopes:
        errors.append(f"allowed_scopes must stay {expected_allowed_scopes}")
    if data.get("preferred_kinds") != expected_preferred_kinds:
        errors.append(f"preferred_kinds must stay {expected_preferred_kinds}")
    if data.get("temperature_order") != expected_temperature_order:
        errors.append(f"temperature_order must stay {expected_temperature_order}")
    if data.get("inspect_surface") != "generated/memory_object_catalog.min.json":
        errors.append("inspect_surface must stay generated/memory_object_catalog.min.json")
    if expected_capsule_surface is not None and data.get("capsule_surface") != expected_capsule_surface:
        errors.append(f"capsule_surface must stay {expected_capsule_surface}")
    if data.get("expand_surface") != "generated/memory_object_sections.full.json":
        errors.append("expand_surface must stay generated/memory_object_sections.full.json")
    if data.get("source_route_required") is not expected_source_route_required:
        errors.append(f"source_route_required must stay {expected_source_route_required}")
    if errors:
        raise SystemExit(f"{path}: " + "; ".join(errors))


def validate_determinism() -> None:
    expected = build_surface_family()
    actual = {
        FULL_CATALOG_PATH.name: load_json(FULL_CATALOG_PATH),
        MIN_CATALOG_PATH.name: load_json(MIN_CATALOG_PATH),
        CAPSULES_PATH.name: load_json(CAPSULES_PATH),
        SECTIONS_PATH.name: load_json(SECTIONS_PATH),
    }
    for name, expected_data in expected.items():
        if actual[name] != expected_data:
            raise SystemExit(f"{name}: checked-in output drifted from generator output")


def main() -> int:
    manifest_data = validate_schema(MANIFEST_PATH, "memory_object_surface_manifest.schema.json")
    curated_ids, current_ids = validate_contradictions_and_replacements(manifest_data)

    full_catalog = validate_schema(FULL_CATALOG_PATH, "memory_object_catalog.schema.json")
    min_catalog = validate_schema(MIN_CATALOG_PATH, "memory_object_catalog.schema.json")
    capsules = validate_schema(CAPSULES_PATH, "memory_object_capsules.schema.json")
    sections = validate_schema(SECTIONS_PATH, "memory_object_sections.schema.json")

    validate_full_catalog(full_catalog, curated_ids)
    validate_min_catalog(min_catalog, current_ids)
    validate_capsules(capsules, curated_ids)
    validate_sections(sections, curated_ids)
    validate_recall_contract(
        EXAMPLES / "recall_contract.object.working.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_source_route_required=False,
    )
    validate_recall_contract(
        EXAMPLES / "recall_contract.object.working.phase-alpha.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_source_route_required=False,
        expected_capsule_surface="generated/memory_object_capsules.json",
    )
    validate_recall_contract(
        EXAMPLES / "recall_contract.object.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_source_route_required=True,
        expected_capsule_surface="generated/memory_object_capsules.json",
    )
    validate_recall_contract(
        EXAMPLES / "recall_contract.object.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_source_route_required=True,
        expected_capsule_surface="generated/memory_object_capsules.json",
    )
    validate_determinism()
    print("Object-facing memo surfaces validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
