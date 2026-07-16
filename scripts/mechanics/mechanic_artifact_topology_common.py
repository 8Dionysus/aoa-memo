from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT_DISTRICTS_CONFIG = REPO_ROOT / "config" / "root-topology" / "root_technical_districts.json"
ROOT_DISTRICTS_SCHEMA_VERSION = "aoa_memo_root_technical_districts_v11"
ROOT_TECHNICAL_DISTRICTS = (
    "config",
    "evals",
    "examples",
    "generated",
    "kag",
    "manifests",
    "schemas",
    "skills",
    "scripts",
    "tests",
)
GENERATED_SOURCE_KINDS = {
    "source-authored",
    "checked-in-derived",
    "generator-backed",
    "projection",
}
BUILDER_REQUIRED_GENERATED_SOURCE_KINDS = {"generator-backed", "projection"}
SCRIPT_FAMILY_ROLES = {
    "docs-and-agent-validator",
    "mechanic-artifact-validator",
    "mechanic-validator",
    "orchestrator",
    "route-card-validator",
    "validator-and-generator",
}
TEST_FAMILY_ROLES = {
    "cross-mechanic-contract-regression",
    "downstream-contract-regression",
    "local-memo-port-regression",
    "mechanic-contract-regression",
    "memory-object-regression",
    "route-and-topology-regression",
}
SCHEMA_FAMILY_ROLES = {
    "generated-surface-contract",
    "local-memo-port-contract",
    "memory-object-contract",
    "recall-posture-contract",
    "support-object-contract",
}
EXAMPLE_FAMILY_ROLES = {
    "base-memory-object-example",
    "continuity-relay-example",
    "lifecycle-audit-example",
    "local-memo-port-example",
    "phase-alpha-thread-example",
    "recall-contract-example",
    "support-contract-example",
    "surface-manifest-example",
}
CONFIG_FAMILY_ROLES = {
    "local-memo-port-vocabulary",
    "mechanic-index-source-map",
    "route-card-source-map",
    "technical-district-source-map",
    "validation-lane-source-map",
}
MANIFEST_POLICY_ROLE = "reserved-shared-recurrence-manifest-home"

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
        "test_stage1_boundary_contract",
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
        return None, ["config/root-topology/root_technical_districts.json is missing"]
    try:
        payload = json.loads(ROOT_DISTRICTS_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"config/root-topology/root_technical_districts.json is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return None, ["config/root-topology/root_technical_districts.json must be a JSON object"]
    return payload, []


def as_string_list(value: object, label: str, issues: list[str]) -> list[str] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        issues.append(f"config/root-topology/root_technical_districts.json: {label} must be a string array")
        return None
    return value


def validate_local_ref(path_text: object, label: str) -> list[str]:
    if not isinstance(path_text, str) or not path_text:
        return [f"config/root-topology/root_technical_districts.json: {label} must be a local path"]
    path_without_anchor = path_text.split("#", 1)[0]
    path = Path(path_without_anchor)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        return [f"config/root-topology/root_technical_districts.json: {label} must stay inside the repo: {path_text}"]
    target = (REPO_ROOT / path).resolve()
    try:
        target.relative_to(REPO_ROOT)
    except ValueError:
        return [f"config/root-topology/root_technical_districts.json: {label} resolves outside repo: {path_text}"]
    if not target.exists():
        return [f"config/root-topology/root_technical_districts.json: {label} points to missing path {path_text}"]
    return []
