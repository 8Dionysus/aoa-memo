#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_DISTRICTS_CONFIG = REPO_ROOT / "config" / "root_technical_districts.json"
ROOT_TECHNICAL_DISTRICTS = (
    "config",
    "examples",
    "generated",
    "manifests",
    "schemas",
    "scripts",
    "tests",
)

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


def load_root_districts_config() -> tuple[dict[str, object] | None, list[str]]:
    if not ROOT_DISTRICTS_CONFIG.exists():
        return None, ["config/root_technical_districts.json is missing"]
    try:
        payload = json.loads(ROOT_DISTRICTS_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"config/root_technical_districts.json is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return None, ["config/root_technical_districts.json must be a JSON object"]
    return payload, []


def validate_root_district_allowlist() -> list[str]:
    issues: list[str] = []
    payload, config_errors = load_root_districts_config()
    issues.extend(config_errors)
    if payload is None:
        return issues

    if payload.get("schema_version") != "aoa_memo_root_technical_districts_v1":
        issues.append("config/root_technical_districts.json must keep schema_version aoa_memo_root_technical_districts_v1")
    if payload.get("source_of_truth") != "mechanics/ARTIFACT_TOPOLOGY.md":
        issues.append("config/root_technical_districts.json must route source_of_truth to mechanics/ARTIFACT_TOPOLOGY.md")

    districts = payload.get("districts")
    if not isinstance(districts, dict):
        issues.append("config/root_technical_districts.json: districts must be an object")
        return issues

    missing_districts = sorted(set(ROOT_TECHNICAL_DISTRICTS) - set(districts))
    extra_districts = sorted(set(districts) - set(ROOT_TECHNICAL_DISTRICTS))
    for district in missing_districts:
        issues.append(f"config/root_technical_districts.json: missing district {district}")
    for district in extra_districts:
        issues.append(f"config/root_technical_districts.json: unsupported district {district}")

    for district in ROOT_TECHNICAL_DISTRICTS:
        config = districts.get(district)
        if not isinstance(config, dict):
            if district in districts:
                issues.append(f"config/root_technical_districts.json: {district} must be an object")
            continue
        if not isinstance(config.get("root_role"), str) or not config.get("root_role"):
            issues.append(f"config/root_technical_districts.json: {district} must name root_role")
        allowed_files = config.get("allowed_files")
        if not isinstance(allowed_files, list) or not all(isinstance(item, str) for item in allowed_files):
            issues.append(f"config/root_technical_districts.json: {district}.allowed_files must be a string array")
            continue

        duplicate_paths = sorted({item for item in allowed_files if allowed_files.count(item) > 1})
        for duplicate_path in duplicate_paths:
            issues.append(f"config/root_technical_districts.json: duplicate allowed path {duplicate_path}")

        allowed = set(allowed_files)
        for allowed_path in allowed:
            parts = Path(allowed_path).parts
            if not parts or parts[0] != district:
                issues.append(f"config/root_technical_districts.json: {allowed_path} is outside district {district}")
            if Path(allowed_path).name == "AGENTS.md":
                issues.append(f"config/root_technical_districts.json: {allowed_path} should rely on the route-card exception, not allowed_files")

        actual = {path.relative_to(REPO_ROOT).as_posix() for path in root_files(district)}
        for missing in sorted(allowed - actual):
            issues.append(f"{missing}: allowed root technical artifact is missing")
        for unexpected in sorted(actual - allowed):
            issues.append(
                f"{unexpected}: root technical artifact must be listed in config/root_technical_districts.json or moved under mechanics/<slug>/"
            )

    return issues


def validate() -> list[str]:
    issues: list[str] = []
    issues.extend(validate_root_district_allowlist())

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
