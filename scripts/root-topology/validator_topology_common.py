from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validation_lanes


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "config" / "validation_lanes.json"
TOPOLOGY_PATH = REPO_ROOT / "docs" / "validation" / "VALIDATOR_TOPOLOGY.md"
MEMO_VALIDATOR_CLI = REPO_ROOT / "scripts" / "memory" / "validate_memo.py"
MEMO_VALIDATOR_MODULE_DIR = REPO_ROOT / "scripts" / "memory" / "validators"
MEMO_VALIDATOR_CLI_MAX_LINES = 120
MEMO_VALIDATOR_MODULE_MAX_LINES = 750
REQUIRED_MEMO_VALIDATOR_MODULES = {
    "__init__.py",
    "_shared.py",
    "eval_boundary.py",
    "handoff_boundary.py",
    "memory_context.py",
    "profiles.py",
    "questbook.py",
    "runtime_boundary.py",
    "runtime_receipts.py",
    "runtime_writeback.py",
    "schema.py",
}

REQUIRED_LAYERS = {
    "source_topology",
    "projection_generated",
    "capability_permission",
    "runtime_policy",
    "trace_eval",
    "memory_context",
    "inter_agent_handoff",
    "observability_audit",
    "security_adversarial",
    "release_operations",
}
REQUIRED_CI_MODES = {
    "source-fast",
    "generated",
    "export/runtime",
    "runtime",
    "memory",
    "handoff",
    "eval",
    "audit",
    "release",
    "nightly",
    "post-merge",
}
ALLOWED_OWNERSHIP = {"owned", "boundary-only", "routed"}
ALLOWED_GATE_ROLES = {
    "hard",
    "boundary",
    "regression",
    "promoted-audit",
    "release",
}
ALLOWED_STEP_MODES = {"blocking", "blocking-in-release", "boundary-only", "advisory"}
SOURCE_FAST_ALLOWED_LAYERS = {"source_topology"}
RELEASE_REQUIRED_LAYERS = {
    "source_topology",
    "projection_generated",
    "capability_permission",
    "runtime_policy",
    "trace_eval",
    "memory_context",
    "inter_agent_handoff",
    "observability_audit",
    "release_operations",
}
TOPOLOGY_REQUIRED_SNIPPETS = (
    "Source/Topology Validators",
    "Projection/Generated Validators",
    "Capability/Permission Validators",
    "Runtime Policy Validators",
    "Trace/Eval Validators",
    "Memory/RAG/Context Validators",
    "Inter-Agent/Handoff Validators",
    "Observability/Audit Validators",
    "Security/Adversarial Validators",
    "Release/Nightly/Post-Merge Validators",
    "Generated validators do not own source meaning.",
    "Prompt-only guardrails are not a security boundary.",
    "Do not add a single `validate_everything.py`.",
    "The profile implementations live under `scripts/memory/validators/`",
)


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def local_ref_exists(ref: object) -> bool:
    if not isinstance(ref, str) or not ref:
        return False
    if ":" in ref.split("/", 1)[0]:
        return True
    path_text = ref.split("#", 1)[0]
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        return False
    return (REPO_ROOT / path).exists()


def append_string_list_errors(
    issues: list[str],
    *,
    value: object,
    where: str,
) -> None:
    if not isinstance(value, list) or not value:
        issues.append(f"{where} must be a non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            issues.append(f"{where}[{index}] must be a non-empty string")


def expanded_layers(sequence_name: str) -> set[str]:
    return {step.layer for step in validation_lanes.command_sequence(sequence_name)}


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())
