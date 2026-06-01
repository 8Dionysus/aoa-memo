"""Memory/RAG/context validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403
from .questbook import validate_questbook_surface

def validate_core_memory_contract() -> None:
    validator = validator_for("core-memory-contract.schema.json")
    data = load_json(example_path_for("core_memory_contract.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    expected_core = registry.get("memory_object_kinds", [])
    expected_supporting = registry.get("supporting_objects", [])
    expected_profile_schema = "schemas/memory-objects/memory_object_profile.schema.json"
    expected_kind_schemas = CORE_KIND_SCHEMA_MAP

    append_ref_errors(
        errors,
        [("profile_schema", data.get("profile_schema"))]
        + [
            (f"kind_profile_schemas.{kind}", ref)
            for kind, ref in data.get("kind_profile_schemas", {}).items()
        ],
    )

    if sorted(data.get("core_memory_surfaces", [])) != sorted(expected_core):
        errors.append("core_memory_surfaces does not match generated/memory/memo_registry.min.json memory_object_kinds")
    if sorted(data.get("supporting_objects", [])) != sorted(expected_supporting):
        errors.append("supporting_objects does not match generated/memory/memo_registry.min.json supporting_objects")
    if data.get("profile_schema") != expected_profile_schema:
        errors.append("profile_schema must stay schemas/memory-objects/memory_object_profile.schema.json")
    if data.get("kind_profile_schemas") != expected_kind_schemas:
        errors.append("kind_profile_schemas does not match the shipped per-kind profile schema map")

    for ref in [expected_profile_schema, *expected_kind_schemas.values()]:
        if ref not in registry.get("schemas", []):
            errors.append(f"generated/memory/memo_registry.min.json must list {ref}")
    if "docs/memory/MEMORY_OBJECT_PROFILES.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list docs/memory/MEMORY_OBJECT_PROFILES.md")

    if errors:
        print("[FAIL] core_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   core_memory_contract.example.json")

def validate_witness_trace_contract() -> None:
    validator = validator_for("witness-trace.schema.json")
    data = load_json(example_path_for("witness_trace.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if "witness_trace" in registry.get("memory_object_kinds", []):
        errors.append("witness_trace must not appear in generated/memory/memo_registry.min.json memory_object_kinds")
    if "witness_trace" in registry.get("supporting_objects", []):
        errors.append("witness_trace must not appear in generated/memory/memo_registry.min.json supporting_objects")
    if "mechanics/recurrence-support/parts/witness-trace-contract/schemas/witness-trace.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/recurrence-support/parts/witness-trace-contract/schemas/witness-trace.schema.json")
    if "mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md")

    if not any(step.get("kind") == "tool" for step in data.get("steps", [])):
        errors.append("witness_trace.example.json must include at least one tool-visible step")
    if not any("state_delta" in step for step in data.get("steps", [])):
        errors.append("witness_trace.example.json must include at least one state_delta example")
    summary_output = data.get("summary_output", {})
    if summary_output.get("format") != "markdown":
        errors.append("witness_trace.example.json summary_output.format must stay 'markdown'")

    if errors:
        print("[FAIL] witness_trace.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   witness_trace.example.json")

def validate_quest_chronicle_surface() -> None:
    validator = validator_for("quest_chronicle.schema.json")
    data = load_json(example_path_for("quest_chronicle.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if "quest_chronicle" in registry.get("memory_object_kinds", []):
        errors.append("quest_chronicle must not appear in generated/memory/memo_registry.min.json memory_object_kinds")
    if "quest_chronicle" in registry.get("supporting_objects", []):
        errors.append("quest_chronicle must not appear in generated/memory/memo_registry.min.json supporting_objects")
    if "mechanics/writeback/parts/quest-and-chronicle/schemas/quest_chronicle.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/writeback/parts/quest-and-chronicle/schemas/quest_chronicle.schema.json")
    if "mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md")

    if data.get("public_safe") is not True:
        errors.append("quest_chronicle.example.json must stay public_safe")
    if data.get("temperature") == "hot":
        errors.append("quest_chronicle.example.json must not default to hot temperature")

    allowed_anchor_refs: set[str] = set()
    for field_name in ("campaign_ref", "recall_anchor_ref"):
        value = data.get(field_name)
        if isinstance(value, str) and value:
            allowed_anchor_refs.add(value)
    for field_name in ("quest_refs", "evidence_refs"):
        values = data.get(field_name)
        if isinstance(values, list):
            allowed_anchor_refs.update(value for value in values if isinstance(value, str) and value)

    for index, stage in enumerate(data.get("stage_witness", [])):
        if not isinstance(stage, dict):
            continue
        anchor_ref = stage.get("anchor_ref")
        if isinstance(anchor_ref, str) and anchor_ref not in allowed_anchor_refs:
            errors.append(
                f"quest_chronicle.example.json stage_witness[{index}].anchor_ref must resolve through quest_refs, evidence_refs, campaign_ref, or recall_anchor_ref"
            )
        next_recall_cue = stage.get("next_recall_cue")
        if not isinstance(next_recall_cue, str) or not next_recall_cue.strip():
            errors.append(f"quest_chronicle.example.json stage_witness[{index}] must include next_recall_cue")

    notes = data.get("notes")
    if not isinstance(notes, str) or "witness" not in notes.lower() or "not quest authority" not in notes.lower():
        errors.append("quest_chronicle.example.json notes must keep witness-only, non-authority posture explicit")

    if errors:
        print("[FAIL] quest_chronicle.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   quest_chronicle.example.json")

def validate_checkpoint_to_memory_contract() -> None:
    validator = validator_for("checkpoint-to-memory-contract.schema.json")
    data = load_json(example_path_for("checkpoint_to_memory_contract.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks = [("source_event_ref", data.get("source_event_ref"))]
    checkpoint_artifact = data.get("checkpoint_artifact", {})
    if isinstance(checkpoint_artifact, dict):
        ref_checks.append(("checkpoint_artifact.schema_ref", checkpoint_artifact.get("schema_ref")))
    runtime_boundary = data.get("runtime_boundary", {})
    if isinstance(runtime_boundary, dict):
        for index, value in enumerate(runtime_boundary.get("review_boundary_refs", [])):
            ref_checks.append((f"runtime_boundary.review_boundary_refs[{index}]", value))
    for index, rule in enumerate(data.get("mapping_rules", [])):
        if not isinstance(rule, dict):
            continue
        for ref_index, value in enumerate(rule.get("runtime_refs", [])):
            ref_checks.append((f"mapping_rules[{index}].runtime_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    if data.get("contract_type") != "checkpoint_to_memory_contract":
        errors.append("checkpoint_to_memory_contract.example.json contract_type must stay 'checkpoint_to_memory_contract'")
    if checkpoint_artifact.get("artifact_name") != "inquiry_checkpoint":
        errors.append("checkpoint_to_memory_contract.example.json must keep inquiry_checkpoint as the checkpoint artifact")
    if runtime_boundary.get("scratchpad_posture") != "runtime_local_only":
        errors.append("runtime scratchpad posture must stay runtime_local_only")
    if runtime_boundary.get("checkpoint_export_kind") != "state_capsule":
        errors.append("checkpoint export kind must stay state_capsule")
    if runtime_boundary.get("distillation_review_posture") != "review_required":
        errors.append("distillation review posture must stay review_required")

    expected_pairs = {
        ("checkpoint_export", "state_capsule"),
        ("approval_record", "decision"),
        ("transition_record", "decision"),
        ("execution_trace", "episode"),
        ("review_trace", "audit_event"),
        ("distillation_claim_candidate", "claim"),
        ("distillation_pattern_candidate", "pattern"),
        ("distillation_bridge_candidate", "bridge"),
    }
    seen_pairs = {
        (rule.get("runtime_surface"), rule.get("target_kind"))
        for rule in data.get("mapping_rules", [])
        if isinstance(rule, dict)
    }
    missing_pairs = sorted(expected_pairs - seen_pairs)
    if missing_pairs:
        errors.append(
            "checkpoint_to_memory_contract.example.json is missing required runtime-to-memo mappings: "
            + ", ".join(f"{surface}->{kind}" for surface, kind in missing_pairs)
        )

    runtime_surface_targets: dict[str, set[str]] = {}
    for rule in data.get("mapping_rules", []):
        if not isinstance(rule, dict):
            continue
        runtime_surface = rule.get("runtime_surface")
        target_kind = rule.get("target_kind")
        if not isinstance(runtime_surface, str) or not isinstance(target_kind, str):
            continue
        runtime_surface_targets.setdefault(runtime_surface, set()).add(target_kind)
    conflicting_runtime_mappings = {
        runtime_surface: sorted(target_kinds)
        for runtime_surface, target_kinds in runtime_surface_targets.items()
        if len(target_kinds) > 1
    }
    for runtime_surface, target_kinds in sorted(conflicting_runtime_mappings.items()):
        errors.append(
            "checkpoint_to_memory_contract.example.json has conflicting target kinds for "
            f"{runtime_surface}: {', '.join(target_kinds)}"
        )

    for target_kind in ("claim", "pattern", "bridge"):
        matching_rules = [
            rule
            for rule in data.get("mapping_rules", [])
            if isinstance(rule, dict) and rule.get("target_kind") == target_kind
        ]
        if not matching_rules:
            continue
        for rule in matching_rules:
            if rule.get("writeback_class") != "reviewed_candidate":
                errors.append(f"{target_kind} mappings must stay reviewed_candidate writeback")
            if rule.get("requires_human_review") is not True:
                errors.append(f"{target_kind} mappings must require human review")

    if "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json")
    if "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md")

    if errors:
        print("[FAIL] checkpoint_to_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   checkpoint_to_memory_contract.example.json")
