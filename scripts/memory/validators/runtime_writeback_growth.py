"""Runtime writeback projection and governance checks."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .runtime_writeback_builders import (
    load_growth_refinery_writeback_lanes_builder,
    load_phase_alpha_writeback_builder,
)

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
