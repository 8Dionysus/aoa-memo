"""Memory/RAG/context validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403
from .questbook import validate_questbook_surface

def validate_memory_readiness_boundary_materialization() -> None:
    boundary_doc = MEMORY_READINESS_BOUNDARY_DOC_PATH.read_text(encoding="utf-8")
    checkpoint = load_json(example_path_for("inquiry_checkpoint.return.example.json"))
    contradiction = load_json(example_path_for("claim.phase-alpha-runtime-history-later-infra-track.example.json"))
    bridge = load_json(example_path_for("bridge.kag-lift.example.json"))
    retention = load_json(example_path_for("audit_event.memory-retention-check.example.json"))
    service = load_json(example_path_for("audit_event.service-governed-fallback.example.json"))
    catalog = load_json(GENERATED / "memory-objects" / "memory_object_catalog.min.json")
    errors: list[str] = []

    for phrase in (
        "memory delta",
        "canon delta reference",
        "retention check",
        "unresolved contradiction",
        "survivor or bridge candidate",
        "civil/service assistant trace",
    ):
        if phrase not in boundary_doc:
            errors.append(f"{MEMORY_READINESS_BOUNDARY_DOC_REF} must keep pressure row {phrase!r}")

    memory_delta_refs = checkpoint.get("memory_delta_refs")
    canon_delta_refs = checkpoint.get("canon_delta_refs")
    if not isinstance(memory_delta_refs, list) or not memory_delta_refs:
        errors.append("inquiry_checkpoint.return.example.json must keep non-empty memory_delta_refs")
    if not isinstance(canon_delta_refs, list) or not canon_delta_refs:
        errors.append("inquiry_checkpoint.return.example.json must keep non-empty canon_delta_refs")
    if isinstance(memory_delta_refs, list) and isinstance(canon_delta_refs, list):
        overlap = sorted(set(memory_delta_refs) & set(canon_delta_refs))
        if overlap:
            errors.append(
                "inquiry_checkpoint.return.example.json must keep memory_delta_refs distinct from canon_delta_refs "
                f"(overlap={overlap})"
            )

    contradiction_refs = contradiction.get("lifecycle", {}).get("current_recall", {}).get("contradiction_refs")
    if not isinstance(contradiction_refs, list) or not contradiction_refs:
        errors.append(
            "claim.phase-alpha-runtime-history-later-infra-track.example.json must keep explicit contradiction_refs"
        )

    bridge_lifecycle = bridge.get("lifecycle", {})
    if bridge_lifecycle.get("review_state") != "proposed":
        errors.append("bridge.kag-lift.example.json must keep lifecycle.review_state == 'proposed'")
    if bridge_lifecycle.get("retention_class") != "bridge-candidate":
        errors.append("bridge.kag-lift.example.json must keep lifecycle.retention_class == 'bridge-candidate'")

    retention_sources = retention.get("provenance", {}).get("source_refs")
    if retention.get("kind") != "audit_event":
        errors.append("audit_event.memory-retention-check.example.json must stay an audit_event")
    if retention.get("lifecycle", {}).get("retention_class") != "audit-trace":
        errors.append("audit_event.memory-retention-check.example.json must keep lifecycle.retention_class == 'audit-trace'")
    if not isinstance(retention_sources, list) or (
        MEMORY_READINESS_BOUNDARY_PRESSURE_REF not in retention_sources
    ):
        errors.append(
            f"audit_event.memory-retention-check.example.json must cite {MEMORY_READINESS_BOUNDARY_PRESSURE_REF}"
        )

    service_sources = service.get("provenance", {}).get("source_refs")
    if service.get("kind") != "audit_event":
        errors.append("audit_event.service-governed-fallback.example.json must stay an audit_event")
    if service.get("lifecycle", {}).get("retention_class") != "audit-trace":
        errors.append(
            "audit_event.service-governed-fallback.example.json must keep lifecycle.retention_class == 'audit-trace'"
        )
    if not isinstance(service_sources, list) or not any(
        "service_degradation_receipt" in ref for ref in service_sources
    ):
        errors.append(
            "audit_event.service-governed-fallback.example.json must preserve a source receipt ref"
        )
    if not isinstance(service_sources, list) or "repo:aoa-agents/docs/AGENT_RUNTIME_SEAM.md" not in service_sources:
        errors.append(
            "audit_event.service-governed-fallback.example.json must preserve the aoa-agents owner boundary ref"
        )

    catalog_objects = catalog.get("memory_objects")
    catalog_ids: set[str] = set()
    if isinstance(catalog_objects, list):
        catalog_ids = {
            item.get("id")
            for item in catalog_objects
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
    for object_id in (
        "memo.audit.2026-04-13.memo-entrypoint-retention-check",
        "memo.audit.2026-04-07.hybrid-query-service-fallback",
    ):
        if object_id not in catalog_ids:
            errors.append(
                "generated/memory-objects/memory_object_catalog.min.json must surface memory readiness example "
                f"{object_id}"
            )

    if errors:
        print("[FAIL] memory readiness boundary materialization")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory readiness boundary materialization")

def validate_memory_readiness_boundary_contract() -> None:
    doc = MEMORY_READINESS_BOUNDARY_DOC_PATH.read_text(encoding="utf-8")
    schema = validator_for(MEMORY_READINESS_BOUNDARY_CONTRACT_SCHEMA)
    payload = load_json(MEMORY_READINESS_BOUNDARY_CONTRACT_PATH)
    errors: list[str] = []

    for token in (
        "mechanics/readiness-boundary/parts/memory-readiness-boundary/schemas/memory_readiness_boundary_contract.schema.json",
        "mechanics/readiness-boundary/parts/memory-readiness-boundary/examples/memory_readiness_boundary_contract.example.json",
        "memory_gate",
        "retention_boundary",
        "writeback_boundary",
    ):
        if token not in doc:
            errors.append(f"{MEMORY_READINESS_BOUNDARY_DOC_REF} must mention {token}")

    if payload.get("contract_id") != "aoa-memo.memory-readiness-boundary.v1":
        errors.append(
            "memory_readiness_boundary_contract.example.json must keep contract_id aoa-memo.memory-readiness-boundary.v1"
        )
    if payload.get("owner_repo") != "aoa-memo":
        errors.append("memory_readiness_boundary_contract.example.json must keep owner_repo aoa-memo")

    errors.extend(
        f"memory_readiness_boundary_contract.example.json schema violation: {error.message}"
        for error in schema.iter_errors(payload)
    )

    gate = payload.get("memory_gate", {})
    retention = payload.get("retention_boundary", {})
    writeback = payload.get("writeback_boundary", {})
    if not isinstance(gate, dict) or "live scratchpad residue" not in gate.get("rejected_inputs", []):
        errors.append("memory_readiness_boundary_contract.example.json must reject live scratchpad residue")
    if not isinstance(retention, dict) or retention.get("owned_by") != "abyss-stack":
        errors.append("memory_readiness_boundary_contract.example.json must keep retention owned by abyss-stack")
    if not isinstance(writeback, dict) or "mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md" not in writeback.get("export_surfaces", []):
        errors.append(
            "memory_readiness_boundary_contract.example.json must point writeback at mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md"
        )

    if errors:
        print("[FAIL] memory readiness boundary contract")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory readiness boundary contract")
