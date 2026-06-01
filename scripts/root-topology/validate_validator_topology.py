#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


def _load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _local_ref_exists(ref: object) -> bool:
    if not isinstance(ref, str) or not ref:
        return False
    if ":" in ref.split("/", 1)[0]:
        return True
    path_text = ref.split("#", 1)[0]
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        return False
    return (REPO_ROOT / path).exists()


def _append_string_list_errors(
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


def _expanded_layers(sequence_name: str) -> set[str]:
    return {step.layer for step in validation_lanes.command_sequence(sequence_name)}


def validate_topology_doc() -> list[str]:
    issues: list[str] = []
    if not TOPOLOGY_PATH.is_file():
        return [f"{TOPOLOGY_PATH.relative_to(REPO_ROOT).as_posix()} is missing"]
    text = TOPOLOGY_PATH.read_text(encoding="utf-8")
    for snippet in TOPOLOGY_REQUIRED_SNIPPETS:
        if snippet not in text:
            issues.append(f"docs/validation/VALIDATOR_TOPOLOGY.md must mention {snippet!r}")
    return issues


def validate_manifest_shape(manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if manifest.get("schema_version") != 2:
        issues.append("config/validation_lanes.json schema_version must be 2")
    if manifest.get("owner") != "docs/validation/VALIDATOR_TOPOLOGY.md":
        issues.append("config/validation_lanes.json owner must be docs/validation/VALIDATOR_TOPOLOGY.md")
    if manifest.get("testing_inventory_ref") != "docs/testing/test_inventory.json":
        issues.append("config/validation_lanes.json must route test inventory to docs/testing/test_inventory.json")

    layers = manifest.get("validator_layers")
    if not isinstance(layers, dict):
        return issues + ["validator_layers must be a mapping"]
    missing_layers = sorted(REQUIRED_LAYERS - set(layers))
    extra_layers = sorted(set(layers) - REQUIRED_LAYERS)
    if missing_layers:
        issues.append("validator_layers missing required ids: " + ", ".join(missing_layers))
    if extra_layers:
        issues.append("validator_layers has unexpected ids: " + ", ".join(extra_layers))

    for layer_id, layer in sorted(layers.items()):
        if not isinstance(layer, dict):
            issues.append(f"validator_layers.{layer_id} must be an object")
            continue
        for field in ("title", "purpose", "route", "owner_surface"):
            if not isinstance(layer.get(field), str) or not layer[field]:
                issues.append(f"validator_layers.{layer_id}.{field} must be a non-empty string")
        if layer.get("ownership") not in ALLOWED_OWNERSHIP:
            issues.append(f"validator_layers.{layer_id}.ownership has unsupported value")
        if layer.get("gate_role") not in ALLOWED_GATE_ROLES:
            issues.append(f"validator_layers.{layer_id}.gate_role has unsupported value")
        if not _local_ref_exists(layer.get("owner_surface")):
            issues.append(f"validator_layers.{layer_id}.owner_surface points to a missing local surface")
        _append_string_list_errors(issues, value=layer.get("checks"), where=f"validator_layers.{layer_id}.checks")
        _append_string_list_errors(issues, value=layer.get("must_not"), where=f"validator_layers.{layer_id}.must_not")

    return issues


def validate_sequences(manifest: dict[str, Any], *, scope: str) -> list[str]:
    issues: list[str] = []
    sequences = manifest.get("command_sequences")
    defaults = manifest.get("sequence_defaults")
    compositions = manifest.get("sequence_compositions")
    ci_modes = manifest.get("ci_modes")
    if not isinstance(sequences, dict):
        return ["command_sequences must be a mapping"]
    if not isinstance(defaults, dict):
        return ["sequence_defaults must be a mapping"]
    if not isinstance(compositions, dict):
        return ["sequence_compositions must be a mapping"]
    if not isinstance(ci_modes, dict):
        return ["ci_modes must be a mapping"]

    for sequence_name in sequences:
        default = defaults.get(sequence_name)
        if not isinstance(default, dict):
            issues.append(f"sequence_defaults.{sequence_name} must exist")
            continue
        if default.get("layer") not in REQUIRED_LAYERS:
            issues.append(f"sequence_defaults.{sequence_name}.layer must name a validator layer")
        if default.get("mode") not in ALLOWED_STEP_MODES:
            issues.append(f"sequence_defaults.{sequence_name}.mode has unsupported value")
        if not _local_ref_exists(default.get("owner_surface")):
            issues.append(f"sequence_defaults.{sequence_name}.owner_surface points to a missing local surface")
        if not isinstance(default.get("failure_route"), str) or not default["failure_route"]:
            issues.append(f"sequence_defaults.{sequence_name}.failure_route must be a non-empty string")

    missing_modes = sorted(REQUIRED_CI_MODES - set(ci_modes))
    if missing_modes:
        issues.append("ci_modes missing required modes: " + ", ".join(missing_modes))

    for mode, sequence_name in sorted(ci_modes.items()):
        if not isinstance(sequence_name, str) or not sequence_name:
            issues.append(f"ci_modes.{mode} must name a sequence")
        elif sequence_name not in sequences and sequence_name not in compositions:
            issues.append(f"ci_modes.{mode} points to unknown sequence {sequence_name!r}")

    for sequence_name, sequence in sorted(sequences.items()):
        if not isinstance(sequence, list) or not sequence:
            issues.append(f"command_sequences.{sequence_name} must be a non-empty list")
            continue
        for index, step in enumerate(sequence):
            where = f"command_sequences.{sequence_name}[{index}]"
            if not isinstance(step, dict):
                issues.append(f"{where} must be an object")
                continue
            command = step.get("command")
            if not isinstance(command, list) or not command:
                issues.append(f"{where}.command must be a non-empty list")
                continue
            if command[0] == "python" and len(command) > 1 and command[1] != "-m":
                path = Path(command[1])
                if path.is_absolute() or ".." in path.parts or not (REPO_ROOT / path).exists():
                    issues.append(f"{where}.command points to a missing repo-local script")

    if scope in {"all", "source-fast"}:
        source_fast_layers = _expanded_layers("source_fast")
        if not source_fast_layers <= SOURCE_FAST_ALLOWED_LAYERS:
            issues.append("source_fast may only contain source_topology commands")
        generated_layers = _expanded_layers("generated")
        if generated_layers != {"projection_generated"}:
            issues.append("generated sequence may only contain projection_generated commands")

    if scope in {"all", "release-ops"}:
        release_layers = _expanded_layers("release_check")
        missing_release_layers = sorted(RELEASE_REQUIRED_LAYERS - release_layers)
        if missing_release_layers:
            issues.append("release_check missing required layer coverage: " + ", ".join(missing_release_layers))

        release_steps = validation_lanes.command_sequence("release_check")
        for step in release_steps:
            if step.layer == "observability_audit" and step.mode != "blocking-in-release":
                issues.append(f"{step.label}: audit steps in release must be blocking-in-release")
            if step.mode == "advisory":
                issues.append(f"{step.label}: advisory steps must not be in release_check")
            if step.command[:2] == ("python", "scripts/memory/validate_memo.py"):
                if "--profile" not in step.command:
                    issues.append(f"{step.label}: release must not call unprofiled validate_memo.py")
                else:
                    profile = step.command[step.command.index("--profile") + 1]
                    if profile == "all":
                        issues.append(f"{step.label}: release must not call validate_memo.py --profile all")

        labels = [step.label for step in release_steps]
        if len(labels) != len(set(labels)):
            issues.append("release_check contains duplicate step labels")

    return issues


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def validate_memo_validator_module_split() -> list[str]:
    issues: list[str] = []
    if not MEMO_VALIDATOR_CLI.is_file():
        return ["scripts/memory/validate_memo.py is missing"]
    if not (MEMO_VALIDATOR_MODULE_DIR / "AGENTS.md").is_file():
        issues.append("scripts/memory/validators/AGENTS.md is missing")
    if not MEMO_VALIDATOR_MODULE_DIR.is_dir():
        return issues + ["scripts/memory/validators/ directory is missing"]

    cli_lines = _line_count(MEMO_VALIDATOR_CLI)
    if cli_lines > MEMO_VALIDATOR_CLI_MAX_LINES:
        issues.append(
            f"scripts/memory/validate_memo.py must stay a thin CLI "
            f"({cli_lines} lines > {MEMO_VALIDATOR_CLI_MAX_LINES})"
        )
    cli_text = MEMO_VALIDATOR_CLI.read_text(encoding="utf-8")
    if "profiles.run_profile" not in cli_text:
        issues.append("scripts/memory/validate_memo.py must dispatch through validators.profiles")
    if "Draft202012Validator" in cli_text or "def validate_schema_profile" in cli_text:
        issues.append("scripts/memory/validate_memo.py must not own schema implementation logic")

    actual_modules = {path.name for path in MEMO_VALIDATOR_MODULE_DIR.glob("*.py")}
    missing_modules = sorted(REQUIRED_MEMO_VALIDATOR_MODULES - actual_modules)
    if missing_modules:
        issues.append("scripts/memory/validators missing modules: " + ", ".join(missing_modules))
    for module_name in sorted(REQUIRED_MEMO_VALIDATOR_MODULES & actual_modules):
        module_path = MEMO_VALIDATOR_MODULE_DIR / module_name
        module_lines = _line_count(module_path)
        if module_lines > MEMO_VALIDATOR_MODULE_MAX_LINES:
            issues.append(
                f"scripts/memory/validators/{module_name} is too large for a layer module "
                f"({module_lines} lines > {MEMO_VALIDATOR_MODULE_MAX_LINES})"
            )
    return issues


def validate(scope: str = "all") -> list[str]:
    manifest = _load_manifest()
    issues = []
    issues.extend(validate_topology_doc())
    issues.extend(validate_manifest_shape(manifest))
    issues.extend(validate_sequences(manifest, scope=scope))
    issues.extend(validate_memo_validator_module_split())
    return issues


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate aoa-memo validator topology.")
    parser.add_argument(
        "--scope",
        choices=("all", "source-fast", "release-ops"),
        default="all",
        help="Run only the topology checks needed by a focused lane.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    issues = validate(scope=args.scope)
    if issues:
        print("Validator topology validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print(f"[ok] validator topology ({args.scope})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
