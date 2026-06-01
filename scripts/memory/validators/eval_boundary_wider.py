"""Trace/eval guardrail validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .eval_boundary_helpers import _guardrail_case_input_refs, _has_ref_with_prefix

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
