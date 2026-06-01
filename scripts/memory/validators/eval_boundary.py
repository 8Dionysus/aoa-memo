"""Trace/eval guardrail validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def _guardrail_case_input_refs(case: dict[str, object]) -> set[str]:
    values = case.get("input_refs", [])
    if not isinstance(values, list):
        return set()
    return {value for value in values if isinstance(value, str)}

def _has_ref_with_prefix(refs: set[str], prefixes: tuple[str, ...]) -> bool:
    return any(ref.startswith(prefix) for ref in refs for prefix in prefixes)

def _validate_guardrail_pilot_cases(
    case_by_focus: dict[str, dict[str, object]],
    errors: list[str],
) -> None:
    pilot_focuses = {"recall_precision", "provenance_fidelity", "staleness"}
    missing_pilot_focuses = sorted(pilot_focuses - set(case_by_focus))
    if missing_pilot_focuses:
        errors.append(
            "memory_eval_guardrail_pack.example.json must keep first-pilot focuses: "
            + ", ".join(missing_pilot_focuses)
        )

    precision_case = case_by_focus.get("recall_precision")
    if isinstance(precision_case, dict):
        refs = _guardrail_case_input_refs(precision_case)
        recall_contract_refs = [
            ref for ref in refs if ref.startswith("examples/recall/recall_contract.")
        ]
        if not recall_contract_refs:
            errors.append(
                "recall_precision guardrail case must reference at least one recall contract example"
            )
        doctrine_surface_family = {
            "generated/memory/memory_catalog.min.json",
            "generated/memory/memory_capsules.json",
            "generated/memory/memory_sections.full.json",
        }
        object_surface_family = {
            "generated/memory-objects/memory_object_catalog.min.json",
            "generated/memory-objects/memory_object_capsules.json",
            "generated/memory-objects/memory_object_sections.full.json",
        }
        if not (
            doctrine_surface_family.issubset(refs) or object_surface_family.issubset(refs)
        ):
            errors.append(
                "recall_precision guardrail case must reference one inspect/capsule/expand surface family"
            )

    provenance_case = case_by_focus.get("provenance_fidelity")
    if isinstance(provenance_case, dict):
        refs = _guardrail_case_input_refs(provenance_case)
        if not _has_ref_with_prefix(
            refs,
            (
                "examples/provenance_thread.",
                "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/provenance_thread.",
                "mechanics/writeback/parts/growth-and-continuity/examples/provenance_thread.",
            ),
        ):
            errors.append(
                "provenance_fidelity guardrail case must reference a provenance_thread example"
            )
        if not _has_ref_with_prefix(
            refs,
            ("examples/claim.", "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/claim."),
        ):
            errors.append(
                "provenance_fidelity guardrail case must reference a claim example"
            )
        if not _has_ref_with_prefix(
            refs,
            ("examples/bridge.", "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge."),
        ):
            errors.append(
                "provenance_fidelity guardrail case must reference a bridge example"
            )

    staleness_case = case_by_focus.get("staleness")
    if isinstance(staleness_case, dict):
        refs = _guardrail_case_input_refs(staleness_case)
        required_docs = {
            "docs/posture/LIFECYCLE.md",
            "docs/posture/MEMORY_TRUST_POSTURE.md",
        }
        missing_docs = sorted(required_docs - refs)
        if missing_docs:
            errors.append(
                "staleness guardrail case must reference lifecycle/trust docs: "
                + ", ".join(missing_docs)
            )
        required_examples = {
            "examples/lifecycle/claim.current-entrypoint.example.json",
            "examples/lifecycle/claim.superseded.example.json",
            "examples/lifecycle/claim.retracted.example.json",
        }
        missing_examples = sorted(required_examples - refs)
        if missing_examples:
            errors.append(
                "staleness guardrail case must reference current/superseded/retracted examples: "
                + ", ".join(missing_examples)
            )

def _validate_guardrail_wider_cases(
    case_by_focus: dict[str, dict[str, object]],
    errors: list[str],
) -> None:
    temporal_case = case_by_focus.get("temporal_reasoning")
    if isinstance(temporal_case, dict):
        refs = _guardrail_case_input_refs(temporal_case)
        required_refs = {
            "docs/posture/LIFECYCLE.md",
            "docs/posture/MEMORY_TEMPERATURES.md",
            "examples/lifecycle/claim.current-entrypoint.example.json",
            "examples/lifecycle/claim.superseded.example.json",
            "mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md",
        }
        missing_refs = sorted(required_refs - refs)
        if missing_refs:
            errors.append(
                "temporal_reasoning guardrail case must reference lifecycle, temperature, claims, and forgetting operation: "
                + ", ".join(missing_refs)
            )

    knowledge_update_case = case_by_focus.get("knowledge_update")
    if isinstance(knowledge_update_case, dict):
        refs = _guardrail_case_input_refs(knowledge_update_case)
        required_refs = {
            "mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md",
            "mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.supersede.example.json",
            "examples/lifecycle/claim.current-entrypoint.example.json",
            "examples/lifecycle/claim.superseded.example.json",
        }
        missing_refs = sorted(required_refs - refs)
        if missing_refs:
            errors.append(
                "knowledge_update guardrail case must reference supersession docs and examples: "
                + ", ".join(missing_refs)
            )

    abstention_case = case_by_focus.get("abstention")
    if isinstance(abstention_case, dict):
        refs = _guardrail_case_input_refs(abstention_case)
        required_refs = {
            "docs/boundaries/BOUNDARIES.md",
            "docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md",
            "mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md",
            "mechanics/operational-gate/parts/write-path-guardrails/examples/memory_write_path_guard.untrusted_prompt_injection.example.json",
        }
        missing_refs = sorted(required_refs - refs)
        if missing_refs:
            errors.append(
                "abstention guardrail case must reference boundary and untrusted write-path examples: "
                + ", ".join(missing_refs)
            )

    selective_forgetting_case = case_by_focus.get("selective_forgetting")
    if isinstance(selective_forgetting_case, dict):
        refs = _guardrail_case_input_refs(selective_forgetting_case)
        required_refs = {
            "mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md",
            "mechanics/retention/parts/consolidation-and-forgetting/examples/memory_consolidation_forgetting.archive.example.json",
            "docs/posture/LIFECYCLE.md",
        }
        missing_refs = sorted(required_refs - refs)
        if missing_refs:
            errors.append(
                "selective_forgetting guardrail case must reference archive operation and lifecycle: "
                + ", ".join(missing_refs)
            )

    poisoning_case = case_by_focus.get("poisoning")
    if isinstance(poisoning_case, dict):
        refs = _guardrail_case_input_refs(poisoning_case)
        required_refs = {
            "docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md",
            "mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md",
            "mechanics/operational-gate/parts/write-path-guardrails/schemas/memory_write_path_guard_v1.json",
            "mechanics/operational-gate/parts/write-path-guardrails/examples/memory_write_path_guard.untrusted_prompt_injection.example.json",
        }
        missing_refs = sorted(required_refs - refs)
        if missing_refs:
            errors.append(
                "poisoning guardrail case must reference write-path guard docs, schema, and untrusted example: "
                + ", ".join(missing_refs)
            )

    contradiction_case = case_by_focus.get("contradiction_handling")
    if isinstance(contradiction_case, dict):
        refs = _guardrail_case_input_refs(contradiction_case)
        required_refs = {
            "docs/posture/LIFECYCLE.md",
            "examples/lifecycle/claim.current-entrypoint.example.json",
            "examples/lifecycle/claim.superseded.example.json",
            "examples/lifecycle/claim.retracted.example.json",
        }
        missing_refs = sorted(required_refs - refs)
        if missing_refs:
            errors.append(
                "contradiction_handling guardrail case must reference lifecycle and current/superseded/retracted claims: "
                + ", ".join(missing_refs)
            )

    permission_case = case_by_focus.get("permission_leakage")
    if isinstance(permission_case, dict):
        refs = _guardrail_case_input_refs(permission_case)
        required_prefixes = {
            "mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md": "agent memory posture seam",
            "docs/boundaries/BOUNDARIES.md": "memo boundary doc",
            "docs/boundaries/OPERATIONAL_BOUNDARY.md": "operational boundary doc",
        }
        missing_labels = [
            label
            for prefix, label in required_prefixes.items()
            if not any(ref.startswith(prefix) for ref in refs)
        ]
        if missing_labels:
            errors.append(
                "permission_leakage guardrail case must reference: "
                + ", ".join(sorted(missing_labels))
            )

    promotion_case = case_by_focus.get("over_promotion")
    if isinstance(promotion_case, dict):
        refs = _guardrail_case_input_refs(promotion_case)
        required_prefixes = {
            "mechanics/writeback/docs/WRITEBACK_TEMPERATURE_POLICY.md": "writeback temperature policy",
            "mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md": "agent memory posture seam",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.": "bridge candidate example",
        }
        missing_labels = [
            label
            for prefix, label in required_prefixes.items()
            if not any(ref.startswith(prefix) for ref in refs)
        ]
        if missing_labels:
            errors.append(
                "over_promotion guardrail case must reference: "
                + ", ".join(sorted(missing_labels))
            )

    merge_case = case_by_focus.get("hallucinated_merge")
    if isinstance(merge_case, dict):
        refs = _guardrail_case_input_refs(merge_case)
        required_prefixes = {
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/episode.": "episode example",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/claim.": "claim example",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.": "bridge example",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/provenance_thread.": "provenance_thread example",
        }
        missing_labels = [
            label
            for prefix, label in required_prefixes.items()
            if not any(ref.startswith(prefix) for ref in refs)
        ]
        if missing_labels:
            errors.append(
                "hallucinated_merge guardrail case must reference: "
                + ", ".join(sorted(missing_labels))
            )

def validate_memory_eval_guardrail_pack() -> None:
    validator = validator_for("memory_eval_guardrail_pack.schema.json")
    data = load_json(example_path_for("memory_eval_guardrail_pack.example.json"))
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks: list[tuple[str, object]] = []
    for index, value in enumerate(data.get("source_refs", [])):
        ref_checks.append((f"memory_eval_guardrail_pack.source_refs[{index}]", value))
    for case_index, case in enumerate(data.get("cases", [])):
        if not isinstance(case, dict):
            continue
        for ref_index, value in enumerate(case.get("input_refs", [])):
            ref_checks.append((f"memory_eval_guardrail_pack.cases[{case_index}].input_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    seen_case_ids: set[str] = set()
    seen_focuses: set[str] = set()
    case_by_focus: dict[str, dict[str, object]] = {}
    for case in data.get("cases", []):
        if not isinstance(case, dict):
            continue
        case_id = case.get("case_id")
        focus = case.get("focus")
        if isinstance(case_id, str):
            if case_id in seen_case_ids:
                errors.append(f"duplicate guardrail case id: {case_id}")
            seen_case_ids.add(case_id)
        if isinstance(focus, str):
            seen_focuses.add(focus)
            case_by_focus[focus] = case

    required_focuses = {
        "recall_precision",
        "provenance_fidelity",
        "staleness",
        "contradiction_handling",
        "temporal_reasoning",
        "knowledge_update",
        "abstention",
        "selective_forgetting",
        "poisoning",
        "permission_leakage",
        "over_promotion",
        "hallucinated_merge",
    }
    missing_focuses = sorted(required_focuses - seen_focuses)
    if missing_focuses:
        errors.append("memory_eval_guardrail_pack.example.json is missing required focuses: " + ", ".join(missing_focuses))

    _validate_guardrail_pilot_cases(case_by_focus, errors)
    _validate_guardrail_wider_cases(case_by_focus, errors)

    if data.get("handoff_target") != "aoa-evals":
        errors.append("memory_eval_guardrail_pack.example.json must hand off to aoa-evals")
    if "mechanics/consumer-handoff/parts/eval-guardrail-handoff/schemas/memory_eval_guardrail_pack.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/consumer-handoff/parts/eval-guardrail-handoff/schemas/memory_eval_guardrail_pack.schema.json")
    if "mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md")

    if errors:
        print("[FAIL] memory_eval_guardrail_pack.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory_eval_guardrail_pack.example.json")

def run() -> None:
    validate_memory_eval_guardrail_pack()
