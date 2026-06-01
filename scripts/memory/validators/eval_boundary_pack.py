"""Trace/eval guardrail validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .eval_boundary_pilot import _validate_guardrail_pilot_cases
from .eval_boundary_wider import _validate_guardrail_wider_cases

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
