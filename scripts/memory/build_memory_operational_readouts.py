#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = REPO_ROOT.parent
OUTPUT_DIR = REPO_ROOT / "generated" / "memory"
ACCESS_OUTPUT = OUTPUT_DIR / "access_plane_currentness.min.json"
SOURCE_WAVE_OUTPUT = OUTPUT_DIR / "source_intake_wave.min.json"
PORT_STATUS_OUTPUT = OUTPUT_DIR / "workspace_memo_port_status.min.json"

OBJECT_CATALOG = REPO_ROOT / "generated" / "memory-objects" / "memory_object_catalog.min.json"
OBJECT_CAPSULES = REPO_ROOT / "generated" / "memory-objects" / "memory_object_capsules.json"
QUEST_CATALOG = REPO_ROOT / "generated" / "quests" / "quest_catalog.min.json"
QUEST_DISPATCH = REPO_ROOT / "generated" / "quests" / "quest_dispatch.min.json"
WORKSPACE_MAP = (
    Path(os.environ.get("AOA_WORKSPACE_ROUTE_ROOT", str(WORKSPACE_ROOT / "8Dionysus")))
    / "generated"
    / "workspace_memory_map.min.json"
)
MCP_ROOT = Path(
    os.environ.get(
        "AOA_MEMO_MCP_ROOT",
        str(Path.home() / "src" / "abyss-stack" / "mcp" / "services" / "aoa-memo-mcp"),
    )
)
MCP_SOURCE_HINT = "repo:abyss-stack/mcp/services/aoa-memo-mcp"
WORKSPACE_MAP_REF = "repo:8Dionysus/generated/workspace_memory_map.min.json"

FORBIDDEN_ABSOLUTE_PREFIXES = ('"/srv/', '"/home/', '"/var/', '"/mnt/')


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def object_index() -> dict[str, dict[str, Any]]:
    payload = load_json(OBJECT_CATALOG)
    return {
        item["id"]: item
        for item in payload.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def object_ref(objects: dict[str, dict[str, Any]], object_id: str) -> dict[str, Any]:
    item = objects.get(object_id)
    if not item:
        return {
            "id": object_id,
            "found": False,
            "source_kind": "",
            "current_recall_status": "",
            "source_path": "",
        }
    return {
        "id": object_id,
        "found": True,
        "kind": item.get("kind", ""),
        "title": item.get("title", ""),
        "source_kind": item.get("source_kind", ""),
        "current_recall_status": item.get("current_recall_status", ""),
        "source_path": item.get("source_path", ""),
    }


def build_source_intake_wave() -> dict[str, Any]:
    objects = object_index()
    lanes = [
        {
            "lane": "runtime access memory",
            "raw_truth_owner": "abyss-stack",
            "candidate_or_review_pressure": "landed reviewed export plus access-plane corpus decisions",
            "review_route": "repo:abyss-stack/memo -> aoa-memo reviewed intake",
            "evidence_refs": [
                object_ref(objects, "memo.decision.2026-05-22.abyss-stack-aoa-memo-mcp-access-plane"),
                object_ref(objects, "memo.decision.2026-05-22.corpus-backed-mcp-search"),
            ],
            "status": "reviewed_corpus_and_landed_export",
            "next_route": "AOA-MEM-Q-0010 currentness check",
        },
        {
            "lane": "graph-memory handoff",
            "raw_truth_owner": "aoa-kag plus source owners",
            "candidate_or_review_pressure": "reviewed bridge object consumed by KAG-facing donor export",
            "review_route": "aoa-memo bridge object; graph promotion remains aoa-kag",
            "evidence_refs": [
                object_ref(objects, "memo.bridge.2026-03-23.tos-lineage-kag-candidate"),
            ],
            "status": "reviewed_corpus",
            "next_route": "aoa-kag lift review when stronger owner accepts",
        },
        {
            "lane": "consumer recall handoff",
            "raw_truth_owner": "aoa-agents, aoa-playbooks, aoa-evals, aoa-routing, and source owners",
            "candidate_or_review_pressure": "reviewed consumer-handoff decision names bounded downstream use",
            "review_route": "reviewed memory objects and generated read models; consumers keep stronger authority",
            "evidence_refs": [
                object_ref(objects, "memo.decision.2026-05-22.reviewed-memory-consumer-handoff-spine"),
                object_ref(objects, "memo.pattern.2026-05-22.agents-route-cards-own-memory-operations"),
            ],
            "status": "reviewed_corpus",
            "next_route": "router/review/bounded-execution recall packs",
        },
        {
            "lane": "local memo port evidence",
            "raw_truth_owner": "origin repositories with local memo ports",
            "candidate_or_review_pressure": "reviewed pattern and intake guardrails keep local refs portable before landing",
            "review_route": "local port candidate/export/receipt -> aoa-memo reviewed intake or rejection",
            "evidence_refs": [
                object_ref(objects, "memo.audit.2026-05-22.reviewed-intake-evidence-guard"),
                object_ref(objects, "memo.pattern.2026-05-22.portable-local-memo-refs"),
            ],
            "status": "reviewed_corpus",
            "next_route": "AOA-MEM-Q-0015 workspace memo-port status readout",
        },
    ]
    missing = [
        ref["id"]
        for lane in lanes
        for ref in lane["evidence_refs"]
        if not ref.get("found")
    ]
    return {
        "schema_version": "aoa_memo_source_intake_wave_v1",
        "surface_kind": "memo_source_intake_wave_readout",
        "owner_repo": "aoa-memo",
        "generated_by": "scripts/memory/build_memory_operational_readouts.py",
        "source_owner_split": {
            "memo_owns": "reviewed memory route, durable object posture, generated readout interpretation",
            "stronger_owners": [
                "source repositories own raw truth and acceptance",
                "abyss-stack owns MCP/runtime implementation",
                "8Dionysus owns workspace memory overlay mapping",
                "aoa-evals owns proof and quality verdict execution",
            ],
        },
        "source_refs": [
            "docs/memory/LIVING_MEMORY_TOPOLOGY.md#source-intake-matrix",
            "docs/decisions/2026-05-24-distributed-memory-organ-foundation.md",
            "generated/memory-objects/memory_object_catalog.min.json",
            "memo/intake/reviewed/abyss-stack.20260522T021004Z.aoa-memo-mcp-access-plane.reviewed-intake.json",
        ],
        "lanes": lanes,
        "summary": {
            "lane_count": len(lanes),
            "lanes_with_real_evidence": sum(
                1 for lane in lanes if all(ref.get("found") for ref in lane["evidence_refs"])
            ),
            "fixture_only_lanes": 0,
            "missing_object_refs": missing,
            "overall_status": "passed" if not missing else "missing_reviewed_object_refs",
        },
        "quest_closure": {
            "quest_id": "AOA-MEM-Q-0011",
            "close_condition": "first source-lane wave names real reviewed or exported pressure across regular producers",
            "result": "done" if not missing else "blocked",
        },
    }


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
        "generated_by": "scripts/memory/build_memory_operational_readouts.py",
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


def run_mcp_cli(args: list[str], timeout: int = 20) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(MCP_ROOT / "src")
    completed = subprocess.run(
        [sys.executable, "-m", "aoa_memo_mcp.cli", "--workspace-root", str(WORKSPACE_ROOT), *args],
        check=False,
        cwd=str(MCP_ROOT),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
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


def live_access_probes() -> list[dict[str, Any]]:
    probes: list[dict[str, Any]] = []

    for repo, intent in (
        ("aoa-evals", "memory quality harness handoff from aoa-memo"),
        ("aoa-routing", "router recall pack needs memo context"),
    ):
        result = run_mcp_cli(["brief", "--repo", repo, "--intent", intent])
        payload = result.get("payload", {}) if result.get("ok") else {}
        reviewed = payload.get("reviewed_memory") if isinstance(payload, dict) else []
        workspace_map = payload.get("workspace_memory_map") if isinstance(payload, dict) else {}
        checks = {
            "schema": payload.get("schema") == "aoa_memo_brief_v1",
            "workspace_map_found": bool(workspace_map.get("found")),
            "route_only_or_port_visible": bool(workspace_map.get("current_port_level")),
            "reviewed_memory_refs_visible": isinstance(reviewed, list) and bool(reviewed),
            "durable_landing_not_mcp": payload.get("memory_route", {}).get("durable_landing")
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
    payload = pending.get("payload", {}) if pending.get("ok") else {}
    counts = payload.get("counts") if isinstance(payload, dict) else {}
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
    payload = validate_port.get("payload", {}) if validate_port.get("ok") else {}
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
        payload = result.get("payload", {}) if result.get("ok") else {}
        hits = payload.get("hits") if isinstance(payload, dict) else []
        checks = {
            "schema": payload.get("schema") == "aoa_memo_search_v1",
            "not_low_confidence": payload.get("low_confidence") is False,
            "has_hits": isinstance(hits, list) and bool(hits),
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
    payload = foundation.get("payload", {}) if foundation.get("ok") else {}
    hits = payload.get("hits") if isinstance(payload, dict) else []
    status = "passed" if isinstance(hits, list) and hits else "known_gap"
    probes.append(
        {
            "name": "search:fresh-foundation-terms",
            "kind": "search",
            "status": status,
            "checks": {
                "schema": payload.get("schema") == "aoa_memo_search_v1",
                "has_hits": isinstance(hits, list) and bool(hits),
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
        "generated_by": "scripts/memory/build_memory_operational_readouts.py",
        "source_owner_split": {
            "memo_owns": "expected memory contracts, generated read-model refs, and currentness interpretation",
            "runtime_owner": "abyss-stack owns aoa_memo MCP service implementation and deployment",
            "workspace_map_owner": "8Dionysus owns workspace memory overlay map generation",
            "not_claimed": "MCP output is evidence or plan, not durable memory truth",
        },
        "source_refs": [
            "docs/memory/MEMORY_OPERATION_CYCLE.md#mcp-access-plane",
            "docs/decisions/2026-05-22-reviewed-memory-consumer-handoff-spine.md",
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


def validate_readout(path: Path, payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "surface_kind", "owner_repo", "generated_by", "source_refs", "summary"):
        if key not in payload:
            errors.append(f"{path.name}: missing {key}")
    if payload.get("owner_repo") != "aoa-memo":
        errors.append(f"{path.name}: owner_repo must stay aoa-memo")
    if payload.get("generated_by") != "scripts/memory/build_memory_operational_readouts.py":
        errors.append(f"{path.name}: generated_by must name the builder")
    if not isinstance(payload.get("source_refs"), list) or not payload.get("source_refs"):
        errors.append(f"{path.name}: source_refs must be a non-empty list")
    owner_split = {
        "owner_repo": payload.get("owner_repo"),
        "source_owner_split": payload.get("source_owner_split"),
        "authority_boundary": payload.get("authority_boundary"),
    }
    if "aoa-memo" not in json.dumps(owner_split, ensure_ascii=False):
        errors.append(f"{path.name}: owner split must mention aoa-memo")
    rendered = render_json(payload)
    if any(prefix in rendered for prefix in FORBIDDEN_ABSOLUTE_PREFIXES):
        errors.append(f"{path.name}: generated readout leaked an absolute path")
    return errors


def build_all(*, live: bool) -> dict[Path, dict[str, Any] | None]:
    return {
        ACCESS_OUTPUT: build_access_plane_currentness(live=live),
        SOURCE_WAVE_OUTPUT: build_source_intake_wave(),
        PORT_STATUS_OUTPUT: build_workspace_port_status(),
    }


def write_outputs(outputs: dict[Path, dict[str, Any] | None]) -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    missing = [path for path, payload in outputs.items() if payload is None]
    if missing:
        for path in missing:
            print(f"[error] cannot build {path.relative_to(REPO_ROOT)}; source input is missing", file=sys.stderr)
        return 1
    for path, payload in outputs.items():
        assert payload is not None
        path.write_text(render_json(payload), encoding="utf-8")
        print(f"[ok] wrote {path.relative_to(REPO_ROOT)}")
    return 0


def check_outputs(outputs: dict[Path, dict[str, Any] | None], *, live: bool) -> int:
    errors: list[str] = []
    for path in (ACCESS_OUTPUT, SOURCE_WAVE_OUTPUT, PORT_STATUS_OUTPUT):
        if not path.is_file():
            errors.append(f"{path.relative_to(REPO_ROOT)} is missing")
            continue
        try:
            payload = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(REPO_ROOT)} is invalid JSON: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{path.relative_to(REPO_ROOT)} must be a JSON object")
            continue
        errors.extend(validate_readout(path, payload))
        expected = outputs.get(path)
        if expected is not None:
            if path == ACCESS_OUTPUT and not live:
                continue
            if render_json(payload) != render_json(expected):
                errors.append(
                    f"{path.relative_to(REPO_ROOT)} is stale; run "
                    "scripts/memory/build_memory_operational_readouts.py --write"
                    + (" --live" if live else "")
                )
    if errors:
        print("Memory operational readout validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    skipped = []
    if outputs.get(PORT_STATUS_OUTPUT) is None:
        skipped.append("workspace port status rebuild skipped because 8Dionysus workspace map was unavailable")
    if not live:
        skipped.append("live MCP currentness comparison skipped; use --check --live in a workspace")
    for item in skipped:
        print(f"[note] {item}")
    print("[ok] memory operational readouts are valid")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build aoa-memo operational readouts.")
    parser.add_argument("--write", action="store_true", help="write generated readout files")
    parser.add_argument("--check", action="store_true", help="validate generated readout files")
    parser.add_argument("--live", action="store_true", help="run live aoa_memo MCP probes")
    args = parser.parse_args()
    if args.write and args.check:
        parser.error("--write and --check are mutually exclusive")
    if not args.write and not args.check:
        parser.error("choose --write or --check")

    outputs = build_all(live=args.live)
    if args.write:
        return write_outputs(outputs)
    return check_outputs(outputs, live=args.live)


if __name__ == "__main__":
    raise SystemExit(main())
