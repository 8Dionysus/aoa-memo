from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[5]
MODULE_PATH = (
    REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "receipt-publication-regression"
    / "scripts"
    / "publish_live_receipts.py"
)
RECEIPT_FIXTURE_PATH = (
    REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "receipt-publication-regression"
    / "tests"
    / "fixtures"
    / "memo_writeback_receipts.example.jsonl"
)
MEMORY_OBJECT_CATALOG_PATH = (
    REPO_ROOT
    / "generated"
    / "memory-objects"
    / "memory_object_catalog.min.json"
)
MEMORY_OBJECT_CAPSULES_PATH = (
    REPO_ROOT
    / "generated"
    / "memory-objects"
    / "memory_object_capsules.json"
)
MEMORY_OBJECT_SECTIONS_PATH = (
    REPO_ROOT
    / "generated"
    / "memory-objects"
    / "memory_object_sections.full.json"
)
GROWTH_REFINERY_LANES_PATH = (
    REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "growth-and-continuity"
    / "generated"
    / "growth_refinery_writeback_lanes.min.json"
)
ADOPTED_OBJECT_ID = "memo.decision.2026-04-02.alpha-validation-remediation-rerun"
ADOPTED_RECALL_REF = (
    "repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#"
    "memo.decision.2026-04-02.alpha-validation-remediation-rerun"
)
REVIEWED_CANDIDATE_CASES = {
    "distillation_claim_candidate": {
        "object_id": "memo.claim.2026-04-03.phase-alpha-runtime-history-later-infra-track",
        "source_path": "examples/phase-alpha/claim.phase-alpha-runtime-history-later-infra-track.example.json",
        "target_kind": "claim",
        "review_state": "confirmed",
        "writeback_anchor_ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation.md",
        "candidate_source_ref": "repo:abyss-stack/Logs/phase-alpha/alpha-04-long-horizon-model-tier-orchestra/distillation_pack.md",
    },
    "distillation_pattern_candidate": {
        "object_id": "memo.pattern.2026-04-02.alpha-remediation-recurrence",
        "source_path": "examples/phase-alpha/pattern.phase-alpha-remediation-recurrence.example.json",
        "target_kind": "pattern",
        "review_state": "confirmed",
        "writeback_anchor_ref": "repo:aoa-playbooks/docs/alpha-reviewed-runs/2026-04-02.validation-driven-remediation-recall-rerun.md",
        "candidate_source_ref": "repo:abyss-stack/Logs/phase-alpha/alpha-04-long-horizon-model-tier-orchestra/distillation_pack.md",
    },
    "distillation_bridge_candidate": {
        "object_id": "memo.bridge.2026-03-23.tos-lineage-kag-candidate",
        "source_path": "memo/objects/bridges/2026/tos-lineage-kag-candidate/object.json",
        "target_kind": "bridge",
        "review_state": "confirmed",
        "writeback_anchor_ref": "repo:aoa-memo/mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow",
        "candidate_source_ref": "repo:aoa-memo/mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/claim.tos-bridge-ready.example.json",
    },
}
GROWTH_LANE_CASES = {
    "growth_refinery_failure_lesson": {
        "memory_id": "memo:session-growth-cycle-owner-reanchor-first",
        "source_path": "mechanics/antifragility/parts/failure-lesson-memory/examples/failure_lesson_memory.lineage.example.json",
        "target_kind": "failure_lesson",
        "review_status": "reviewed",
        "required_evidence_refs": [
            "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
            "aoa-playbooks:review_note_v1#AOA-P-0025:owner-reanchor",
            "aoa-sdk:closeout_context_lineage_v1#session-growth-cycle",
            "aoa-evals:aoa-owner-fit-routing-quality#report:session-growth-cycle",
            "Agents-of-Abyss:reviewable_growth_refinery_v1#owner-boundaries",
        ],
    },
    "growth_refinery_recovery_pattern": {
        "memory_id": "memo:session-growth-cycle-playbook-reanchor",
        "source_path": "mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.lineage.example.json",
        "target_kind": "recovery_pattern",
        "review_status": "reviewed",
        "required_evidence_refs": [
            "aoa-skills:harvest_packet_receipt_v1#candidate:aoa-playbooks:session-growth-cycle",
            "Dionysus:source_lineage_entry_v1#source:aoa:session-growth-cycle",
            "aoa-evals:aoa-candidate-lineage-integrity#report:session-growth-cycle",
            "aoa-evals:aoa-owner-fit-routing-quality#report:session-growth-cycle",
            "aoa-stats:candidate_lineage_summary_v1#summary:session-growth-cycle",
        ],
    },
}


def load_module():
    spec = importlib.util.spec_from_file_location("publish_live_receipts", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def build_receipt(event_kind: str = "memo_writeback_receipt") -> dict:
    return {
        "event_kind": event_kind,
        "event_id": "evt-memo-001",
        "observed_at": "2026-04-06T20:10:00Z",
        "run_ref": "run-memo-001",
        "session_ref": "session:test-memo-closeout",
        "actor_ref": "aoa-memo:runtime-writeback",
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "memory_object",
            "id": ADOPTED_OBJECT_ID,
            "version": "main",
        },
        "evidence_refs": [
            {
                "kind": "memory_object",
                "ref": ADOPTED_RECALL_REF,
            }
        ],
        "payload": {
            "target_kind": "decision",
            "writeback_class": "memo_surviving_event",
            "review_state": "confirmed",
        },
    }


def build_reviewed_candidate_receipt(runtime_surface: str) -> dict:
    case = REVIEWED_CANDIDATE_CASES[runtime_surface]
    object_id = case["object_id"]
    return {
        "event_kind": "memo_writeback_receipt",
        "event_id": f"evt-{runtime_surface}",
        "observed_at": "2026-04-13T21:05:00Z",
        "run_ref": "run-memo-reviewed-candidate-adoption-2026-04-13",
        "session_ref": "session:2026-04-13-reviewed-candidate-adoption",
        "actor_ref": "aoa-memo:runtime-writeback",
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "memory_object",
            "id": object_id,
            "version": "main",
        },
        "evidence_refs": [
            {
                "kind": "memory_object",
                "ref": f"repo:aoa-memo/{case['source_path']}",
                "role": "primary",
            },
            {
                "kind": "memory_catalog_entry",
                "ref": f"repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#{object_id}",
                "role": "catalog",
            },
            {
                "kind": "candidate_source",
                "ref": case["candidate_source_ref"],
                "role": "candidate-source",
            },
            {
                "kind": "review_anchor",
                "ref": case["writeback_anchor_ref"],
                "role": "writeback-anchor",
            },
        ],
        "payload": {
            "memory_object_ref": case["source_path"],
            "runtime_surface": runtime_surface,
            "review_state": case["review_state"],
            "target_kind": case["target_kind"],
            "writeback_anchor_ref": case["writeback_anchor_ref"],
            "writeback_class": "reviewed_candidate",
        },
    }


def build_growth_receipt(lane_ref: str) -> dict:
    case = GROWTH_LANE_CASES[lane_ref]
    source_path = case["source_path"]
    return {
        "event_kind": "memo_growth_writeback_receipt",
        "event_id": f"evt-{lane_ref}",
        "observed_at": "2026-04-14T00:05:00Z",
        "run_ref": "run-memo-growth-refinery-writeback-2026-04-14",
        "session_ref": "session:2026-04-14-growth-refinery-writeback",
        "actor_ref": "aoa-memo:growth-refinery-writeback",
        "object_ref": {
            "repo": "aoa-memo",
            "kind": "support_memory",
            "id": case["memory_id"],
            "version": "main",
        },
        "evidence_refs": [
            {
                "kind": "support_memory",
                "ref": f"repo:aoa-memo/{source_path}",
                "role": "primary",
            },
            {
                "kind": "growth_lane_entry",
                "ref": f"repo:aoa-memo/mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json#{lane_ref}",
                "role": "lane",
            },
        ]
        + [
            {
                "kind": "growth_evidence",
                "ref": ref,
                "role": "required-evidence",
            }
            for ref in case["required_evidence_refs"]
        ],
        "payload": {
            "growth_lane_ref": lane_ref,
            "source_example_ref": source_path,
            "target_kind": case["target_kind"],
            "review_status": case["review_status"],
            "writeback_class": "growth_refinery_memory",
        },
    }
