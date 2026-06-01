"""Runtime writeback projection and governance checks."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def load_runtime_writeback_targets_builder():
    module_path = WRITEBACK_RUNTIME_PART / "scripts" / "generate_runtime_writeback_targets.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_targets",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_targets.min.json")
        print("  - unable to load runtime writeback target generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_runtime_writeback_intake_builder():
    module_path = WRITEBACK_RUNTIME_PART / "scripts" / "generate_runtime_writeback_intake.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_intake",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_intake.min.json")
        print("  - unable to load runtime writeback intake generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_runtime_writeback_governance_builder():
    module_path = WRITEBACK_RUNTIME_PART / "scripts" / "generate_runtime_writeback_governance.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_governance",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_governance.min.json")
        print("  - unable to load runtime writeback governance generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_growth_refinery_writeback_lanes_builder():
    module_path = WRITEBACK_GROWTH_PART / "scripts" / "generate_growth_refinery_writeback_lanes.py"
    spec = importlib.util.spec_from_file_location(
        "generate_growth_refinery_writeback_lanes",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] growth_refinery_writeback_lanes.min.json")
        print("  - unable to load growth refinery writeback lane generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_phase_alpha_writeback_builder():
    module_path = WRITEBACK_GROWTH_PART / "scripts" / "generate_phase_alpha_writeback_map.py"
    spec = importlib.util.spec_from_file_location(
        "generate_phase_alpha_writeback_map",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] phase_alpha_writeback_map.min.json")
        print("  - unable to load Phase Alpha writeback map generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

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

def validate_growth_refinery_writeback_lanes() -> None:
    builder = load_growth_refinery_writeback_lanes_builder()
    expected = builder.build_growth_refinery_writeback_lanes_payload()
    data = load_json(GROWTH_REFINERY_WRITEBACK_LANES_PATH)
    errors: list[str] = []

    if data != expected:
        errors.append(
            "mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json is out of date; "
            "run mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py"
        )
    if data.get("schema_version") != 1:
        errors.append("mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json must declare schema_version 1")
    if data.get("layer") != "aoa-memo":
        errors.append("mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json must declare layer aoa-memo")
    if data.get("scope") != "growth-refinery-writeback":
        errors.append("mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json must declare scope growth-refinery-writeback")

    lanes = data.get("lanes")
    if not isinstance(lanes, list):
        errors.append("mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json must expose lanes as a list")
    else:
        seen_lane_refs: set[str] = set()
        seen_memory_ids: set[str] = set()
        for index, lane in enumerate(lanes):
            if not isinstance(lane, dict):
                errors.append(f"lanes[{index}] must be an object")
                continue
            for field_name in (
                "lane_ref",
                "target_kind",
                "object_ref_kind",
                "writeback_class",
                "review_status",
                "memory_id",
                "source_path",
                "primary_ref",
            ):
                if not isinstance(lane.get(field_name), str) or not lane[field_name]:
                    errors.append(f"lanes[{index}].{field_name} must be a non-empty string")
            lane_ref = lane.get("lane_ref")
            if isinstance(lane_ref, str):
                if lane_ref in seen_lane_refs:
                    errors.append(f"lanes[{index}].lane_ref duplicates {lane_ref!r}")
                else:
                    seen_lane_refs.add(lane_ref)
            memory_id = lane.get("memory_id")
            if isinstance(memory_id, str):
                if memory_id in seen_memory_ids:
                    errors.append(f"lanes[{index}].memory_id duplicates {memory_id!r}")
                else:
                    seen_memory_ids.add(memory_id)
            if lane.get("object_ref_kind") != "support_memory":
                errors.append(f"lanes[{index}].object_ref_kind must stay 'support_memory'")
            if lane.get("writeback_class") != "growth_refinery_memory":
                errors.append(f"lanes[{index}].writeback_class must stay 'growth_refinery_memory'")
            for list_name in ("required_evidence_refs", "optional_evidence_refs"):
                values = lane.get(list_name)
                if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
                    errors.append(f"lanes[{index}].{list_name} must be a list of non-empty strings")
            required_refs = lane.get("required_evidence_refs")
            if isinstance(required_refs, list) and not required_refs:
                errors.append(f"lanes[{index}].required_evidence_refs must not be empty")

    if errors:
        print("[FAIL] growth_refinery_writeback_lanes.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   growth_refinery_writeback_lanes.min.json")

def validate_phase_alpha_writeback_map() -> None:
    builder = load_phase_alpha_writeback_builder()
    expected = builder.build_phase_alpha_writeback_map_payload()
    data = load_json(PHASE_ALPHA_WRITEBACK_OUTPUT_PATH)
    source = load_json(PHASE_ALPHA_WRITEBACK_MAP_PATH)

    errors: list[str] = []
    if data != expected:
        errors.append(
            "mechanics/writeback/parts/growth-and-continuity/generated/phase_alpha_writeback_map.min.json is out of date; "
            "run mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py"
        )
    if not isinstance(source, dict):
        errors.append("mechanics/writeback/parts/growth-and-continuity/examples/phase_alpha_writeback_map.example.json must stay an object")
    else:
        if source.get("surface_type") != "phase_alpha_writeback_map":
            errors.append(
                "mechanics/writeback/parts/growth-and-continuity/examples/phase_alpha_writeback_map.example.json surface_type must stay phase_alpha_writeback_map"
            )
        playbooks = source.get("playbooks")
        if not isinstance(playbooks, list) or len(playbooks) != 5:
            errors.append(
                "mechanics/writeback/parts/growth-and-continuity/examples/phase_alpha_writeback_map.example.json must keep the five Alpha playbook mappings"
            )
        else:
            expected_ids = ["AOA-P-0014", "AOA-P-0006", "AOA-P-0018", "AOA-P-0008", "AOA-P-0009"]
            seen_ids: list[str] = []
            for index, item in enumerate(playbooks):
                if not isinstance(item, dict):
                    errors.append(f"playbooks[{index}] must be an object")
                    continue
                playbook_id = item.get("playbook_id")
                seen_ids.append(playbook_id)
                for field_name in ("writeback_kinds", "source_refs"):
                    value = item.get(field_name)
                    if not isinstance(value, list) or not value:
                        errors.append(f"playbooks[{index}].{field_name} must be a non-empty list")
                        continue
                    for ref_index, ref in enumerate(value):
                        if field_name == "source_refs":
                            error = local_ref_error(ref, f"playbooks[{index}].source_refs[{ref_index}]")
                            if error:
                                errors.append(error)
                if playbook_id == "AOA-P-0018" and item.get("pattern_after_second_recurrence") is not True:
                    errors.append("validation-driven-remediation must keep pattern_after_second_recurrence true")
                if playbook_id == "AOA-P-0008" and item.get("claim_candidate_after_reviewer") is not True:
                    errors.append("long-horizon-model-tier-orchestra must keep claim_candidate_after_reviewer true")
                if playbook_id == "AOA-P-0009":
                    retained = item.get("route_artifacts_retained")
                    if retained != ["inquiry_checkpoint"]:
                        errors.append("restartable-inquiry-loop must keep inquiry_checkpoint as a retained route artifact")
            if seen_ids != expected_ids:
                errors.append(
                    "mechanics/writeback/parts/growth-and-continuity/examples/phase_alpha_writeback_map.example.json playbooks drifted from the fixed Alpha order"
                )

        recall_posture = source.get("recall_posture")
        if not isinstance(recall_posture, dict):
            errors.append("mechanics/writeback/parts/growth-and-continuity/examples/phase_alpha_writeback_map.example.json must keep recall_posture")
        else:
            if recall_posture.get("path") != ["inspect", "capsule", "expand"]:
                errors.append("Phase Alpha recall_posture.path must stay inspect -> capsule -> expand")
            if recall_posture.get("memo_first_only") is not True:
                errors.append("Phase Alpha recall_posture.memo_first_only must stay true")
            expected_contract_ref = "examples/recall/recall_contract.object.working.phase-alpha.json"
            if recall_posture.get("contract_ref") != expected_contract_ref:
                errors.append(f"Phase Alpha recall_posture.contract_ref must stay {expected_contract_ref}")
            error = local_ref_error(recall_posture.get("contract_ref"), "recall_posture.contract_ref")
            if error:
                errors.append(error)

    if errors:
        print("[FAIL] phase_alpha_writeback_map")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   phase_alpha_writeback_map")
