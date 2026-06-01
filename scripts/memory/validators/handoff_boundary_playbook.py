"""Inter-agent handoff and export-boundary validation profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def validate_playbook_memory_scope_surface() -> None:
    doc = load_text(
        ROOT
        / "mechanics"
        / "consumer-handoff"
        / "docs"
        / "PLAYBOOK_MEMORY_SCOPES.md"
    )
    doc_compact = " ".join(doc.split())
    readme = load_text(ROOT / "README.md")
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")
    working_contract = load_json(example_path_for("recall_contract.working.json"))
    return_contract = load_json(example_path_for("recall_contract.object.working.return.json"))
    inquiry_return = load_json(example_path_for("inquiry_checkpoint.return.example.json"))
    guardrail_pack = load_json(example_path_for("memory_eval_guardrail_pack.example.json"))
    errors: list[str] = []

    if "mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md" not in readme:
        errors.append("README.md must route mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md")
    if "mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md")

    for fragment in [
        "Playbooks should ask memo for bounded recall modes and explicit scopes.",
        "They should not assume a blank check to the whole memory layer.",
        "The default memo-side entrypoint for relaunch and checkpoint use is `examples/recall/recall_contract.working.json`.",
        "Return-oriented relaunch should prefer working recall plus explicit checkpoint continuity over widening the whole memo scope.",
        "Scope expansion should be explicit and reviewable.",
        "When a playbook requests return, it should ask for checkpoint anchors and exported state surfaces, not a new memory family.",
    ]:
        if fragment not in doc_compact:
            errors.append(f"mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md must mention {fragment!r}")

    for token in ["`working`", "`episodic`", "`semantic`", "`procedural`", "`lineage`", "`source_route`"]:
        if token not in doc:
            errors.append(f"mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md must mention {token}")
    for token in ["`thread`", "`session`", "`project`", "`workspace`", "`ecosystem`"]:
        if token not in doc:
            errors.append(f"mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md must mention {token}")
    for token in ["`inquiry_checkpoint`", "`state_capsule`", "`episode`", "`decision`", "`audit_event`", "`provenance_thread`"]:
        if token not in doc:
            errors.append(f"mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md must mention {token}")

    if working_contract.get("mode") != "working":
        errors.append("recall_contract.working.json must stay in working mode")
    if working_contract.get("allowed_scopes") != ["thread", "session", "project"]:
        errors.append("recall_contract.working.json must keep allowed_scopes ['thread', 'session', 'project']")
    if working_contract.get("preferred_kinds") != ["state_capsule", "decision", "episode", "audit_event"]:
        errors.append(
            "recall_contract.working.json must keep preferred_kinds ['state_capsule', 'decision', 'episode', 'audit_event']"
        )
    if working_contract.get("source_route_required") is not False:
        errors.append("recall_contract.working.json must keep source_route_required false")

    if return_contract.get("checkpoint_continuity_supported") is not True:
        errors.append("recall_contract.object.working.return.json must keep checkpoint_continuity_supported true")
    if return_contract.get("return_ready") is not True:
        errors.append("recall_contract.object.working.return.json must keep return_ready true")
    expected_support_refs = [
        "mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
        "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json",
        "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
        "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
    ]
    if return_contract.get("support_artifact_refs") != expected_support_refs:
        errors.append("recall_contract.object.working.return.json must keep the bounded checkpoint support artifact chain")

    return_pack = inquiry_return.get("return_pack", {})
    if return_pack.get("reentry_refs") != [
        "examples/recall/recall_contract.object.working.return.json",
        "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
    ]:
        errors.append("inquiry_checkpoint.return.example.json must keep object return recall plus recurrence docs as reentry_refs")
    if inquiry_return.get("memory_delta_refs") != ["mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json"]:
        errors.append("inquiry_checkpoint.return.example.json must keep checkpoint_to_memory_contract as the bounded memory delta")
    if inquiry_return.get("evidence_pack_refs") != [
        "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md",
        "mechanics/recurrence-support/docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
    ]:
        errors.append("inquiry_checkpoint.return.example.json must keep runtime and recurrence docs as evidence_pack_refs")

    recall_precision_case = None
    for case in guardrail_pack.get("cases", []):
        if isinstance(case, dict) and case.get("focus") == "recall_precision":
            recall_precision_case = case
            break
    if not isinstance(recall_precision_case, dict):
        errors.append("memory_eval_guardrail_pack.example.json must keep a recall_precision case")
    elif "mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md" not in recall_precision_case.get("input_refs", []):
        errors.append("memory_eval_guardrail_pack.example.json recall_precision case must reference mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md")

    if errors:
        print("[FAIL] playbook memory scope surface")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   playbook memory scope surface")
