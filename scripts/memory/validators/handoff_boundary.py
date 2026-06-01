"""Inter-agent handoff and export-boundary validation profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def load_kag_export_builder():
    module_path = CONSUMER_HANDOFF_KAG_SOURCE_EXPORT_PART / "scripts" / "generate_kag_export.py"
    spec = importlib.util.spec_from_file_location(
        "generate_kag_export",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json")
        print("  - unable to load KAG export generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def validate_routing_memory_adoption_surface() -> None:
    doc = load_text(ROOT / "mechanics" / "adoption" / "docs" / "ROUTING_MEMORY_ADOPTION.md")
    doc_compact = " ".join(doc.split())
    readme = load_text(ROOT / "README.md")
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")
    errors: list[str] = []

    if "mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md" not in readme:
        errors.append("README.md must route mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md")
    if "mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md")

    for fragment in [
        "Inspect first.",
        "Hydrate through capsules second.",
        "Expand only when the capsule step is insufficient.",
        "The inspect id is the join key across all three steps.",
        "If a route still needs stronger grounding after the capsule or section step",
        "routing authority outside the memory layer",
    ]:
        if fragment not in doc_compact:
            errors.append(f"mechanics/adoption/docs/ROUTING_MEMORY_ADOPTION.md must mention {fragment!r}")

    router_contracts = {
        name: load_json(example_path_for(name))
        for name in (
            "recall_contract.router.semantic.json",
            "recall_contract.router.lineage.json",
        )
    }
    object_contracts = {
        name: load_json(example_path_for(name))
        for name in (
            "recall_contract.object.semantic.json",
            "recall_contract.object.lineage.json",
            "recall_contract.object.working.return.json",
        )
    }

    for name, payload in router_contracts.items():
        if payload.get("inspect_surface") != "generated/memory/memory_catalog.min.json":
            errors.append(f"{name} must inspect through generated/memory/memory_catalog.min.json")
        if payload.get("capsule_surface") != "generated/memory/memory_capsules.json":
            errors.append(f"{name} must hydrate through generated/memory/memory_capsules.json")
        if payload.get("expand_surface") != "generated/memory/memory_sections.full.json":
            errors.append(f"{name} must expand through generated/memory/memory_sections.full.json")
        if payload.get("source_route_required") is not True:
            errors.append(f"{name} must keep source_route_required true")
        notes = payload.get("notes")
        if not isinstance(notes, str) or "inspect" not in notes.lower() or "capsule" not in notes.lower():
            errors.append(f"{name} notes must keep inspect/capsule posture explicit")

    for name, payload in object_contracts.items():
        if payload.get("inspect_surface") != "generated/memory-objects/memory_object_catalog.min.json":
            errors.append(f"{name} must inspect through generated/memory-objects/memory_object_catalog.min.json")
        if payload.get("capsule_surface") != "generated/memory-objects/memory_object_capsules.json":
            errors.append(f"{name} must hydrate through generated/memory-objects/memory_object_capsules.json")
        if payload.get("expand_surface") != "generated/memory-objects/memory_object_sections.full.json":
            errors.append(f"{name} must expand through generated/memory-objects/memory_object_sections.full.json")
        expected_source_route_required = name != "recall_contract.object.working.return.json"
        if payload.get("source_route_required") is not expected_source_route_required:
            errors.append(
                f"{name} must keep source_route_required {expected_source_route_required}"
            )
        notes = payload.get("notes")
        if not isinstance(notes, str) or "inspect" not in notes.lower() or "capsule" not in notes.lower():
            errors.append(f"{name} notes must keep inspect/capsule posture explicit")

    if errors:
        print("[FAIL] routing memory adoption surface")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   routing memory adoption surface")

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

def validate_bridge_export_contracts() -> None:
    chunk_validator = validator_for("memory_chunk_face.schema.json")
    graph_validator = validator_for("memory_graph_face.schema.json")
    registry = load_json(GENERATED / "memory" / "memo_registry.min.json")

    episode = load_json(example_path_for("episode.tos-interpretation.example.json"))
    claim = load_json(example_path_for("claim.tos-bridge-ready.example.json"))
    bridge = load_json(example_path_for("bridge.kag-lift.example.json"))
    thread = load_json(example_path_for("provenance_thread.kag-lift.example.json"))
    chunk = load_json(example_path_for("memory_chunk_face.bridge.example.json"))
    graph = load_json(example_path_for("memory_graph_face.bridge.example.json"))

    errors = [
        f"chunk.{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(chunk_validator.iter_errors(chunk), key=lambda err: list(err.absolute_path))
    ]
    errors.extend(
        f"graph.{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(graph_validator.iter_errors(graph), key=lambda err: list(err.absolute_path))
    )

    ref_checks: list[tuple[str, object]] = []
    for index, value in enumerate(thread.get("source_refs", [])):
        ref_checks.append((f"provenance_thread.kag-lift.source_refs[{index}]", value))
    for list_name in ("section_refs", "source_refs", "source_fragment_refs", "strongest_next_sources"):
        for index, value in enumerate(chunk.get(list_name, [])):
            ref_checks.append((f"memory_chunk_face.bridge.{list_name}[{index}]", value))
    for index, value in enumerate(graph.get("tos_refs", [])):
        ref_checks.append((f"memory_graph_face.bridge.tos_refs[{index}]", value))
    for index, value in enumerate(graph.get("strongest_authored_refs", [])):
        ref_checks.append((f"memory_graph_face.bridge.strongest_authored_refs[{index}]", value))
    for rel_index, relation in enumerate(graph.get("relation_candidates", [])):
        if not isinstance(relation, dict):
            continue
        for ref_index, value in enumerate(relation.get("evidence_refs", [])):
            ref_checks.append((f"memory_graph_face.bridge.relation_candidates[{rel_index}].evidence_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    episode_id = episode.get("id")
    claim_id = claim.get("id")
    bridge_id = bridge.get("id")
    thread_id = thread.get("id")

    if episode_id not in claim.get("provenance", {}).get("episode_refs", []):
        errors.append("claim.tos-bridge-ready.example.json must point back to the ToS interpretation episode")
    if claim.get("provenance", {}).get("provenance_thread_id") != thread_id:
        errors.append("claim.tos-bridge-ready.example.json must stay attached to provenance_thread.kag-lift.example.json")
    if bridge.get("provenance", {}).get("provenance_thread_id") != thread_id:
        errors.append("bridge.kag-lift.example.json must stay attached to provenance_thread.kag-lift.example.json")
    if sorted(thread.get("memory_object_ids", [])) != sorted([episode_id, claim_id, bridge_id]):
        errors.append("provenance_thread.kag-lift.example.json must track the episode, claim, and bridge example ids")

    if chunk.get("source_memory_id") != bridge_id:
        errors.append("memory_chunk_face.bridge.example.json must export the bridge.kag-lift example")
    if bridge_id not in chunk.get("bridge_refs", []):
        errors.append("memory_chunk_face.bridge.example.json must keep the bridge id in bridge_refs")
    if graph.get("source_memory_id") != bridge_id:
        errors.append("memory_graph_face.bridge.example.json must export the bridge.kag-lift example")
    if thread_id not in graph.get("provenance_thread_ids", []):
        errors.append("memory_graph_face.bridge.example.json must preserve the provenance thread id")

    relation_targets = {relation.get("target_ref") for relation in graph.get("relation_candidates", []) if isinstance(relation, dict)}
    if episode_id not in relation_targets:
        errors.append("memory_graph_face.bridge.example.json must expose a relation candidate back to the source episode")
    if claim_id not in relation_targets:
        errors.append("memory_graph_face.bridge.example.json must expose a relation candidate back to the reviewed claim")

    bridge_bridges = bridge.get("bridges", {})
    shared_envelope_ref = bridge_bridges.get("shared_envelope_ref")
    if shared_envelope_ref != "repo:aoa-kag/examples/aoa_tos_bridge_envelope.example.json":
        errors.append("bridge.kag-lift.example.json must keep shared_envelope_ref pointed at the canonical aoa-kag envelope example")
    append_ref_errors(
        errors,
        [("bridge.kag-lift.shared_envelope_ref", shared_envelope_ref)],
    )
    if bridge_bridges.get("kag_lift_status") != "candidate":
        errors.append("bridge.kag-lift.example.json must keep kag_lift_status as candidate")
    if not bridge_bridges.get("tos_refs"):
        errors.append("bridge.kag-lift.example.json must keep at least one ToS ref")
    if graph.get("kag_lift_status") != bridge_bridges.get("kag_lift_status"):
        errors.append("memory_graph_face.bridge.example.json must match the bridge kag_lift_status")

    if "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_chunk_face.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_chunk_face.schema.json")
    if "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_graph_face.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_graph_face.schema.json")
    if "mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md" not in registry.get("core_docs", []):
        errors.append("generated/memory/memo_registry.min.json must list mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md")

    if errors:
        print("[FAIL] bridge export contract surfaces")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   bridge export contract surfaces")

def validate_kag_source_export() -> None:
    builder = load_kag_export_builder()
    kag_export_path = builder.KAG_EXPORT_PATH

    errors: list[str] = []
    expected_payload = builder.build_kag_export_payload()
    if not kag_export_path.exists():
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must exist")
        actual_payload = {}
    else:
        actual_payload = load_json(kag_export_path)

    if actual_payload != expected_payload:
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must match the committed generator-backed payload")

    missing_fields = sorted(KAG_EXPORT_REQUIRED_FIELDS - set(actual_payload))
    if missing_fields:
        errors.append(
            "mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json is missing required fields: "
            + ", ".join(missing_fields)
        )

    append_ref_errors(
        errors,
        [
            ("kag_export.entry_surface.path", actual_payload.get("entry_surface", {}).get("path")),
        ]
        + [
            (f"kag_export.direct_relations[{index}].target_ref", relation.get("target_ref"))
            for index, relation in enumerate(actual_payload.get("direct_relations", []))
            if isinstance(relation, dict)
        ],
    )

    source_inputs = actual_payload.get("source_inputs")
    if not isinstance(source_inputs, list) or len(source_inputs) != 2:
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep exactly two source_inputs")
    else:
        expected_source_inputs = expected_payload["source_inputs"]
        if source_inputs != expected_source_inputs:
            errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep the memo-primary / ToS-supporting source_inputs split")

    if actual_payload.get("section_handles") != expected_payload["section_handles"]:
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep the canonical bridge section_handles")
    if actual_payload.get("direct_relations") != expected_payload["direct_relations"]:
        errors.append(
            "mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep the source/claim/episode/ToS/provenance direct_relations set"
        )

    kag_root_text = os.environ.get("AOA_KAG_ROOT")
    if kag_root_text:
        kag_root = Path(kag_root_text).expanduser().resolve()
        schema_path = kag_root / "schemas" / "federation-kag-export.schema.json"
        if not schema_path.exists():
            errors.append(
                f"AOA_KAG_ROOT canonical schema path does not exist: {schema_path}"
            )
        else:
            schema = load_json(schema_path)
            validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
            schema_errors = [
                f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
                for err in sorted(
                    validator.iter_errors(actual_payload),
                    key=lambda err: list(err.absolute_path),
                )
            ]
            errors.extend(
                f"AOA_KAG_ROOT federation-kag-export.schema.json -> {message}"
                for message in schema_errors
            )

    if errors:
        print("[FAIL] mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json")

def run() -> None:
    validate_routing_memory_adoption_surface()
    validate_playbook_memory_scope_surface()
    validate_bridge_export_contracts()
    validate_kag_source_export()
