#!/usr/bin/env python3
"""Generate object-facing aoa-memo surfaces from reviewed corpus objects and examples."""

from __future__ import annotations

import argparse
import json
import sys

from memory_object_surface_common import (
    ARTIFACT_IDENTITY,
    CAPSULES_PATH,
    EXPORTABLE_RECALL_STATUSES,
    FULL_CATALOG_PATH,
    MANIFEST_PATH,
    MIN_CATALOG_PATH,
    ROOT,
    SECTION_SPECS,
    SECTIONS_PATH,
    SHARED_SCOPE_CLASSES,
    SOURCE_KIND_REVIEWED_CORPUS,
    SOURCE_KIND_TEACHING_FIXTURE,
    SOURCE_OF_TRUTH,
    JsonDict,
    load_json,
    scope_classes_for,
    write_json,
)
from memory_object_surface_items import catalog_item, capsules_item, sections_item
from memory_object_surface_sources import (
    load_source_objects,
    validate_internal_object_refs,
    validate_manifest,
)


def build_surface_family() -> dict[str, JsonDict]:
    manifest = validate_manifest()
    curated = load_source_objects(manifest)
    validate_internal_object_refs(curated)

    curated_ids = {memory_object["id"] for _, _, memory_object, _ in curated}
    full_items = [
        catalog_item(memory_object, source_path, recall_modes, curated_ids, source_kind=source_kind, include_full=True)
        for source_path, recall_modes, memory_object, source_kind in curated
    ]
    min_items = [
        catalog_item(memory_object, source_path, recall_modes, curated_ids, source_kind=source_kind, include_full=False)
        for source_path, recall_modes, memory_object, source_kind in curated
        if memory_object["lifecycle"]["current_recall"]["status"] in EXPORTABLE_RECALL_STATUSES
    ]
    capsules = [
        capsules_item(memory_object, source_path, recall_modes, source_kind)
        for source_path, recall_modes, memory_object, source_kind in curated
    ]
    sections = [
        sections_item(memory_object, source_path, recall_modes, curated_ids, source_kind)
        for source_path, recall_modes, memory_object, source_kind in curated
    ]

    return {
        "memory_object_catalog.json": {
            "catalog_version": 1,
            "catalog_kind": "full",
            "source_of_truth": SOURCE_OF_TRUTH,
            "artifact_identity": ARTIFACT_IDENTITY,
            "memory_objects": full_items,
        },
        "memory_object_catalog.min.json": {
            "catalog_version": 1,
            "catalog_kind": "min",
            "source_of_truth": SOURCE_OF_TRUTH,
            "artifact_identity": ARTIFACT_IDENTITY,
            "memory_objects": min_items,
        },
        "memory_object_capsules.json": {
            "capsule_version": 1,
            "source_of_truth": SOURCE_OF_TRUTH,
            "artifact_identity": ARTIFACT_IDENTITY,
            "memory_objects": capsules,
        },
        "memory_object_sections.full.json": {
            "sections_version": 1,
            "source_of_truth": SOURCE_OF_TRUTH,
            "artifact_identity": ARTIFACT_IDENTITY,
            "memory_objects": sections,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate object-facing aoa-memo surfaces from curated examples."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="check that generated memory-object surfaces are current",
    )
    args = parser.parse_args()

    outputs = build_surface_family()
    output_paths = (FULL_CATALOG_PATH, MIN_CATALOG_PATH, CAPSULES_PATH, SECTIONS_PATH)
    if args.check:
        issues: list[str] = []
        for path in output_paths:
            expected = json.dumps(outputs[path.name], indent=2) + "\n"
            if not path.is_file():
                issues.append(f"{path.relative_to(ROOT)} is missing")
                continue
            actual = path.read_text(encoding="utf-8")
            if actual != expected:
                issues.append(f"{path.relative_to(ROOT)} is stale")
        if issues:
            print("[FAIL] generated memory-object surfaces")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        print("[OK]   generated memory-object surfaces are current")
        return 0

    write_json(FULL_CATALOG_PATH, outputs[FULL_CATALOG_PATH.name])
    write_json(MIN_CATALOG_PATH, outputs[MIN_CATALOG_PATH.name])
    write_json(CAPSULES_PATH, outputs[CAPSULES_PATH.name])
    write_json(SECTIONS_PATH, outputs[SECTIONS_PATH.name])
    for path in output_paths:
        print(f"[OK]   wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
