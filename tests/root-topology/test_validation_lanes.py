from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validation_lanes  # noqa: E402


LANES_PATH = REPO_ROOT / "config" / "validation_lanes.json"


def test_validation_lanes_manifest_loads_and_names_owner() -> None:
    payload = json.loads(LANES_PATH.read_text(encoding="utf-8"))

    assert payload["schema_version"] == 2
    assert payload["owner"] == "docs/validation/VALIDATOR_TOPOLOGY.md"
    assert payload["testing_inventory_ref"] == "docs/testing/test_inventory.json"
    assert payload["command_authority"] == "config/validation_lanes.json"
    assert payload["ci_modes"]["release"] == "release_check"


def test_release_check_sequence_is_composed_from_named_lanes() -> None:
    expected = (
        *validation_lanes.RELEASE_OPS_COMMAND_SEQUENCE,
        *validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE,
        *validation_lanes.MEMORY_CONTEXT_COMMAND_SEQUENCE,
        *validation_lanes.RUNTIME_COMMAND_SEQUENCE,
        *validation_lanes.EXPORT_RUNTIME_COMMAND_SEQUENCE,
        *validation_lanes.INTER_AGENT_HANDOFF_COMMAND_SEQUENCE,
        *validation_lanes.EVAL_COMMAND_SEQUENCE,
        *validation_lanes.GENERATED_COMMAND_SEQUENCE,
        *validation_lanes.AUDIT_COMMAND_SEQUENCE,
        *validation_lanes.TEST_COMMAND_SEQUENCE,
    )

    assert validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE == expected
    assert validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE[-1].command == (
        "python",
        "-m",
        "pytest",
        "-q",
    )


def test_ci_modes_resolve_to_known_sequences() -> None:
    assert validation_lanes.ci_modes() == (
        "audit",
        "eval",
        "export/runtime",
        "generated",
        "handoff",
        "mechanics",
        "memory",
        "nightly",
        "post-merge",
        "release",
        "runtime",
        "security",
        "source-fast",
        "tests",
    )

    for mode in validation_lanes.ci_modes():
        sequence_name = validation_lanes.ci_mode_sequence_name(mode)
        assert validation_lanes.command_sequence(sequence_name)


def test_command_steps_carry_boundary_metadata() -> None:
    for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE:
        assert step.layer
        assert step.mode in {"blocking", "blocking-in-release", "boundary-only", "advisory"}
        assert step.owner_surface
        assert step.failure_route

    assert {step.layer for step in validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE} == {
        "source_topology"
    }
    assert {step.layer for step in validation_lanes.GENERATED_COMMAND_SEQUENCE} == {
        "projection_generated"
    }


def test_command_paths_are_repo_local_and_existing_when_file_backed() -> None:
    for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE:
        command = step.command
        assert command
        assert all(part for part in command)
        if command[0] != "python":
            continue
        if len(command) < 2 or command[1] == "-m":
            continue
        path = Path(command[1])
        assert not path.is_absolute(), step
        assert ".." not in path.parts, step
        assert (REPO_ROOT / path).exists(), step
