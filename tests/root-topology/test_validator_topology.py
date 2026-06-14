from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import types
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_INVENTORY_PATH = REPO_ROOT / "docs" / "validation" / "validator_inventory.json"
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validation_lanes  # noqa: E402


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


def test_validator_topology_validator_passes() -> None:
    completed = subprocess.run(
        (sys.executable, "scripts/root-topology/validate_validator_topology.py"),
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_validator_topology_entrypoint_stays_split() -> None:
    entrypoint = REPO_ROOT / "scripts" / "root-topology" / "validate_validator_topology.py"
    common = REPO_ROOT / "scripts" / "root-topology" / "validator_topology_common.py"

    assert common.is_file()
    assert len(entrypoint.read_text(encoding="utf-8").splitlines()) <= 300


def test_validator_topology_layers_are_named_in_manifest() -> None:
    payload = json.loads((REPO_ROOT / "config" / "validation_lanes.json").read_text(encoding="utf-8"))

    assert set(payload["validator_layers"]) == REQUIRED_LAYERS
    assert payload["validator_layers"]["projection_generated"]["must_not"]
    assert "source meaning" in " ".join(payload["validator_layers"]["projection_generated"]["must_not"])
    assert payload["validator_layers"]["security_adversarial"]["gate_role"] == "boundary"


def test_validator_inventory_records_entrypoint_authority() -> None:
    payload = json.loads(VALIDATOR_INVENTORY_PATH.read_text(encoding="utf-8"))
    paths = {
        path
        for entry in payload["entries"]
        for path in entry["paths"]
    }

    assert payload["owner"] == "docs/validation/VALIDATOR_TOPOLOGY.md"
    assert payload["command_authority"] == "config/validation_lanes.json"
    assert "scripts/memory/validate_memo.py" in paths
    assert "scripts/ci_gate.py" in paths
    assert "scripts/release/release_check.py" in paths
    assert "scripts/memory/validators/schema.py" not in paths


def test_source_fast_and_generated_lanes_keep_their_boundaries() -> None:
    assert {step.layer for step in validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE} == {
        "source_topology"
    }
    assert {step.layer for step in validation_lanes.GENERATED_COMMAND_SEQUENCE} == {
        "projection_generated"
    }
    assert "scripts/root-topology/validate_validator_topology.py" in {
        step.command[1]
        for step in validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE
        if len(step.command) > 1
    }


def test_release_uses_profiled_memory_validator_instead_of_monolith() -> None:
    for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE:
        if step.command[:2] != ("python", "scripts/memory/validate_memo.py"):
            continue
        assert "--profile" in step.command, step
        assert step.command[step.command.index("--profile") + 1] != "all", step


def test_memo_validator_entrypoint_stays_thin_and_layer_owned() -> None:
    entrypoint = REPO_ROOT / "scripts" / "memory" / "validate_memo.py"
    module_dir = REPO_ROOT / "scripts" / "memory" / "validators"

    assert len(entrypoint.read_text(encoding="utf-8").splitlines()) <= 120
    assert (module_dir / "AGENTS.md").is_file()
    assert {path.name for path in module_dir.glob("*.py")} >= {
        "_shared.py",
        "schema.py",
        "memory_context.py",
        "questbook.py",
        "runtime_boundary.py",
        "runtime_receipts.py",
        "runtime_writeback.py",
        "handoff_boundary.py",
        "eval_boundary.py",
        "profiles.py",
    }
    for path in module_dir.glob("*.py"):
        assert len(path.read_text(encoding="utf-8").splitlines()) <= 750, path


def test_memo_validator_entrypoint_ignores_preloaded_top_level_validators(
    monkeypatch,
) -> None:
    entrypoint = REPO_ROOT / "scripts" / "memory" / "validate_memo.py"
    module_name = "_validate_memo_import_probe"
    spec = importlib.util.spec_from_file_location(module_name, entrypoint)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "validators", types.ModuleType("validators"))
    monkeypatch.setitem(sys.modules, module_name, module)

    spec.loader.exec_module(module)

    assert "schema" in module.PROFILE_NAMES


def test_release_and_nightly_are_distinct_compositions() -> None:
    release_labels = [step.label for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE]
    nightly_labels = [step.label for step in validation_lanes.NIGHTLY_COMMAND_SEQUENCE]

    assert release_labels[-1] == "run tests"
    assert "run tests" not in nightly_labels
    assert validation_lanes.POST_MERGE_COMMAND_SEQUENCE[-1].label == "run tests"
    assert "validate memory operations security boundary" in nightly_labels
    assert "validate memory operations security boundary" not in release_labels
    assert release_labels[0] == "validate release, nightly, and post-merge composition"
