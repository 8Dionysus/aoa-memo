"""Inter-agent handoff and export-boundary validation profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def validate_routing_memory_adoption_surface() -> None:
    doc = load_text(ROOT / "mechanics" / "adoption" / "docs" / "ROUTING_MEMORY_ADOPTION.md")
    doc_compact = " ".join(doc.split())
    readme = load_text(ROOT / "README.md")
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")
    errors: list[str] = []

    if "mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md" not in readme:
        errors.append("README.md must route mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md")
    if "mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md")

    for fragment in [
        "Inspect first.",
        "Hydrate through capsules second.",
        "Expand only when the capsule step is insufficient.",
        "The inspect id is the join key across all three steps.",
        "If a route still needs stronger grounding after the capsule or section step",
        "routing authority outside the memory layer",
    ]:
        if fragment not in doc_compact:
            errors.append(f"mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md must mention {fragment!r}")

    router_contracts = {
        name: load_json(example_path_for(name))
        for name in (
            "recall_contract.router.semantic.json",
            "recall_contract.router.lineage.json",
        )
    }
    object_contracts = {
        name: load_json(example_path_for(name))
        for name in (
            "recall_contract.object.semantic.json",
            "recall_contract.object.lineage.json",
            "recall_contract.object.working.return.json",
        )
    }

    for name, payload in router_contracts.items():
        if payload.get("inspect_surface") != "generated/memory/memory_catalog.min.json":
            errors.append(f"{name} must inspect through generated/memory/memory_catalog.min.json")
        if payload.get("capsule_surface") != "generated/memory/memory_capsules.json":
            errors.append(f"{name} must hydrate through generated/memory/memory_capsules.json")
        if payload.get("expand_surface") != "generated/memory/memory_sections.full.json":
            errors.append(f"{name} must expand through generated/memory/memory_sections.full.json")
        if payload.get("source_route_required") is not True:
            errors.append(f"{name} must keep source_route_required true")
        notes = payload.get("notes")
        if not isinstance(notes, str) or "inspect" not in notes.lower() or "capsule" not in notes.lower():
            errors.append(f"{name} notes must keep inspect/capsule posture explicit")

    for name, payload in object_contracts.items():
        if payload.get("inspect_surface") != "generated/memory-objects/memory_object_catalog.min.json":
            errors.append(f"{name} must inspect through generated/memory-objects/memory_object_catalog.min.json")
        if payload.get("capsule_surface") != "generated/memory-objects/memory_object_capsules.json":
            errors.append(f"{name} must hydrate through generated/memory-objects/memory_object_capsules.json")
        if payload.get("expand_surface") != "generated/memory-objects/memory_object_sections.full.json":
            errors.append(f"{name} must expand through generated/memory-objects/memory_object_sections.full.json")
        expected_source_route_required = name != "recall_contract.object.working.return.json"
        if payload.get("source_route_required") is not expected_source_route_required:
            errors.append(
                f"{name} must keep source_route_required {expected_source_route_required}"
            )
        notes = payload.get("notes")
        if not isinstance(notes, str) or "inspect" not in notes.lower() or "capsule" not in notes.lower():
            errors.append(f"{name} notes must keep inspect/capsule posture explicit")

    if errors:
        print("[FAIL] routing memory adoption surface")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   routing memory adoption surface")
