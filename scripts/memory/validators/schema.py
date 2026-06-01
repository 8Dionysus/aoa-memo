"""Source/schema validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def validate_nested_agents_surface() -> None:
    try:
        from validate_nested_agents import validate_nested_agents_docs
    except Exception as exc:  # pragma: no cover - defensive wiring guard
        print("[FAIL] nested AGENTS docs")
        print(f"  - unable to load nested AGENTS validator: {exc}")
        raise SystemExit(1) from exc

    try:
        validate_nested_agents_docs()
    except RuntimeError as exc:
        print("[FAIL] nested AGENTS docs")
        print(f"  - {exc}")
        raise SystemExit(1) from exc

    print("[OK]   nested AGENTS docs")

def validate_support_schema(schema_name: str) -> None:
    validator_for(schema_name)
    print(f"[OK]   {schema_name}")

def validate_memory_object_surface_manifest() -> None:
    validator = validator_for("memory_object_surface_manifest.schema.json")
    data = load_json(example_path_for("memory_object_surface_manifest.json"))

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    seen_paths: set[str] = set()
    for index, entry in enumerate(data.get("entries", [])):
        path = entry.get("example_path")
        if path in seen_paths:
            errors.append(f"entries[{index}].example_path duplicates {path}")
        if isinstance(path, str):
            seen_paths.add(path)
        error = local_ref_error(path, f"entries[{index}].example_path")
        if error:
            errors.append(error)

    if errors:
        print("[FAIL] memory_object_surface_manifest.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory_object_surface_manifest.json")

def validate_recall_contract_example(
    example_name: str,
    *,
    expected_mode: str,
    expected_allowed_scopes: list[str],
    expected_preferred_kinds: list[str],
    expected_temperature_order: list[str],
    expected_inspect_surface: str,
    expected_expand_surface: str,
    expected_source_route_required: bool,
    expected_capsule_surface: str | None = None,
    expected_checkpoint_continuity_supported: bool | None = None,
    expected_return_ready: bool | None = None,
    expected_preferred_anchor_kinds: list[str] | None = None,
    expected_support_artifact_refs: list[str] | None = None,
) -> None:
    validator = validator_for("recall_contract.schema.json")
    data = load_json(example_path_for(example_name))

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    support_artifact_refs = data.get("support_artifact_refs")
    if not isinstance(support_artifact_refs, list):
        support_artifact_refs = []
    append_ref_errors(
        errors,
        [
            ("inspect_surface", data.get("inspect_surface")),
            ("capsule_surface", data.get("capsule_surface")),
            ("expand_surface", data.get("expand_surface")),
        ]
        + [
            (f"support_artifact_refs[{index}]", value)
            for index, value in enumerate(support_artifact_refs)
        ],
    )

    if data.get("mode") != expected_mode:
        errors.append(f"{example_name} mode must stay '{expected_mode}'")
    if data.get("allowed_scopes") != expected_allowed_scopes:
        errors.append(f"{example_name} allowed_scopes must stay {expected_allowed_scopes}")
    if data.get("preferred_kinds") != expected_preferred_kinds:
        errors.append(f"{example_name} preferred_kinds must stay {expected_preferred_kinds}")
    if data.get("temperature_order") != expected_temperature_order:
        errors.append(f"{example_name} temperature_order must stay {expected_temperature_order}")
    if data.get("inspect_surface") != expected_inspect_surface:
        errors.append(f"{example_name} inspect_surface must stay {expected_inspect_surface}")
    if expected_capsule_surface is not None and data.get("capsule_surface") != expected_capsule_surface:
        errors.append(f"{example_name} capsule_surface must stay {expected_capsule_surface}")
    if data.get("expand_surface") != expected_expand_surface:
        errors.append(f"{example_name} expand_surface must stay {expected_expand_surface}")
    if data.get("source_route_required") is not expected_source_route_required:
        errors.append(f"{example_name} source_route_required must stay {expected_source_route_required}")
    if expected_checkpoint_continuity_supported is not None and data.get("checkpoint_continuity_supported") is not expected_checkpoint_continuity_supported:
        errors.append(
            f"{example_name} checkpoint_continuity_supported must stay {expected_checkpoint_continuity_supported}"
        )
    if expected_return_ready is not None and data.get("return_ready") is not expected_return_ready:
        errors.append(f"{example_name} return_ready must stay {expected_return_ready}")
    if expected_preferred_anchor_kinds is not None and data.get("preferred_anchor_kinds") != expected_preferred_anchor_kinds:
        errors.append(f"{example_name} preferred_anchor_kinds must stay {expected_preferred_anchor_kinds}")
    if expected_support_artifact_refs is not None and data.get("support_artifact_refs") != expected_support_artifact_refs:
        errors.append(f"{example_name} support_artifact_refs must stay {expected_support_artifact_refs}")

    if errors:
        print(f"[FAIL] {example_name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {example_name}")

SUPPORT_SCHEMA_NAMES = (
    "memory_object_profile.schema.json",
    "trust_posture.schema.json",
    "lifecycle_posture.schema.json",
    "anchor.schema.json",
    "state_capsule.schema.json",
    "episode.schema.json",
    "claim.schema.json",
    "decision.schema.json",
    "pattern.schema.json",
    "bridge.schema.json",
    "audit_event.schema.json",
    "failure_lesson_memory_v1.json",
    "recovery_pattern_memory_v1.json",
    "memory_object_surface_manifest.schema.json",
    "memory_object_catalog.schema.json",
    "memory_object_capsules.schema.json",
    "memory_object_sections.schema.json",
    "decay_policy.schema.json",
    "inquiry_checkpoint.schema.json",
    "checkpoint-to-memory-contract.schema.json",
    "memory_chunk_face.schema.json",
    "memory_graph_face.schema.json",
    "quest_chronicle.schema.json",
    "memory_eval_guardrail_pack.schema.json",
)

MEMORY_OBJECT_EXAMPLE_NAMES = (
    "episode.example.json",
    "claim.example.json",
    "checkpoint_approval_record.example.json",
    "checkpoint_health_check.example.json",
    "episode.tos-interpretation.example.json",
    "claim.tos-bridge-ready.example.json",
    "bridge.kag-lift.example.json",
)

PROVENANCE_THREAD_EXAMPLE_NAMES = (
    "provenance_thread.example.json",
    "checkpoint_improvement_thread.example.json",
    "provenance_thread.kag-lift.example.json",
    "provenance_thread.self-agency-continuity.example.json",
    PHASE_ALPHA_PROVENANCE_THREAD_EXAMPLE,
)

FAILURE_LESSON_EXAMPLE_NAMES = (
    "failure_lesson_memory.example.json",
    "failure_lesson_memory.lineage.example.json",
    "failure_lesson_memory.rollout.example.json",
)

RECOVERY_PATTERN_EXAMPLE_NAMES = (
    "recovery_pattern_memory.example.json",
    "recovery_pattern_memory.lineage.example.json",
    "recovery_pattern_memory.rollout.example.json",
    "recovery_pattern_memory.component_refresh.example.json",
)

def run() -> None:
    validate_nested_agents_surface()
    for schema_name in SUPPORT_SCHEMA_NAMES:
        validate_support_schema(schema_name)
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
