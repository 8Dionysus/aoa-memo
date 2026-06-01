"""Inter-agent handoff and export-boundary validation profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

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
