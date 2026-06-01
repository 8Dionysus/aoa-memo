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
COMMAND_AUTHORITY_PATH = REPO_ROOT / "docs" / "validation" / "COMMAND_AUTHORITY.md"
INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "validator_inventory.json"
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
REQUIRED_INVENTORY_FIELDS = {
    "family", "paths", "protects", "owner_surface", "layer",
    "lane", "mode", "callers", "failure_route", "status",
}
ALLOWED_INVENTORY_MODES = {
    "advisory", "blocking", "blocking-in-release", "blocking-orchestrator",
    "blocking-when-called", "blocking-with-check", "boundary-only",
}
ALLOWED_INVENTORY_STATUS = {"active", "compatibility", "manual"}
VALIDATION_ENTRYPOINT_NAMES = {"ci_gate.py", "release_check.py", "validation_lanes.py"}
VALIDATION_ENTRYPOINT_ROOTS = ("scripts", ".agents", "mechanics")
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
    "docs/validation/validator_inventory.json",
    "docs/validation/COMMAND_AUTHORITY.md",
)


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_inventory() -> dict[str, Any]:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


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


def split_layer_ids(value: object) -> set[str]:
    if not isinstance(value, str) or not value:
        return set()
    return {part for part in value.split("/") if part}


def inventoried_paths(inventory: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for entry in inventory.get("entries", []):
        if not isinstance(entry, dict):
            continue
        for path in entry.get("paths", []):
            if isinstance(path, str):
                paths.add(path)
    return paths


def discovered_validation_entrypoints() -> set[str]:
    paths: set[str] = set()
    for root_name in VALIDATION_ENTRYPOINT_ROOTS:
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            if path.name.startswith("validate") or path.name in VALIDATION_ENTRYPOINT_NAMES:
                paths.add(path.relative_to(REPO_ROOT).as_posix())
    return paths


def lane_command_file_paths(manifest: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    sequences = manifest.get("command_sequences")
    if not isinstance(sequences, dict):
        return paths
    for sequence in sequences.values():
        if not isinstance(sequence, list):
            continue
        for step in sequence:
            if not isinstance(step, dict):
                continue
            command = step.get("command")
            if not isinstance(command, list) or len(command) < 2:
                continue
            if command[0] != "python" or command[1] == "-m":
                continue
            path = Path(str(command[1]))
            if path.is_absolute() or ".." in path.parts:
                continue
            if (REPO_ROOT / path).is_file():
                paths.add(path.as_posix())
    return paths


def validate_command_authority_doc() -> list[str]:
    if not COMMAND_AUTHORITY_PATH.is_file():
        return ["docs/validation/COMMAND_AUTHORITY.md is missing"]
    text = COMMAND_AUTHORITY_PATH.read_text(encoding="utf-8")
    required = (
        "config/validation_lanes.json", "docs/validation/validator_inventory.json",
        "scripts/validation_lanes.py", "Do not put full validation command blocks",
    )
    return [
        f"docs/validation/COMMAND_AUTHORITY.md must mention {snippet!r}"
        for snippet in required
        if snippet not in text
    ]


def validate_inventory_shape(manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not INVENTORY_PATH.is_file():
        return ["docs/validation/validator_inventory.json is missing"]
    inventory = load_inventory()
    if inventory.get("schema_version") != 1:
        issues.append("docs/validation/validator_inventory.json schema_version must be 1")
    if inventory.get("owner") != "docs/validation/VALIDATOR_TOPOLOGY.md":
        issues.append("docs/validation/validator_inventory.json owner must be docs/validation/VALIDATOR_TOPOLOGY.md")
    if inventory.get("command_authority") != "config/validation_lanes.json":
        issues.append("docs/validation/validator_inventory.json command_authority must be config/validation_lanes.json")
    if set(inventory.get("required_fields", [])) != REQUIRED_INVENTORY_FIELDS:
        issues.append("docs/validation/validator_inventory.json required_fields are out of sync")

    entries = inventory.get("entries")
    if not isinstance(entries, list) or not entries:
        return issues + ["docs/validation/validator_inventory.json entries must be a non-empty list"]

    seen_paths: set[str] = set()
    for index, entry in enumerate(entries):
        where = f"validator_inventory.entries[{index}]"
        if not isinstance(entry, dict):
            issues.append(f"{where} must be an object")
            continue
        missing_fields = sorted(REQUIRED_INVENTORY_FIELDS - set(entry))
        if missing_fields:
            issues.append(f"{where} missing required fields: " + ", ".join(missing_fields))
        for field in ("family", "protects", "lane", "failure_route", "status"):
            if not isinstance(entry.get(field), str) or not entry[field]:
                issues.append(f"{where}.{field} must be a non-empty string")
        if entry.get("mode") not in ALLOWED_INVENTORY_MODES:
            issues.append(f"{where}.mode has unsupported value")
        if entry.get("status") not in ALLOWED_INVENTORY_STATUS:
            issues.append(f"{where}.status has unsupported value")
        layer_ids = split_layer_ids(entry.get("layer"))
        if not layer_ids:
            issues.append(f"{where}.layer must name at least one validator layer")
        else:
            unknown_layers = sorted(layer_ids - REQUIRED_LAYERS)
            if unknown_layers:
                issues.append(f"{where}.layer has unknown layers: " + ", ".join(unknown_layers))
        if not local_ref_exists(entry.get("owner_surface")):
            issues.append(f"{where}.owner_surface points to a missing local surface")
        append_string_list_errors(issues, value=entry.get("callers"), where=f"{where}.callers")
        paths = entry.get("paths")
        if not isinstance(paths, list) or not paths:
            issues.append(f"{where}.paths must be a non-empty list")
            continue
        for path_text in paths:
            if not isinstance(path_text, str) or not path_text:
                issues.append(f"{where}.paths contains a non-empty string violation")
                continue
            path = Path(path_text)
            if path.is_absolute() or ".." in path.parts:
                issues.append(f"{where}.paths contains non-local path {path_text!r}")
                continue
            if path_text in seen_paths:
                issues.append(f"{path_text} appears more than once in validator inventory")
            seen_paths.add(path_text)
            if not (REPO_ROOT / path).exists():
                issues.append(f"{path_text} is listed in validator inventory but missing")

    inventoried = inventoried_paths(inventory)
    missing_entrypoints = sorted(discovered_validation_entrypoints() - inventoried)
    if missing_entrypoints:
        issues.append("validator inventory missing validation entrypoints: " + ", ".join(missing_entrypoints))
    missing_lane_paths = sorted(lane_command_file_paths(manifest) - inventoried)
    if missing_lane_paths:
        issues.append("validator inventory missing lane command files: " + ", ".join(missing_lane_paths))
    return issues
