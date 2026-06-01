"""Runtime writeback projection and governance checks."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .runtime_writeback_builders import load_runtime_writeback_governance_builder

def validate_runtime_writeback_governance() -> None:
    builder = load_runtime_writeback_governance_builder()
    expected = builder.build_runtime_writeback_governance_payload()
    data = load_json(RUNTIME_WRITEBACK_GOVERNANCE_PATH)
    target_surface = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)
    intake_surface = load_json(RUNTIME_WRITEBACK_INTAKE_PATH)

    errors: list[str] = []
    if data != expected:
        errors.append(
            "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json is out of date; "
            "run mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py"
        )
    if data.get("schema_version") != 1:
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json must declare schema_version 1")
    if data.get("layer") != "aoa-memo":
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json must declare layer aoa-memo")
    if data.get("scope") != "runtime-writeback":
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json must declare scope runtime-writeback")

    expected_source_of_truth = {
        "runtime_writeback_targets": "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json",
        "runtime_writeback_intake": "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json",
    }
    if data.get("source_of_truth") != expected_source_of_truth:
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json must keep the canonical source_of_truth map")

    targets = data.get("targets")
    source_targets = target_surface.get("targets") if isinstance(target_surface, dict) else None
    intake_targets = intake_surface.get("targets") if isinstance(intake_surface, dict) else None
    if not isinstance(targets, list):
        errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json targets must be a list")
    elif not isinstance(source_targets, list) or not isinstance(intake_targets, list):
        errors.append(
            "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json requires runtime writeback target and intake surfaces"
        )
    else:
        source_by_surface = {
            item.get("runtime_surface"): item
            for item in source_targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        }
        intake_by_surface = {
            item.get("runtime_surface"): item
            for item in intake_targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        }
        expected_surfaces = sorted(set(source_by_surface) | set(intake_by_surface))
        actual_surfaces = [
            item.get("runtime_surface")
            for item in targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        ]
        if actual_surfaces != expected_surfaces:
            errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json must cover every runtime writeback surface exactly once")
        if len(actual_surfaces) != len(set(actual_surfaces)):
            errors.append("mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_governance.min.json must not duplicate runtime_surface entries")

        for index, item in enumerate(targets):
            if not isinstance(item, dict):
                errors.append(f"targets[{index}] must be an object")
                continue
            runtime_surface = item.get("runtime_surface")
            if not isinstance(runtime_surface, str):
                errors.append(f"targets[{index}].runtime_surface must be a non-empty string")
                continue

            source_item = source_by_surface.get(runtime_surface)
            intake_item = intake_by_surface.get(runtime_surface)
            if item.get("in_writeback_targets") is not (source_item is not None):
                errors.append(f"targets[{index}].in_writeback_targets must reflect mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json")
            if item.get("in_writeback_intake") is not (intake_item is not None):
                errors.append(f"targets[{index}].in_writeback_intake must reflect mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json")

            if source_item is None:
                errors.append(f"targets[{index}] references missing runtime writeback target {runtime_surface!r}")
                continue
            if intake_item is None:
                errors.append(f"targets[{index}] references missing runtime writeback intake {runtime_surface!r}")
                continue

            for field_name in (
                "target_kind",
                "writeback_class",
                "requires_human_review",
                "review_state_default",
            ):
                if item.get(field_name) != source_item.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must match mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json"
                    )
                if item.get(field_name) != intake_item.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must match mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json"
                    )

            intake_posture = item.get("intake_posture")
            if intake_posture != intake_item.get("intake_posture"):
                errors.append(
                    f"targets[{index}].intake_posture must match mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json"
                )
            if not isinstance(intake_posture, str) or not intake_posture:
                errors.append(f"targets[{index}].intake_posture must be a non-empty string")

            blockers = item.get("blockers")
            if not isinstance(blockers, list) or not all(isinstance(entry, str) for entry in blockers):
                errors.append(f"targets[{index}].blockers must be a list of strings")
                continue
            if item.get("governance_passed") is not (len(blockers) == 0):
                errors.append(f"targets[{index}].governance_passed must reflect whether blockers is empty")
            if blockers:
                errors.append(f"targets[{index}] must not carry blockers in the committed governance surface")

    if errors:
        print("[FAIL] runtime_writeback_governance.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   runtime_writeback_governance.min.json")
