#!/usr/bin/env python3
"""Generate object-facing aoa-memo surfaces from curated memory-object examples."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from validate_memo import local_ref_error, validator_for

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"
SCHEMAS = ROOT / "schemas"

SOURCE_OF_TRUTH = "aoa-memo-object-example-surfaces-v1"
MANIFEST_PATH = EXAMPLES / "memory_object_surface_manifest.json"
FULL_CATALOG_PATH = GENERATED / "memory_object_catalog.json"
MIN_CATALOG_PATH = GENERATED / "memory_object_catalog.min.json"
CAPSULES_PATH = GENERATED / "memory_object_capsules.json"
SECTIONS_PATH = GENERATED / "memory_object_sections.full.json"
EXPORTABLE_RECALL_STATUSES = {"preferred", "allowed"}
SECTION_SPECS = [
    ("identity-and-recall", "Identity and Recall"),
    ("provenance-and-evidence", "Provenance and Evidence"),
    ("trust-and-lifecycle", "Trust and Lifecycle"),
    ("bridges-and-access", "Bridges and Access"),
]

JsonDict = dict[str, Any]


def load_json(path: Path) -> JsonDict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: JsonDict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fail(label: str, errors: list[str]) -> None:
    print(f"[FAIL] {label}")
    for err in errors:
        print(f"  - {err}")
    raise SystemExit(1)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def short_list(values: list[str]) -> str:
    return ", ".join(values) if values else "none"


def first_nonempty(values: list[str]) -> str:
    for value in values:
        if isinstance(value, str) and value:
            return value
    return ""


def clean_sentence_fragment(value: str) -> str:
    return value.rstrip().rstrip(".")


def shipped_kinds() -> set[str]:
    schema = load_json(SCHEMAS / "memory_object.schema.json")
    return set(schema["properties"]["kind"]["enum"])


def object_reference_fields(memory_object: JsonDict) -> list[tuple[str, list[str]]]:
    provenance = memory_object.get("provenance", {})
    lifecycle = memory_object.get("lifecycle", {})
    current_recall = lifecycle.get("current_recall", {})

    scalar_refs = []
    if isinstance(lifecycle.get("superseded_by"), str):
        scalar_refs.append(("lifecycle.superseded_by", [lifecycle["superseded_by"]]))
    if isinstance(current_recall.get("replacement_ref"), str):
        scalar_refs.append(("lifecycle.current_recall.replacement_ref", [current_recall["replacement_ref"]]))

    list_refs = [
        ("provenance.episode_refs", provenance.get("episode_refs", [])),
        ("lifecycle.supersedes", lifecycle.get("supersedes", [])),
        ("lifecycle.current_recall.contradiction_refs", current_recall.get("contradiction_refs", [])),
    ]
    return list_refs + scalar_refs


def strongest_next_sources(memory_object: JsonDict) -> list[str]:
    provenance = memory_object.get("provenance", {})
    bridges = memory_object.get("bridges", {})
    candidates = dedupe(list(provenance.get("source_refs", [])))
    if candidates:
        return candidates[:3]
    route_capsule_ref = bridges.get("route_capsule_ref")
    if isinstance(route_capsule_ref, str) and route_capsule_ref:
        return [route_capsule_ref]
    return []


def strongest_next_source(memory_object: JsonDict, source_path: str) -> str:
    candidates = strongest_next_sources(memory_object)
    fallback = [
        memory_object.get("bridges", {}).get("route_capsule_ref"),
        memory_object.get("payload_ref"),
        source_path,
    ]
    return first_nonempty(candidates + [value for value in fallback if isinstance(value, str)])


def related_object_ids(memory_object: JsonDict, curated_ids: set[str]) -> list[str]:
    ordered: list[str] = []
    for _, refs in object_reference_fields(memory_object):
        for ref in refs:
            if ref in curated_ids and ref not in ordered:
                ordered.append(ref)
    return ordered


def catalog_item(
    memory_object: JsonDict,
    source_path: str,
    recall_modes: list[str],
    curated_ids: set[str],
    *,
    include_full: bool,
) -> JsonDict:
    trust = memory_object["trust"]
    lifecycle = memory_object["lifecycle"]
    item: JsonDict = {
        "id": memory_object["id"],
        "kind": memory_object["kind"],
        "title": memory_object["title"],
        "summary": memory_object["summary"],
        "temperature": trust["temperature"],
        "review_state": lifecycle["review_state"],
        "current_recall_status": lifecycle["current_recall"]["status"],
        "authority_kind": trust["authority_kind"],
        "primary_recall_modes": recall_modes,
        "source_path": source_path,
        "inspect_key": memory_object["id"],
        "expand_key": memory_object["id"],
    }
    if include_full:
        item.update(
            {
                "scope": memory_object["scope"],
                "provenance_thread_id": memory_object.get("provenance", {}).get("provenance_thread_id"),
                "related_object_ids": related_object_ids(memory_object, curated_ids),
                "strongest_next_sources": strongest_next_sources(memory_object),
            }
        )
    return item


def recall_posture_short(memory_object: JsonDict) -> str:
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    return (
        f"{current_recall['status']} current recall; "
        f"{lifecycle['review_state']} review state; "
        f"{clean_sentence_fragment(current_recall['status_reason'])}"
    )


def trust_posture_short(memory_object: JsonDict) -> str:
    trust = memory_object["trust"]
    return (
        f"{trust['temperature']} temperature; "
        f"{trust['authority_kind']} authority; "
        f"confidence {trust['confidence']:.2f}; "
        f"freshness {trust['freshness']:.2f}"
    )


def use_when_short(memory_object: JsonDict, recall_modes: list[str]) -> str:
    lifecycle = memory_object["lifecycle"]
    status = lifecycle["current_recall"]["status"]
    kind = memory_object["kind"]
    if status == "preferred":
        return f"Use as the current {kind} surface for {short_list(recall_modes)} recall."
    if status == "allowed":
        return f"Use when {kind}-level recall is needed and this object remains allowed for {short_list(recall_modes)}."
    if status == "historical":
        return f"Use only for trace-back or replacement history around this {kind}."
    return f"Inspect only when auditing why this {kind} was withdrawn."


def do_not_use_short(memory_object: JsonDict) -> str:
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    kind = memory_object["kind"]
    if current_recall["status"] == "withdrawn":
        return f"Do not treat this {kind} as current memo meaning."
    if current_recall["status"] == "historical":
        return f"Do not use this {kind} as the default current entrypoint."
    return f"Do not treat this {kind} as proof or stronger than its cited sources."


def capsules_item(memory_object: JsonDict, source_path: str, recall_modes: list[str]) -> JsonDict:
    return {
        "id": memory_object["id"],
        "kind": memory_object["kind"],
        "title": memory_object["title"],
        "summary": memory_object["summary"],
        "recall_posture_short": recall_posture_short(memory_object),
        "trust_posture_short": trust_posture_short(memory_object),
        "use_when_short": use_when_short(memory_object, recall_modes),
        "do_not_use_short": do_not_use_short(memory_object),
        "strongest_next_source": strongest_next_source(memory_object, source_path),
        "source_path": source_path,
    }


def identity_summary(memory_object: JsonDict, recall_modes: list[str]) -> tuple[str, str]:
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    summary = (
        f"Names the {memory_object['kind']} surface, its active recall modes, "
        f"and its {current_recall['status']} current-recall posture."
    )
    payload_ref = memory_object.get("payload_ref")
    payload_text = f" Payload ref: {payload_ref}." if isinstance(payload_ref, str) and payload_ref else ""
    body = (
        f"{memory_object['title']}. {memory_object['summary']} "
        f"Scope: {short_list(memory_object['scope'])}. "
        f"Primary recall modes: {short_list(recall_modes)}. "
        f"Current recall status: {current_recall['status']} because "
        f"{clean_sentence_fragment(current_recall['status_reason'])}.{payload_text}"
    )
    return summary, body


def provenance_summary(memory_object: JsonDict, curated_ids: set[str]) -> tuple[str, str]:
    provenance = memory_object["provenance"]
    sources = strongest_next_sources(memory_object)
    related_ids = related_object_ids(memory_object, curated_ids)
    summary = "Preserves source refs, provenance thread linkage, and related curated object ids for backward walk."
    body = (
        f"Provenance thread: {provenance.get('provenance_thread_id') or 'none'}. "
        f"Source refs: {short_list(list(provenance.get('source_refs', [])))}. "
        f"Episode refs: {short_list(list(provenance.get('episode_refs', [])))}. "
        f"Related curated object ids: {short_list(related_ids)}. "
        f"Strongest next sources: {short_list(sources)}."
    )
    return summary, body


def trust_summary(memory_object: JsonDict) -> tuple[str, str]:
    trust = memory_object["trust"]
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    freeze_basis = lifecycle.get("freeze_basis", {})
    freeze_text = ""
    if freeze_basis:
        freeze_text = (
            f" Freeze basis: {short_list(list(freeze_basis.get('qualifies_by', [])))}"
            f"{'; ' + clean_sentence_fragment(freeze_basis['note']) if freeze_basis.get('note') else ''}."
        )
    body = (
        f"Authority kind: {trust['authority_kind']} ({trust['authority']}). "
        f"Temperature: {trust['temperature']}; confidence {trust['confidence']:.2f}; "
        f"freshness {trust['freshness']:.2f}; salience {trust['salience']:.2f}. "
        f"Review state: {lifecycle['review_state']}. "
        f"Retention class: {lifecycle['retention_class']}. "
        f"Promotion state: {lifecycle.get('promotion_state', 'none')}. "
        f"Supersedes: {short_list(list(lifecycle.get('supersedes', [])))}. "
        f"Superseded by: {lifecycle.get('superseded_by') or 'none'}. "
        f"Replacement ref: {current_recall.get('replacement_ref') or 'none'}. "
        f"Contradiction refs: {short_list(list(current_recall.get('contradiction_refs', [])))}.{freeze_text}"
    )
    summary = "Summarizes trust posture, lifecycle posture, and contradiction or replacement visibility."
    return summary, body


def bridges_summary(memory_object: JsonDict, source_path: str) -> tuple[str, str]:
    bridges = memory_object.get("bridges", {})
    access = memory_object.get("access", {})
    summary = "Collects access posture, route capsule, and outward bridge refs without turning memory into routing policy."
    body = (
        f"Access class: {access.get('access_class', 'none')}. "
        f"Read scopes: {short_list(list(access.get('read_scopes', [])))}. "
        f"Write scopes: {short_list(list(access.get('write_scopes', [])))}. "
        f"Promotion scopes: {short_list(list(access.get('promotion_scopes', [])))}. "
        f"Route capsule ref: {bridges.get('route_capsule_ref') or source_path}. "
        f"ToS refs: {short_list(list(bridges.get('tos_refs', [])))}. "
        f"Skill refs: {short_list(list(bridges.get('skill_refs', [])))}. "
        f"Eval refs: {short_list(list(bridges.get('eval_refs', [])))}. "
        f"KAG lift status: {bridges.get('kag_lift_status', 'none')}."
    )
    return summary, body


def sections_item(memory_object: JsonDict, source_path: str, recall_modes: list[str], curated_ids: set[str]) -> JsonDict:
    builders = [
        identity_summary(memory_object, recall_modes),
        provenance_summary(memory_object, curated_ids),
        trust_summary(memory_object),
        bridges_summary(memory_object, source_path),
    ]
    sections = []
    for index, ((section_key, heading), (summary, body)) in enumerate(zip(SECTION_SPECS, builders), start=1):
        sections.append(
            {
                "section_id": f"{memory_object['id']}#{section_key}",
                "heading": heading,
                "ordinal": index,
                "summary": summary,
                "body": body,
            }
        )
    return {
        "id": memory_object["id"],
        "kind": memory_object["kind"],
        "title": memory_object["title"],
        "source_path": source_path,
        "sections": sections,
    }


def validate_manifest() -> JsonDict:
    validator = validator_for("memory_object_surface_manifest.schema.json")
    manifest = load_json(MANIFEST_PATH)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(manifest), key=lambda err: list(err.absolute_path))
    ]
    if errors:
        fail(MANIFEST_PATH.name, errors)
    return manifest


def validate_example_refs(memory_object: JsonDict, source_path: str) -> list[str]:
    errors: list[str] = []
    ref_checks: list[tuple[str, object]] = [("payload_ref", memory_object.get("payload_ref"))]
    for index, value in enumerate(memory_object.get("provenance", {}).get("source_refs", [])):
        ref_checks.append((f"provenance.source_refs[{index}]", value))
    ref_checks.append(("bridges.route_capsule_ref", memory_object.get("bridges", {}).get("route_capsule_ref")))
    for label, value in ref_checks:
        error = local_ref_error(value, f"{source_path}:{label}")
        if error:
            errors.append(error)
    return errors


def load_curated_objects(manifest: JsonDict) -> list[tuple[str, list[str], JsonDict]]:
    validator = validator_for("memory_object.schema.json")
    allowed_kinds = shipped_kinds()
    seen_paths: set[str] = set()
    seen_ids: set[str] = set()
    curated: list[tuple[str, list[str], JsonDict]] = []
    errors: list[str] = []

    for entry in manifest["entries"]:
        source_path = entry["example_path"]
        if source_path in seen_paths:
            errors.append(f"duplicate manifest example_path: {source_path}")
            continue
        seen_paths.add(source_path)
        example_path = ROOT / source_path
        if not example_path.exists():
            errors.append(f"manifest example_path does not exist: {source_path}")
            continue
        memory_object = load_json(example_path)
        validation_errors = [
            f"{source_path}:{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
            for err in sorted(validator.iter_errors(memory_object), key=lambda err: list(err.absolute_path))
        ]
        if validation_errors:
            errors.extend(validation_errors)
            continue
        object_id = memory_object["id"]
        if object_id in seen_ids:
            errors.append(f"duplicate memory object id in manifest set: {object_id}")
            continue
        seen_ids.add(object_id)
        if memory_object["kind"] not in allowed_kinds:
            errors.append(f"{source_path}: object kind {memory_object['kind']} is outside the shipped canon")
        errors.extend(validate_example_refs(memory_object, source_path))
        curated.append((source_path, list(entry["recall_modes"]), memory_object))

    if errors:
        fail("curated memory object manifest", errors)
    return curated


def validate_internal_object_refs(curated: list[tuple[str, list[str], JsonDict]]) -> None:
    curated_ids = {memory_object["id"] for _, _, memory_object in curated}
    errors: list[str] = []

    for source_path, _, memory_object in curated:
        for label, refs in object_reference_fields(memory_object):
            for ref in refs:
                if ref not in curated_ids:
                    errors.append(f"{source_path}:{label} references missing curated object id {ref}")

    if errors:
        fail("curated object references", errors)


def build_surface_family() -> dict[str, JsonDict]:
    manifest = validate_manifest()
    curated = load_curated_objects(manifest)
    validate_internal_object_refs(curated)

    curated_ids = {memory_object["id"] for _, _, memory_object in curated}
    full_items = [
        catalog_item(memory_object, source_path, recall_modes, curated_ids, include_full=True)
        for source_path, recall_modes, memory_object in curated
    ]
    min_items = [
        catalog_item(memory_object, source_path, recall_modes, curated_ids, include_full=False)
        for source_path, recall_modes, memory_object in curated
        if memory_object["lifecycle"]["current_recall"]["status"] in EXPORTABLE_RECALL_STATUSES
    ]
    capsules = [
        capsules_item(memory_object, source_path, recall_modes)
        for source_path, recall_modes, memory_object in curated
    ]
    sections = [
        sections_item(memory_object, source_path, recall_modes, curated_ids)
        for source_path, recall_modes, memory_object in curated
    ]

    return {
        "memory_object_catalog.json": {
            "catalog_version": 1,
            "catalog_kind": "full",
            "source_of_truth": SOURCE_OF_TRUTH,
            "memory_objects": full_items,
        },
        "memory_object_catalog.min.json": {
            "catalog_version": 1,
            "catalog_kind": "min",
            "source_of_truth": SOURCE_OF_TRUTH,
            "memory_objects": min_items,
        },
        "memory_object_capsules.json": {
            "capsule_version": 1,
            "source_of_truth": SOURCE_OF_TRUTH,
            "memory_objects": capsules,
        },
        "memory_object_sections.full.json": {
            "sections_version": 1,
            "source_of_truth": SOURCE_OF_TRUTH,
            "memory_objects": sections,
        },
    }


def main() -> int:
    outputs = build_surface_family()
    write_json(FULL_CATALOG_PATH, outputs[FULL_CATALOG_PATH.name])
    write_json(MIN_CATALOG_PATH, outputs[MIN_CATALOG_PATH.name])
    write_json(CAPSULES_PATH, outputs[CAPSULES_PATH.name])
    write_json(SECTIONS_PATH, outputs[SECTIONS_PATH.name])
    for path in (FULL_CATALOG_PATH, MIN_CATALOG_PATH, CAPSULES_PATH, SECTIONS_PATH):
        print(f"[OK]   wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
