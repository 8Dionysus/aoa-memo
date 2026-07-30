"""Source/schema validation profile for memo contracts."""

from __future__ import annotations

from .schema_recall_contracts import *  # noqa: F401,F403
from .schema_surfaces import *  # noqa: F401,F403

def run() -> None:
    validate_nested_agents_surface()
    for schema_name in SUPPORT_SCHEMA_NAMES:
        validate_support_schema(schema_name)
    validate_active_organ_contract_suite()
    validate_memory_object_surface_manifest()
    for example_name in MEMORY_OBJECT_EXAMPLE_NAMES:
        validate_example(validator_for("memory_object.schema.json"), example_name)
    validate_example(validator_for("inquiry_checkpoint.schema.json"), "inquiry_checkpoint.example.json")
    validate_example(validator_for("inquiry_checkpoint.schema.json"), "inquiry_checkpoint.return.example.json")
    for example_name in PROVENANCE_THREAD_EXAMPLE_NAMES:
        validate_example(validator_for("provenance_thread.schema.json"), example_name)
    for example_name in FAILURE_LESSON_EXAMPLE_NAMES:
        validate_example(validator_for("failure_lesson_memory_v1.json"), example_name)
    for example_name in RECOVERY_PATTERN_EXAMPLE_NAMES:
        validate_example(validator_for("recovery_pattern_memory_v1.json"), example_name)
    validate_recall_contract_example(
        "recall_contract.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory/memo_registry.min.json",
        expected_expand_surface="docs/memory/MEMORY_MODEL.md",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.router.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory/memory_catalog.min.json",
        expected_capsule_surface="generated/memory/memory_capsules.json",
        expected_expand_surface="generated/memory/memory_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.working.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory/memory_catalog.min.json",
        expected_expand_surface="mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
        expected_source_route_required=False,
    )
    validate_recall_contract_example(
        "recall_contract.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory/memory_catalog.min.json",
        expected_expand_surface="mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.router.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory/memory_catalog.min.json",
        expected_capsule_surface="generated/memory/memory_capsules.json",
        expected_expand_surface="generated/memory/memory_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.object.working.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
        expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
        expected_source_route_required=False,
    )
    validate_recall_contract_example(
        "recall_contract.object.working.return.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
        expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
        expected_source_route_required=False,
        expected_checkpoint_continuity_supported=True,
        expected_return_ready=True,
        expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
        expected_support_artifact_refs=[
            "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
            "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json",
            "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
            "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
        ],
    )
    validate_recall_contract_example(
        "recall_contract.object.working.phase-alpha.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
        expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
        expected_source_route_required=False,
        expected_checkpoint_continuity_supported=True,
        expected_return_ready=True,
        expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
        expected_support_artifact_refs=[
            "mechanics/writeback/parts/growth-and-continuity/generated/phase_alpha_writeback_map.min.json",
            "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
            "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
            "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
        ],
    )
    validate_recall_contract_example(
        "recall_contract.object.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
        expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.object.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory-objects/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory-objects/memory_object_capsules.json",
        expected_expand_surface="generated/memory-objects/memory_object_sections.full.json",
        expected_source_route_required=True,
    )
