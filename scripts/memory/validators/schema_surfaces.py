"""Source/schema validation profile for memo contracts."""

from __future__ import annotations

import copy
from typing import Any

from ._shared import *  # noqa: F403

ACTIVE_ORGAN_SCHEMA_NAME = "active_organ_memo_contracts_v1.schema.json"
ACTIVE_ORGAN_EXAMPLE_SUITE = "active_organ_memo_contracts_v1.examples.json"
ACTIVE_ORGAN_CONTRACT_TYPES = {
    "memory_evidence_envelope",
    "memory_candidate_packet",
    "memory_quarantine_packet",
    "reviewed_memory_object",
    "provenance_thread",
    "memory_lifecycle_transition",
    "recall_packet",
    "intervention_decision",
    "memory_influence_policy_envelope",
    "memory_projection_manifest",
    "memory_erase_request",
    "distributed_memory_erase_manifest",
    "per_owner_erase_work_item",
    "erase_completion_or_residue_receipt",
}
ACTIVE_ORGAN_ALLOWED_TRANSITIONS = {
    ("captured", "proposed"),
    ("proposed", "confirmed"),
    ("proposed", "retracted"),
    ("confirmed", "frozen"),
    ("confirmed", "superseded"),
    ("confirmed", "retracted"),
    ("frozen", "superseded"),
    ("frozen", "retracted"),
    ("superseded", "archived"),
    ("retracted", "archived"),
}
ACTIVE_ORGAN_ERASE_SURFACE_CLASSES = {
    "ER0": "canonical_object",
    "ER1": "raw_session_attachment",
    "ER2": "local_memo_port",
    "ER3": "projection",
    "ER4": "runtime",
    "ER5": "backup_restore",
    "ER6": "host_local",
    "ER7": "experiment_replay",
    "ER8": "training_unlearning",
    "ER9": "audit_receipt",
}


def _schema_error_messages(error: Any) -> list[str]:
    messages = [error.message]
    for child in error.context:
        messages.extend(_schema_error_messages(child))
    return messages


def _active_organ_contract_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    contract_type = payload.get("contract_type")

    if contract_type in {
        "memory_evidence_envelope",
        "memory_candidate_packet",
        "memory_quarantine_packet",
        "recall_packet",
    }:
        taint = payload.get("taint")
        if isinstance(taint, dict) and taint.get("tainted") is True and taint.get("quarantine_required") is not True:
            errors.append("tainted payload must require quarantine")
        if isinstance(taint, dict) and taint.get("sanitizer_receipt_ref") is not None and not taint.get("labels"):
            errors.append("sanitizer receipt cannot erase taint lineage labels")

    if contract_type == "memory_candidate_packet":
        if payload.get("data_class") == "D4":
            errors.append("D4 prohibited material cannot enter a memory candidate")
        if payload.get("risk_class") == "R6":
            errors.append("R6 external-effect material cannot enter a memory candidate")

    if contract_type == "provenance_thread":
        events = payload.get("ordered_events")
        if isinstance(events, list):
            sequences = [event.get("sequence") for event in events if isinstance(event, dict)]
            if sequences != list(range(1, len(events) + 1)):
                errors.append("ordered_events sequence must be consecutive from 1")

    if contract_type == "memory_lifecycle_transition":
        prior = payload.get("expected_prior_version")
        following = payload.get("next_version")
        if isinstance(prior, int) and isinstance(following, int) and following != prior + 1:
            errors.append("next_version must equal expected_prior_version + 1")
        transition = (payload.get("from_state"), payload.get("to_state"))
        if transition not in ACTIVE_ORGAN_ALLOWED_TRANSITIONS:
            errors.append(f"unsupported lifecycle transition {transition[0]} -> {transition[1]}")
    if contract_type == "recall_packet":
        taint = payload.get("taint")
        if isinstance(taint, dict) and taint.get("tainted") is True and payload.get("result_mode") != "silence":
            errors.append("tainted recall packet must resolve to silence")

    if contract_type == "memory_projection_manifest":
        source_generation = payload.get("source_generation")
        projected_generation = payload.get("projected_generation")
        state = payload.get("projection_state")
        recall_eligible = payload.get("recall_eligible")
        rebuild_required = payload.get("rebuild_required")
        if (
            isinstance(source_generation, int)
            and isinstance(projected_generation, int)
            and projected_generation > source_generation
        ):
            errors.append("projected_generation cannot exceed source_generation")
        if state == "active" and (
            projected_generation != source_generation
            or recall_eligible is not True
            or rebuild_required is not False
            or payload.get("validation_status") != "valid"
            or not payload.get("built_artifact_refs")
        ):
            errors.append(
                "active projection requires exact current source generation, "
                "valid status, built artifacts, recall eligibility, and no rebuild"
            )
        if state != "active" and recall_eligible is not False:
            errors.append("non-active projection must not be recall eligible")
        if state in {"stale", "pending_rebuild", "invalidated"}:
            if rebuild_required is not True:
                errors.append(f"{state} projection must require rebuild")
            if payload.get("invalidation_receipt_ref") is None:
                errors.append(
                    f"{state} projection must cite its invalidation receipt"
                )
        if state == "erased" and (
            rebuild_required is not False or payload.get("built_artifact_refs") != []
        ):
            errors.append("erased projection must have no artifacts or rebuild")

    if contract_type == "distributed_memory_erase_manifest":
        owners = payload.get("owner_set")
        owner_results = payload.get("owner_results")
        erase_surfaces = payload.get("erase_surfaces")
        if isinstance(owners, list) and isinstance(owner_results, list):
            result_owners = [
                result.get("owner")
                for result in owner_results
                if isinstance(result, dict)
            ]
            if len(result_owners) != len(owner_results) or set(result_owners) != set(owners) or len(result_owners) != len(set(result_owners)):
                errors.append("owner_results must cover owner_set exactly once")
            mappings = (
                ("work_item_refs", "work_item_ref"),
                ("erase_receipt_refs", "erase_receipt_ref"),
                ("recovery_probe_refs", "recovery_probe_ref"),
            )
            for manifest_field, result_field in mappings:
                manifest_refs = payload.get(manifest_field)
                result_refs = [
                    result.get(result_field)
                    for result in owner_results
                    if isinstance(result, dict)
                ]
                if isinstance(manifest_refs, list) and set(manifest_refs) != set(result_refs):
                    errors.append(f"{manifest_field} must match owner_results.{result_field}")
            if isinstance(erase_surfaces, list):
                surface_ids = [
                    surface.get("surface_id")
                    for surface in erase_surfaces
                    if isinstance(surface, dict)
                ]
                if len(surface_ids) != len(erase_surfaces) or len(surface_ids) != len(set(surface_ids)):
                    errors.append("erase_surfaces must contain each erase surface at most once")
                for surface in erase_surfaces:
                    if not isinstance(surface, dict):
                        continue
                    surface_id = surface.get("surface_id")
                    expected_class = ACTIVE_ORGAN_ERASE_SURFACE_CLASSES.get(surface_id)
                    if expected_class != surface.get("surface_class"):
                        errors.append(f"{surface_id} must use surface_class {expected_class}")
                    if surface.get("owner") not in owners:
                        errors.append(f"{surface_id} owner must be present in owner_set")
                    if surface.get("work_item_ref") not in payload.get("work_item_refs", []):
                        errors.append(f"{surface_id} work_item_ref must be present in work_item_refs")
            if payload.get("completion_state") == "complete":
                if any(result.get("result") != "erased" for result in owner_results if isinstance(result, dict)):
                    errors.append("complete erase manifest requires every owner result to be erased")
                if payload.get("residue_refs") != []:
                    errors.append("complete erase manifest cannot contain residue_refs")
                if payload.get("validation_status") != "valid":
                    errors.append("complete erase manifest requires validation_status valid")
                if isinstance(erase_surfaces, list) and any(
                    surface.get("surface_state") != "erased" or surface.get("retention_exceptions")
                    for surface in erase_surfaces
                    if isinstance(surface, dict)
                ):
                    errors.append("complete erase manifest requires erased surfaces without retention exceptions")
            if payload.get("completion_state") == "complete_with_approved_exceptions":
                if not isinstance(erase_surfaces, list) or not any(
                    surface.get("retention_exceptions")
                    for surface in erase_surfaces
                    if isinstance(surface, dict)
                ):
                    errors.append("complete_with_approved_exceptions requires a named approved retention exception")
                if any(
                    surface.get("surface_state") not in {"erased", "residue"}
                    for surface in erase_surfaces or []
                    if isinstance(surface, dict)
                ):
                    errors.append("approved-exception closure cannot contain pending, failed, or blocked surfaces")
                if any(
                    surface.get("surface_state") == "residue" and not surface.get("retention_exceptions")
                    for surface in erase_surfaces or []
                    if isinstance(surface, dict)
                ):
                    errors.append("residue surface requires an approved retention exception for closure")

    if contract_type == "per_owner_erase_work_item" and payload.get("target_owner") == "abyss-machine":
        if payload.get("target_class") != "host" or payload.get("erase_surface_id") != "ER6":
            errors.append("abyss-machine erase work must remain host-owned ER6")

    if contract_type == "erase_completion_or_residue_receipt":
        residue_refs = payload.get("residue_refs")
        residue_count = payload.get("residue_count")
        if isinstance(residue_refs, list) and isinstance(residue_count, int) and residue_count != len(residue_refs):
            errors.append("residue_count must equal len(residue_refs)")
        if payload.get("result") == "erased":
            if residue_count != 0 or residue_refs != []:
                errors.append("erased receipt cannot retain residue")
            if not payload.get("recovery_probe_refs"):
                errors.append("erased receipt requires at least one recovery probe")
        if payload.get("result") == "residue" and residue_count == 0:
            errors.append("residue receipt requires non-zero residue_count")

    return errors


def _apply_example_mutation(payload: dict[str, Any], mutation: dict[str, Any]) -> None:
    path = mutation.get("path")
    operation = mutation.get("op")
    if not isinstance(path, str) or not path.startswith("/"):
        raise ValueError("mutation.path must be an absolute JSON pointer")
    tokens = [token.replace("~1", "/").replace("~0", "~") for token in path[1:].split("/")]
    target: Any = payload
    for token in tokens[:-1]:
        target = target[int(token)] if isinstance(target, list) else target[token]
    leaf = tokens[-1]
    if operation == "remove":
        if isinstance(target, list):
            target.pop(int(leaf))
        else:
            target.pop(leaf)
        return
    if operation not in {"add", "replace"}:
        raise ValueError(f"unsupported mutation operation: {operation}")
    value = copy.deepcopy(mutation.get("value"))
    if isinstance(target, list):
        index = int(leaf)
        if operation == "add":
            target.insert(index, value)
        else:
            target[index] = value
    else:
        target[leaf] = value


def validate_active_organ_contract_suite() -> None:
    validator = validator_for(ACTIVE_ORGAN_SCHEMA_NAME)
    suite = load_json(example_path_for(ACTIVE_ORGAN_EXAMPLE_SUITE))
    errors: list[str] = []

    expected_suite_fields = {
        "suite_id",
        "schema_ref",
        "purpose",
        "header_template",
        "valid_cases",
        "invalid_cases",
    }
    if set(suite) != expected_suite_fields:
        errors.append("example suite must use the exact v1 suite fields")
    if suite.get("schema_ref") != f"schemas/support-objects/{ACTIVE_ORGAN_SCHEMA_NAME}":
        errors.append("example suite schema_ref must point to the active-organ v1 owner schema")

    header = suite.get("header_template")
    valid_cases = suite.get("valid_cases")
    invalid_cases = suite.get("invalid_cases")
    if not isinstance(header, dict) or not isinstance(valid_cases, list) or not isinstance(invalid_cases, list):
        errors.append("example suite header_template, valid_cases, and invalid_cases have invalid shapes")
        valid_cases = []
        invalid_cases = []

    materialized: dict[str, dict[str, Any]] = {}
    valid_types: list[str] = []
    for index, case in enumerate(valid_cases):
        if not isinstance(case, dict) or set(case) != {"case_id", "payload"}:
            errors.append(f"valid_cases[{index}] must contain only case_id and payload")
            continue
        case_id = case.get("case_id")
        payload_fragment = case.get("payload")
        if not isinstance(case_id, str) or not isinstance(payload_fragment, dict):
            errors.append(f"valid_cases[{index}] has invalid case_id or payload")
            continue
        payload = {**copy.deepcopy(header), **copy.deepcopy(payload_fragment)}
        materialized[case_id] = payload
        valid_types.append(payload.get("contract_type"))
        schema_errors = [
            message
            for error in validator.iter_errors(payload)
            for message in _schema_error_messages(error)
        ]
        semantic_errors = _active_organ_contract_errors(payload)
        if schema_errors or semantic_errors:
            errors.append(f"{case_id} positive payload failed: {schema_errors + semantic_errors}")

    if set(valid_types) != ACTIVE_ORGAN_CONTRACT_TYPES or len(valid_types) != len(ACTIVE_ORGAN_CONTRACT_TYPES):
        errors.append("valid cases must cover every memo-owned active-organ contract exactly once")

    negative_types: list[str] = []
    for index, case in enumerate(invalid_cases):
        expected_fields = {"case_id", "base_case", "mutation", "expected_failure"}
        if not isinstance(case, dict) or set(case) != expected_fields:
            errors.append(f"invalid_cases[{index}] must use the exact negative-case fields")
            continue
        case_id = case.get("case_id")
        base_case = case.get("base_case")
        mutation = case.get("mutation")
        expected_failure = case.get("expected_failure")
        if not all(isinstance(value, str) for value in (case_id, base_case, expected_failure)) or not isinstance(mutation, dict):
            errors.append(f"invalid_cases[{index}] has an invalid field type")
            continue
        base_payload = materialized.get(base_case)
        if base_payload is None:
            errors.append(f"{case_id} references unknown base case {base_case}")
            continue
        payload = copy.deepcopy(base_payload)
        try:
            _apply_example_mutation(payload, mutation)
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            errors.append(f"{case_id} mutation failed: {exc}")
            continue
        negative_types.append(base_payload["contract_type"])
        failure_messages = [
            message
            for error in validator.iter_errors(payload)
            for message in _schema_error_messages(error)
        ]
        failure_messages.extend(_active_organ_contract_errors(payload))
        if not failure_messages:
            errors.append(f"{case_id} negative payload was accepted")
        elif not any(expected_failure in message for message in failure_messages):
            errors.append(f"{case_id} did not produce expected failure {expected_failure!r}: {failure_messages}")

    if set(negative_types) != ACTIVE_ORGAN_CONTRACT_TYPES or len(negative_types) != len(ACTIVE_ORGAN_CONTRACT_TYPES):
        errors.append("negative cases must cover every memo-owned active-organ contract exactly once")

    if errors:
        print(f"[FAIL] {ACTIVE_ORGAN_EXAMPLE_SUITE}")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)
    print(f"[OK]   {ACTIVE_ORGAN_EXAMPLE_SUITE}")


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
