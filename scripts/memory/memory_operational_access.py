from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from memory_operational_readout_common import (
    GENERATED_BY,
    MCP_ROOT,
    MCP_SOURCE_HINT,
    REPO_ROOT,
    WORKSPACE_MAP_REF,
    WORKSPACE_ROOT,
)


MCP_UNAVAILABLE_ERROR = (
    "MCP checkout unavailable; set AOA_MEMO_MCP_ROOT to a readable "
    "aoa-memo-mcp checkout"
)


def run_mcp_cli(args: list[str], timeout: int = 20) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(MCP_ROOT / "src")
    try:
        if not MCP_ROOT.is_dir():
            return {"ok": False, "error": MCP_UNAVAILABLE_ERROR}
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "aoa_memo_mcp.cli",
                "--workspace-root",
                str(WORKSPACE_ROOT),
                *args,
            ],
            check=False,
            cwd=str(MCP_ROOT),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"MCP probe timed out after {timeout}s"}
    except OSError:
        return {"ok": False, "error": MCP_UNAVAILABLE_ERROR}
    if completed.returncode != 0:
        return {
            "ok": False,
            "error": completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}",
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {"ok": False, "error": f"invalid JSON output: {exc}"}
    return {"ok": True, "payload": payload}


def probe_status(name: str, kind: str, result: dict[str, Any], checks: dict[str, bool]) -> dict[str, Any]:
    if not result.get("ok"):
        return {
            "name": name,
            "kind": kind,
            "status": "failed",
            "checks": checks,
            "details": {"error": result.get("error", "unknown error")},
        }
    failed = sorted(key for key, ok in checks.items() if not ok)
    return {
        "name": name,
        "kind": kind,
        "status": "passed" if not failed else "failed",
        "checks": checks,
        "details": {},
    }


def compact_hit_ref(item: dict[str, Any]) -> str:
    item_id = item.get("id")
    if isinstance(item_id, str) and item_id:
        return item_id
    raw_path = item.get("path")
    if not isinstance(raw_path, str) or not raw_path:
        return ""
    path = Path(raw_path)
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except (OSError, ValueError):
        pass
    try:
        return "workspace:" + path.resolve().relative_to(WORKSPACE_ROOT).as_posix()
    except (OSError, ValueError):
        return "external-source"


def payload_dict(result: dict[str, Any]) -> dict[str, Any]:
    payload = result.get("payload") if result.get("ok") else {}
    return payload if isinstance(payload, dict) else {}


def dict_field(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def list_field(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key)
    return value if isinstance(value, list) else []


def live_access_probes() -> list[dict[str, Any]]:
    probes: list[dict[str, Any]] = []

    for repo, intent in (
        ("aoa-evals", "memory quality harness handoff from aoa-memo"),
        ("aoa-sdk", "router recall pack needs memo context"),
    ):
        result = run_mcp_cli(["brief", "--repo", repo, "--intent", intent])
        payload = payload_dict(result)
        reviewed = list_field(payload, "reviewed_memory")
        workspace_map = dict_field(payload, "workspace_memory_map")
        memory_route = dict_field(payload, "memory_route")
        checks = {
            "schema": payload.get("schema") == "aoa_memo_brief_v1",
            "workspace_map_found": bool(workspace_map.get("found")),
            "route_only_or_port_visible": bool(workspace_map.get("current_port_level")),
            "reviewed_memory_refs_visible": bool(reviewed),
            "durable_landing_not_mcp": memory_route.get("durable_landing")
            == "reviewed source patch in aoa-memo, not MCP direct write",
        }
        probe = probe_status(f"brief:{repo}", "brief", result, checks)
        if result.get("ok"):
            probe["details"] = {
                "current_port_level": workspace_map.get("current_port_level", ""),
                "reviewed_memory_ids": [
                    item.get("id", "")
                    for item in reviewed[:5]
                    if isinstance(item, dict) and item.get("id")
                ],
            }
        probes.append(probe)

    pending = run_mcp_cli(["pending-exports", "--repo", "abyss-stack"])
    payload = payload_dict(pending)
    counts = dict_field(payload, "counts")
    checks = {
        "schema": payload.get("schema") == "aoa_local_memo_pending_exports_v1",
        "ok": payload.get("ok") is True,
        "landed_export_visible": int(counts.get("landed") or 0) >= 1,
        "pending_export_classified": int(counts.get("pending") or 0) >= 1,
        "ready_exports_explicit": "ready" in counts,
    }
    probe = probe_status("pending-exports:abyss-stack", "pending_exports", pending, checks)
    if pending.get("ok"):
        probe["details"] = {"counts": counts}
    probes.append(probe)

    validate_port = run_mcp_cli(["validate-port", "--repo", "Agents-of-Abyss"])
    payload = payload_dict(validate_port)
    checks = {
        "schema": payload.get("schema") == "aoa_local_memo_port_validation_v1",
        "ok": payload.get("ok") is True,
        "errors_empty": not payload.get("errors"),
    }
    probes.append(probe_status("validate-port:Agents-of-Abyss", "port_validation", validate_port, checks))

    for name, query in (
        ("search:access-plane-route", "aoa-memo-mcp access plane route"),
        ("search:consumer-handoff-spine", "reviewed memory consumer handoff spine"),
    ):
        result = run_mcp_cli(["search", query, "--scope", "all", "--mode", "all"])
        payload = payload_dict(result)
        hits = list_field(payload, "hits")
        checks = {
            "schema": payload.get("schema") == "aoa_memo_search_v1",
            "not_low_confidence": payload.get("low_confidence") is False,
            "has_hits": bool(hits),
            "authority_note_visible": "authority_note" in payload,
        }
        probe = probe_status(name, "search", result, checks)
        if result.get("ok"):
            probe["details"] = {
                "hit_ids": [
                    compact_hit_ref(item)
                    for item in hits[:5]
                    if isinstance(item, dict) and compact_hit_ref(item)
                ]
            }
        probes.append(probe)

    foundation = run_mcp_cli(
        [
            "search",
            "memory organ foundation access plane currentness workspace memo port status",
            "--scope",
            "aoa-memo",
            "--mode",
            "contracts",
        ]
    )
    payload = payload_dict(foundation)
    hits = list_field(payload, "hits")
    status = "passed" if hits else "known_gap"
    probes.append(
        {
            "name": "search:fresh-foundation-terms",
            "kind": "search",
            "status": status,
            "checks": {
                "schema": payload.get("schema") == "aoa_memo_search_v1",
                "has_hits": bool(hits),
                "gap_routed": status == "known_gap",
            },
            "details": {
                "note": (
                    "Fresh foundation and quest terms are currently source-doc and generated-quest "
                    "surfaces, not reviewed-corpus search hits."
                ),
                "next_route": "promote only through reviewed object or generated-surface routing, not MCP authority",
            },
        }
    )
    return probes


def contract_only_access_probes() -> list[dict[str, Any]]:
    return [
        {
            "name": "live-mcp-probes",
            "kind": "workspace_required",
            "status": "not_run",
            "checks": {"live_mcp_required_for_currentness": False},
            "details": {
                "run": "python scripts/memory/build_memory_operational_readouts.py --check --live"
            },
        }
    ]


def build_access_plane_currentness(*, live: bool) -> dict[str, Any]:
    probes = live_access_probes() if live else contract_only_access_probes()
    failed = [probe for probe in probes if probe["status"] == "failed"]
    known_gaps = [probe for probe in probes if probe["status"] == "known_gap"]
    passed = [probe for probe in probes if probe["status"] == "passed"]
    if failed:
        overall = "failed"
    elif known_gaps:
        overall = "passed_with_known_gaps"
    elif passed:
        overall = "passed"
    else:
        overall = "contract_only"
    return {
        "schema_version": "aoa_memo_access_plane_currentness_v1",
        "surface_kind": "memo_access_plane_currentness_readout",
        "owner_repo": "aoa-memo",
        "runtime_owner": "abyss-stack",
        "generated_by": GENERATED_BY,
        "source_owner_split": {
            "memo_owns": "expected memory contracts, generated read-model refs, and currentness interpretation",
            "runtime_owner": "abyss-stack owns aoa_memo MCP service implementation and deployment",
            "workspace_map_owner": "8Dionysus owns workspace memory overlay map generation",
            "not_claimed": "MCP output is evidence or plan, not durable memory truth",
        },
        "source_refs": [
            "docs/memory/MEMORY_OPERATION_CYCLE.md#mcp-access-plane",
            "docs/decisions/AOA-MEM-D-0065-reviewed-memory-consumer-handoff-spine.md",
            "generated/memory-objects/memory_object_catalog.min.json",
            "generated/memory-objects/memory_object_capsules.json",
            "generated/quests/quest_catalog.min.json",
            "generated/quests/quest_dispatch.min.json",
            WORKSPACE_MAP_REF,
            MCP_SOURCE_HINT,
        ],
        "checked_surfaces": [
            "generated/memory-objects/memory_object_catalog.min.json",
            "generated/memory-objects/memory_object_capsules.json",
            "generated/quests/quest_catalog.min.json",
            "generated/quests/quest_dispatch.min.json",
            WORKSPACE_MAP_REF,
            MCP_SOURCE_HINT,
        ],
        "probe_mode": "live_mcp" if live else "contract_only",
        "probes": probes,
        "summary": {
            "probes_total": len(probes),
            "passed": len(passed),
            "known_gaps": len(known_gaps),
            "failed": len(failed),
            "overall_status": overall,
        },
        "quest_closure": {
            "quest_id": "AOA-MEM-Q-0010",
            "close_condition": "MCP brief/search/status path compared to current generated surfaces with drift routed",
            "result": "done" if overall in {"passed", "passed_with_known_gaps"} else "blocked",
        },
    }
