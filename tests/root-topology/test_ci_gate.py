from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import ci_gate  # noqa: E402
import validation_lanes  # noqa: E402


def test_source_fast_mode_runs_source_fast_sequence() -> None:
    calls: list[tuple[str, tuple[str, ...]]] = []

    def fake_run(label: str, command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
        calls.append((label, command))

    with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
        ci_gate.run_mode("source-fast")

    assert calls == [(step.label, step.command) for step in validation_lanes.SOURCE_FAST_COMMAND_SEQUENCE]


def test_release_mode_runs_composed_release_sequence() -> None:
    calls: list[tuple[str, tuple[str, ...]]] = []

    def fake_run(label: str, command: tuple[str, ...], repo_root: Path = ci_gate.REPO_ROOT) -> None:
        calls.append((label, command))

    with mock.patch.object(ci_gate, "run_command", side_effect=fake_run):
        ci_gate.run_mode("release")

    assert calls == [(step.label, step.command) for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE]


def test_parse_args_accepts_manifest_modes() -> None:
    args = ci_gate.parse_args(["--mode", "memory"])

    assert args.mode == "memory"
