from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
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


def test_validator_topology_layers_are_named_in_manifest() -> None:
    payload = json.loads((REPO_ROOT / "config" / "validation_lanes.json").read_text(encoding="utf-8"))

    assert set(payload["validator_layers"]) == REQUIRED_LAYERS
    assert payload["validator_layers"]["projection_generated"]["must_not"]
    assert "source meaning" in " ".join(payload["validator_layers"]["projection_generated"]["must_not"])
    assert payload["validator_layers"]["security_adversarial"]["gate_role"] == "boundary"


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


def test_release_and_nightly_are_distinct_compositions() -> None:
    release_labels = [step.label for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE]
    nightly_labels = [step.label for step in validation_lanes.NIGHTLY_COMMAND_SEQUENCE]

    assert release_labels[-1] == "run tests"
    assert "run tests" not in nightly_labels
    assert validation_lanes.POST_MERGE_COMMAND_SEQUENCE[-1].label == "run tests"
    assert "validate memory operations security boundary" in nightly_labels
    assert "validate memory operations security boundary" not in release_labels
    assert release_labels[0] == "validate release, nightly, and post-merge composition"
