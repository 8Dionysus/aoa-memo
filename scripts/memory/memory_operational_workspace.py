from __future__ import annotations

from typing import Any

from memory_operational_readout_common import GENERATED_BY, WORKSPACE_MAP, WORKSPACE_MAP_REF, load_json


def compact_workspace_place(place: dict[str, Any]) -> dict[str, Any]:
    memo_port = place.get("memo_port") if isinstance(place.get("memo_port"), dict) else {}
    return {
        "name": place.get("name", ""),
        "memory_role": place.get("memory_role", ""),
        "current_port_level": place.get("current_port_level", ""),
        "recommended_port_level": place.get("recommended_port_level", ""),
        "memory_route_status": place.get("memory_route_status", ""),
        "reviewed_memory_route": place.get("reviewed_memory_route", ""),
        "evidence_route": place.get("evidence_route", ""),
        "memo_port": {
            "port_level": memo_port.get("port_level", ""),
            "present": bool(memo_port.get("present")),
            "local_candidates": int(memo_port.get("local_candidates") or 0),
            "pending_candidates": int(memo_port.get("pending_candidates") or 0),
            "pending_exports": int(memo_port.get("pending_exports") or 0),
            "ready_exports": int(memo_port.get("ready_exports") or 0),
            "blocked_exports": int(memo_port.get("blocked_exports") or 0),
            "landed_exports": int(memo_port.get("landed_exports") or 0),
            "index_present": bool(memo_port.get("index_present")),
            "privacy_posture": memo_port.get("privacy_posture", ""),
            "stronger_memory_owner": memo_port.get("stronger_memory_owner", ""),
        },
        "issues": list(place.get("issues") or []),
        "next_route": place.get("validation_command", ""),
    }


def build_workspace_port_status() -> dict[str, Any] | None:
    if not WORKSPACE_MAP.is_file():
        return None
    workspace_map = load_json(WORKSPACE_MAP)
    places = [compact_workspace_place(place) for place in workspace_map.get("places", [])]
    return {
        "schema_version": "aoa_memo_workspace_port_status_v1",
        "surface_kind": "memo_imported_workspace_port_status",
        "owner_repo": "aoa-memo",
        "source_owner": "8Dionysus",
        "source_ref": WORKSPACE_MAP_REF,
        "source_refs": [
            "docs/memory/LIVING_MEMORY_TOPOLOGY.md#port-status-surface",
            WORKSPACE_MAP_REF,
        ],
        "generated_by": GENERATED_BY,
        "authority_boundary": {
            "memo_owns": "memory-port interpretation, reviewed-memory route, and consumer handoff posture",
            "workspace_map_owner": "8Dionysus owns workspace overlay scanning and published map shape",
            "runtime_owner": "abyss-stack owns MCP service implementation and runtime status",
            "not_claimed": "this readout does not make aoa-memo the workspace topology owner",
        },
        "source_snapshot": {
            "schema_version": workspace_map.get("schema_version", ""),
            "surface_kind": workspace_map.get("surface_kind", ""),
            "owner_repo": workspace_map.get("owner_repo", ""),
            "reviewed_memory_owner": workspace_map.get("reviewed_memory_owner", ""),
            "session_evidence_owner": workspace_map.get("session_evidence_owner", ""),
            "totals": workspace_map.get("totals", {}),
            "access_plane": workspace_map.get("access_plane", {}),
        },
        "places": places,
        "summary": {
            "places": len(places),
            "with_issues": sum(1 for place in places if place["issues"]),
            "full_ports": sum(1 for place in places if place["current_port_level"] == "full_port"),
            "route_only": sum(1 for place in places if place["current_port_level"] == "route_only"),
            "pending_exports": sum(place["memo_port"]["pending_exports"] for place in places),
            "ready_exports": sum(place["memo_port"]["ready_exports"] for place in places),
            "landed_exports": sum(place["memo_port"]["landed_exports"] for place in places),
            "overall_status": "passed" if all(not place["issues"] for place in places) else "issues_present",
        },
        "quest_closure": {
            "quest_id": "AOA-MEM-Q-0015",
            "close_condition": "current port levels, export posture, issues, and next routes are reproducible from owner surfaces",
            "result": "done",
        },
    }
