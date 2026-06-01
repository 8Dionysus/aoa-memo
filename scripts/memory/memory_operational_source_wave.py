from __future__ import annotations

from typing import Any

from memory_operational_readout_common import GENERATED_BY, object_index, object_ref


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
        "generated_by": GENERATED_BY,
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
            "docs/decisions/AOA-MEM-D-0066-distributed-memory-organ-foundation.md",
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
