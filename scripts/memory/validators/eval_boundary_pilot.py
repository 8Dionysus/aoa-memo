"""Trace/eval guardrail validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .eval_boundary_helpers import _guardrail_case_input_refs, _has_ref_with_prefix

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
