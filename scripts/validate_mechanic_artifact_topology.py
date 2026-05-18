#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_ROOT_PREFIXES = {
    "config": ("agon_",),
    "examples": (
        "adoption_",
        "agon_",
        "assistant_revision_",
        "bridge.kag-lift",
        "certification_",
        "checkpoint_",
        "checkpoint_to_memory_contract",
        "claim.tos-bridge-ready",
        "cross_repo_retention_",
        "deployment_",
        "decision.phase-alpha-self-agent-checkpoint",
        "episode.tos-interpretation",
        "failure_lesson_",
        "audit_event.phase-alpha-self-agent-checkpoint",
        "federation_",
        "first_office_",
        "governance_",
        "inquiry_checkpoint",
        "memo_to_kag_",
        "memory_readiness_boundary_contract",
        "memory_chunk_face",
        "memory_eval_guardrail",
        "memory_graph_face",
        "office_retention_",
        "pattern.antifragility",
        "pattern_lineage_",
        "phase_alpha_writeback_",
        "policy_precedent_",
        "post_release_",
        "provenance_thread.a2a",
        "provenance_thread.kag",
        "provenance_thread.self-agency",
        "quest_chronicle",
        "recovery_pattern_",
        "release_revision_",
        "revocation_",
        "rollback_",
        "service_",
        "shared_lesson_",
        "titan_",
        "train_release_",
        "witness_trace",
    ),
    "generated": (
        "agon_",
        "growth_refinery_",
        "kag_export",
        "phase_alpha_writeback_",
        "runtime_writeback_",
    ),
    "schemas": (
        "adoption_",
        "agon",
        "assistant_revision_",
        "certification_",
        "checkpoint-to-memory",
        "cross_repo_retention_",
        "deployment_",
        "failure_lesson_",
        "federation_",
        "first_office_",
        "governance_",
        "inquiry_checkpoint",
        "memo_to_kag_",
        "memory_readiness_boundary_contract",
        "memory_chunk_face",
        "memory_eval_guardrail",
        "memory_graph_face",
        "office_retention_",
        "pattern_lineage_",
        "policy_precedent_",
        "post_release_",
        "quest_chronicle",
        "recovery_pattern_",
        "release_revision_",
        "revocation_",
        "rollback_",
        "runtime-writeback",
        "service_",
        "shared_lesson_",
        "titan_",
        "train_release_",
        "witness-trace",
    ),
    "scripts": (
        "build_agon_",
        "generate_growth_refinery_",
        "generate_kag_export",
        "generate_phase_alpha_",
        "generate_runtime_writeback_",
        "publish_live_receipts",
        "validate_agon_",
    ),
    "tests": (
        "test_adoption_",
        "test_agon_",
        "test_antifragility_",
        "test_consumer_handoff_",
        "test_checkpoint_",
        "test_wave1_boundary_contract",
        "test_governance_mechanic",
        "test_growth_refinery_",
        "test_lineage_harvest_",
        "test_operational_gate_",
        "test_playbook_memory_scopes",
        "test_publish_live_receipts",
        "test_quest_chronicle_",
        "test_recurrence_support_",
        "test_shape_guard_",
        "test_titan_",
    ),
}


def root_files(directory: str) -> list[Path]:
    root = REPO_ROOT / directory
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name != "AGENTS.md"
        and "__pycache__" not in path.relative_to(REPO_ROOT).parts
    )


def validate() -> list[str]:
    issues: list[str] = []

    for directory, prefixes in FORBIDDEN_ROOT_PREFIXES.items():
        for path in root_files(directory):
            if path.name.startswith(prefixes):
                relative = path.relative_to(REPO_ROOT).as_posix()
                issues.append(
                    f"{relative}: single-mechanic artifact must live under mechanics/<slug>/"
                )

    for path in root_files("manifests"):
        relative = path.relative_to(REPO_ROOT).as_posix()
        issues.append(f"{relative}: root manifests are reserved for shared manifests only")

    return issues


def main() -> int:
    issues = validate()
    if issues:
        print("Mechanic artifact topology validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] mechanic artifact topology is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
