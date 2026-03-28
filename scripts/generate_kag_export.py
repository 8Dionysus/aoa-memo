#!/usr/bin/env python3
"""Generate the source-owned KAG export capsule for aoa-memo."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"

KAG_EXPORT_PATH = GENERATED / "kag_export.min.json"
OBJECT_CAPSULES_PATH = GENERATED / "memory_object_capsules.json"
OBJECT_SECTIONS_PATH = GENERATED / "memory_object_sections.full.json"

BRIDGE_ID = "memo.bridge.2026-03-23.tos-lineage-kag-candidate"
BRIDGE_EXAMPLE_REF = "examples/bridge.kag-lift.example.json"
CLAIM_EXAMPLE_REF = "examples/claim.tos-bridge-ready.example.json"
EPISODE_EXAMPLE_REF = "examples/episode.tos-interpretation.example.json"
TOS_FRAGMENT_REF = "repo:Tree-of-Sophia/docs/CONTEXT_COMPOST.md#memory-bridge-fragment"
SECTION_HANDLES = [
    "identity-and-recall",
    "provenance-and-evidence",
    "trust-and-lifecycle",
    "bridges-and-access",
]
PRIMARY_QUESTION = (
    "How should aoa-memo publish a bridge-bearing memory object for KAG use "
    "without turning memo into graph truth?"
)
SUMMARY_50 = "Source-owned tiny export for a provenance-visible memo bridge."
SUMMARY_200 = (
    "Source-owned tiny export capsule for the current reviewed memo bridge "
    "candidate so aoa-kag can consume one explicit bridge-bearing memory "
    "object by source-owned entry surface rather than by inferred graph "
    "meaning."
)
PROVENANCE_NOTE = (
    "Guide to source, not source replacement, built from the memo-owned bridge "
    "object plus explicit Tree-of-Sophia support refs."
)
NON_IDENTITY_BOUNDARY = (
    "Source-owned memo export for KAG readiness; derived consumers must not "
    "treat this bridge capsule as normalized graph truth, routing authority, "
    "or replacement for Tree-of-Sophia-authored meaning."
)

JsonDict = dict[str, Any]


def load_json(path: Path) -> JsonDict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: JsonDict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fail(message: str) -> None:
    raise RuntimeError(message)


def find_object(payload: JsonDict, *, collection_key: str, object_id: str, label: str) -> JsonDict:
    objects = payload.get(collection_key)
    if not isinstance(objects, list):
        fail(f"{label} must contain a '{collection_key}' list")
    for item in objects:
        if isinstance(item, dict) and item.get("id") == object_id:
            return item
    fail(f"{label} must contain object id '{object_id}'")


def validate_bridge_sections(section_payload: JsonDict) -> None:
    bridge_sections = find_object(
        section_payload,
        collection_key="memory_objects",
        object_id=BRIDGE_ID,
        label=str(OBJECT_SECTIONS_PATH.relative_to(ROOT)),
    )
    sections = bridge_sections.get("sections")
    if not isinstance(sections, list) or len(sections) != len(SECTION_HANDLES):
        fail("bridge section export must keep the four canonical KAG handles")

    actual_handles: list[str] = []
    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            fail(f"bridge sections[{index}] must be an object")
        section_id = section.get("section_id")
        if not isinstance(section_id, str) or "#" not in section_id:
            fail(f"bridge sections[{index}].section_id must be a non-empty section ref")
        actual_handles.append(section_id.split("#", 1)[1])
    if actual_handles != SECTION_HANDLES:
        fail(
            "bridge section export must keep section handles "
            + ", ".join(SECTION_HANDLES)
        )


def build_kag_export_payload() -> JsonDict:
    bridge_example = load_json(EXAMPLES / "bridge.kag-lift.example.json")
    bridge_capsules = load_json(OBJECT_CAPSULES_PATH)
    bridge_sections = load_json(OBJECT_SECTIONS_PATH)

    bridge_capsule = find_object(
        bridge_capsules,
        collection_key="memory_objects",
        object_id=BRIDGE_ID,
        label=str(OBJECT_CAPSULES_PATH.relative_to(ROOT)),
    )
    validate_bridge_sections(bridge_sections)

    if bridge_example.get("id") != BRIDGE_ID:
        fail("bridge example id must stay aligned with the KAG export donor id")
    if bridge_example.get("kind") != "bridge":
        fail("bridge example kind must stay 'bridge'")
    if bridge_capsule.get("id") != BRIDGE_ID:
        fail("bridge capsule id must stay aligned with the KAG export donor id")

    return {
        "owner_repo": "aoa-memo",
        "kind": "bridge",
        "object_id": BRIDGE_ID,
        "primary_question": PRIMARY_QUESTION,
        "summary_50": SUMMARY_50,
        "summary_200": SUMMARY_200,
        "source_inputs": [
            {
                "repo": "aoa-memo",
                "source_class": "memo_object",
                "role": "primary",
            },
            {
                "repo": "Tree-of-Sophia",
                "source_class": "tos_text",
                "role": "supporting",
            },
        ],
        "entry_surface": {
            "repo": "aoa-memo",
            "path": "generated/memory_object_capsules.json",
            "match_key": "id",
            "match_value": BRIDGE_ID,
        },
        "section_handles": list(SECTION_HANDLES),
        "direct_relations": [
            {
                "relation_type": "supported_by_claim",
                "target_ref": CLAIM_EXAMPLE_REF,
            },
            {
                "relation_type": "seeded_by_episode",
                "target_ref": EPISODE_EXAMPLE_REF,
            },
            {
                "relation_type": "points_to_tos_fragment",
                "target_ref": TOS_FRAGMENT_REF,
            },
        ],
        "provenance_note": PROVENANCE_NOTE,
        "non_identity_boundary": NON_IDENTITY_BOUNDARY,
    }


def main() -> int:
    payload = build_kag_export_payload()
    write_json(KAG_EXPORT_PATH, payload)
    print(f"[OK]   wrote {KAG_EXPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1) from exc
