"""Quest source and projection checks for the memory-context profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .questbook_discovery import discover_questbook_files

def build_expected_quest_catalog_entry(
    quest: dict[str, object], *, source_path: str
) -> dict[str, object]:
    entry: dict[str, object] = {
        "id": quest["id"],
        "title": quest["title"],
        "repo": quest["repo"],
        "theme_ref": quest.get("theme_ref", ""),
        "milestone_ref": quest.get("milestone_ref", ""),
        "state": quest["state"],
        "band": quest["band"],
        "kind": quest["kind"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "owner_surface": quest["owner_surface"],
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    for optional_key in (
        "orchestrator_class_ref",
        "capability_target",
        "playbook_family_refs",
        "proof_surface_refs",
        "memory_surface_refs",
    ):
        if optional_key in quest:
            entry[optional_key] = quest[optional_key]
    return entry

def build_expected_quest_dispatch_entry(
    quest: dict[str, object], *, source_path: str
) -> dict[str, object]:
    activation = quest.get("activation")
    if not isinstance(activation, dict):
        activation = {}
    requires_artifacts = ["recurrence_evidence", "promotion_decision"] if quest.get("kind") == "harvest" else [
        "bounded_plan",
        "work_result",
        "verification_result",
    ]
    entry: dict[str, object] = {
        "schema_version": "quest_dispatch_v1",
        "id": quest["id"],
        "repo": quest["repo"],
        "state": quest["state"],
        "band": quest["band"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "control_mode": quest["control_mode"],
        "delegate_tier": quest["delegate_tier"],
        "split_required": quest["split_required"],
        "write_scope": quest["write_scope"],
        "requires_artifacts": requires_artifacts,
        "activation_mode": activation.get("mode"),
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    if "fallback_tier" in quest:
        entry["fallback_tier"] = quest.get("fallback_tier")
    if "wrapper_class" in quest:
        entry["wrapper_class"] = quest.get("wrapper_class")
    for optional_key in ("orchestrator_class_ref", "capability_target"):
        if optional_key in quest:
            entry[optional_key] = quest.get(optional_key)
    return entry

def build_quest_catalog_projection() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for quest_id, path in discover_questbook_files().items():
        payload = load_yaml(path)
        if not isinstance(payload, dict):
            print("[FAIL] questbook writeback surface")
            print(f"  - {path.relative_to(ROOT)} must parse to a mapping")
            raise SystemExit(1)
        entries.append(
            build_expected_quest_catalog_entry(
                payload,
                source_path=path.relative_to(ROOT).as_posix(),
            )
        )
    return entries

def build_quest_dispatch_projection() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for _, path in discover_questbook_files().items():
        payload = load_yaml(path)
        if not isinstance(payload, dict):
            print("[FAIL] questbook writeback surface")
            print(f"  - {path.relative_to(ROOT)} must parse to a mapping")
            raise SystemExit(1)
        entries.append(
            build_expected_quest_dispatch_entry(
                payload,
                source_path=path.relative_to(ROOT).as_posix(),
            )
        )
    return entries
