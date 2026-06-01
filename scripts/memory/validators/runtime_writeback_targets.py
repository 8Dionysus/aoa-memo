"""Runtime writeback projection and governance checks."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .runtime_writeback_builders import (
    load_runtime_writeback_intake_builder,
    load_runtime_writeback_targets_builder,
)

def validate_runtime_writeback_targets() -> None:
    validator = validator_for("runtime-writeback-targets.schema.json")
    builder = load_runtime_writeback_targets_builder()
    expected = builder.build_runtime_writeback_targets_payload()
    data = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)
    contract = load_json(example_path_for("checkpoint_to_memory_contract.example.json"))

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if data != expected:
        errors.append(
            "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json is out of date; "
            "run mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py"
        )

    if data.get("contract_id") != "aoa-memo.runtime-writeback.v1":
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json must keep contract_id aoa-memo.runtime-writeback.v1")
    if data.get("source_of_truth") != "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json":
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json must keep source_of_truth mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json")
    if data.get("runtime_boundary") != contract.get("runtime_boundary", {}):
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json must keep runtime_boundary aligned with checkpoint_to_memory_contract.example.json")

    targets = data.get("targets")
    if not isinstance(targets, list):
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json targets must be a list")
    else:
        expected_targets = contract.get("mapping_rules", [])
        if len(targets) != len(expected_targets):
            errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json must include every mapping rule exactly once")
        runtime_surfaces = [
            target.get("runtime_surface")
            for target in targets
            if isinstance(target, dict) and isinstance(target.get("runtime_surface"), str)
        ]
        if len(runtime_surfaces) != len(set(runtime_surfaces)):
            errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json must not duplicate runtime_surface entries")
        for index, target in enumerate(targets):
            if not isinstance(target, dict):
                errors.append(f"targets[{index}] must be an object")
                continue
            runtime_surface = target.get("runtime_surface")
            if not isinstance(runtime_surface, str):
                continue
            matching_rule = next(
                (
                    rule
                    for rule in expected_targets
                    if isinstance(rule, dict) and rule.get("runtime_surface") == runtime_surface
                ),
                None,
            )
            if matching_rule is None:
                errors.append(f"targets[{index}] references unknown runtime_surface {runtime_surface!r}")
                continue
            for field_name in (
                "target_kind",
                "writeback_class",
                "requires_human_review",
                "review_state_default",
                "runtime_refs",
                "notes",
            ):
                if target.get(field_name) != matching_rule.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must stay aligned with checkpoint_to_memory_contract.example.json"
                    )
            runtime_refs = target.get("runtime_refs")
            if not isinstance(runtime_refs, list) or not runtime_refs or not all(
                isinstance(item, str) and item for item in runtime_refs
            ):
                errors.append(f"targets[{index}].runtime_refs must stay a non-empty string list")

            if target.get("writeback_class") == "reviewed_candidate":
                if target.get("review_state_default") != "proposed":
                    errors.append(f"targets[{index}].review_state_default must stay 'proposed' for reviewed_candidate mappings")
                if target.get("requires_human_review") is not True:
                    errors.append(f"targets[{index}].requires_human_review must stay true for reviewed_candidate mappings")

    if errors:
        print("[FAIL] runtime_writeback_targets.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   runtime_writeback_targets.min.json")

def validate_runtime_writeback_intake() -> None:
    builder = load_runtime_writeback_intake_builder()
    expected = builder.build_runtime_writeback_intake_payload()
    data = load_json(RUNTIME_WRITEBACK_INTAKE_PATH)
    target_surface = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)

    errors: list[str] = []
    if data != expected:
        errors.append(
            "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json is out of date; "
            "run mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py"
        )

    expected_source_of_truth = {
        "runtime_writeback_targets": "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json",
        "checkpoint_to_memory_contract": "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json",
        "runtime_writeback_seam": "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
        "quest_evidence_writeback": "mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md",
    }
    if data.get("source_of_truth") != expected_source_of_truth:
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json must keep the canonical source_of_truth map")

    targets = data.get("targets")
    source_targets = target_surface.get("targets") if isinstance(target_surface, dict) else None
    if not isinstance(targets, list):
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json targets must be a list")
    elif not isinstance(source_targets, list):
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json requires mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json targets")
    else:
        if len(targets) != len(source_targets):
            errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json must include every runtime writeback target exactly once")
        source_by_surface = {
            item.get("runtime_surface"): item
            for item in source_targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        }
        seen_runtime_surfaces: set[str] = set()
        for index, item in enumerate(targets):
            if not isinstance(item, dict):
                errors.append(f"targets[{index}] must be an object")
                continue
            runtime_surface = item.get("runtime_surface")
            if not isinstance(runtime_surface, str):
                errors.append(f"targets[{index}].runtime_surface must be a non-empty string")
                continue
            if runtime_surface in seen_runtime_surfaces:
                errors.append(f"targets[{index}].runtime_surface duplicates {runtime_surface!r}")
                continue
            seen_runtime_surfaces.add(runtime_surface)

            source_item = source_by_surface.get(runtime_surface)
            if source_item is None:
                errors.append(f"targets[{index}] references unknown runtime_surface {runtime_surface!r}")
                continue

            for field_name in (
                "target_kind",
                "writeback_class",
                "requires_human_review",
                "review_state_default",
                "runtime_refs",
            ):
                if item.get(field_name) != source_item.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must stay aligned with mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json"
                    )

            owner_review_refs = item.get("owner_review_refs")
            if not isinstance(owner_review_refs, list) or not owner_review_refs or not all(
                isinstance(ref, str) and ref for ref in owner_review_refs
            ):
                errors.append(f"targets[{index}].owner_review_refs must stay a non-empty string list")
            else:
                if "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md" not in owner_review_refs:
                    errors.append(f"targets[{index}].owner_review_refs must include mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md")
                if "mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md" not in owner_review_refs:
                    errors.append(f"targets[{index}].owner_review_refs must include mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md")

            writeback_class = item.get("writeback_class")
            requires_human_review = item.get("requires_human_review")
            expected_posture = (
                "review_candidate_only"
                if writeback_class == "reviewed_candidate"
                else "review_before_writeback"
                if requires_human_review is True
                else "capturable_runtime_export"
            )
            if item.get("intake_posture") != expected_posture:
                errors.append(f"targets[{index}].intake_posture must stay {expected_posture!r}")

            if writeback_class == "reviewed_candidate":
                if requires_human_review is not True:
                    errors.append(f"targets[{index}].requires_human_review must stay true for reviewed_candidate mappings")
                if item.get("review_state_default") != "proposed":
                    errors.append(f"targets[{index}].review_state_default must stay 'proposed' for reviewed_candidate mappings")

    if errors:
        print("[FAIL] runtime_writeback_intake.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   runtime_writeback_intake.min.json")
