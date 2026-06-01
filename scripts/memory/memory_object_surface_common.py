from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"
MEMO_OBJECTS = ROOT / "memo" / "objects"
GENERATED = ROOT / "generated"
SCHEMAS = ROOT / "schemas"

SOURCE_OF_TRUTH = "aoa-memo-object-read-models-v2"
EXAMPLE_MANIFEST_SOURCE = "aoa-memo-object-example-surfaces-v1"
SOURCE_KIND_REVIEWED_CORPUS = "reviewed_corpus"
SOURCE_KIND_TEACHING_FIXTURE = "teaching_fixture"
MANIFEST_PATH = EXAMPLES / "generated-surfaces" / "memory_object_surface_manifest.json"
FULL_CATALOG_PATH = GENERATED / "memory-objects" / "memory_object_catalog.json"
MIN_CATALOG_PATH = GENERATED / "memory-objects" / "memory_object_catalog.min.json"
CAPSULES_PATH = GENERATED / "memory-objects" / "memory_object_capsules.json"
SECTIONS_PATH = GENERATED / "memory-objects" / "memory_object_sections.full.json"
EXPORTABLE_RECALL_STATUSES = {"preferred", "allowed"}
SECTION_SPECS = [
    ("identity-and-recall", "Identity and Recall"),
    ("provenance-and-evidence", "Provenance and Evidence"),
    ("trust-and-lifecycle", "Trust and Lifecycle"),
    ("bridges-and-access", "Bridges and Access"),
]

JsonDict = dict[str, Any]
SourceObject = tuple[str, list[str], JsonDict, str]

CORPUS_RECALL_MODES_BY_KIND = {
    "anchor": ["semantic", "source_route", "lineage"],
    "state_capsule": ["working", "episodic", "source_route"],
    "episode": ["episodic", "working", "source_route"],
    "claim": ["semantic", "source_route"],
    "decision": ["semantic", "source_route", "lineage"],
    "pattern": ["semantic", "procedural", "lineage"],
    "bridge": ["lineage", "source_route"],
    "audit_event": ["episodic", "lineage", "source_route"],
}

SHARED_SCOPE_CLASSES = ("thread", "session", "repo", "project", "workspace", "ecosystem")


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
    schema = load_json(SCHEMAS / "memory-objects" / "memory_object.schema.json")
    return set(schema["properties"]["kind"]["enum"])


def scope_class_from_identifier(scope_identifier: str) -> str:
    prefix, separator, _ = scope_identifier.partition(":")
    scope_class = prefix if separator else scope_identifier
    if scope_class not in SHARED_SCOPE_CLASSES:
        raise ValueError(f"unsupported scope class '{scope_class}' from scope identifier '{scope_identifier}'")
    return scope_class


def scope_classes_for(memory_object: JsonDict) -> list[str]:
    return dedupe([scope_class_from_identifier(scope_identifier) for scope_identifier in memory_object["scope"]])


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
