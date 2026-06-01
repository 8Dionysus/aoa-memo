from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validation_lanes  # noqa: E402

RELEASE_CHECK_PATH = REPO_ROOT / "scripts" / "release" / "release_check.py"
spec = importlib.util.spec_from_file_location("memo_release_check", RELEASE_CHECK_PATH)
release_check = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(release_check)


def test_resolve_command_uses_current_python_executable() -> None:
    assert release_check.resolve_command(("python", "scripts/memory/validate_memo.py")) == (
        sys.executable,
        "scripts/memory/validate_memo.py",
    )
    assert release_check.resolve_command(("git", "status")) == ("git", "status")


def test_release_check_uses_validation_lanes_manifest() -> None:
    assert release_check.RELEASE_CHECK_COMMAND_SEQUENCE is validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE
    assert release_check.COMMANDS == tuple(
        (step.label, step.command) for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE
    )


def test_main_runs_release_commands_in_manifest_order() -> None:
    calls: list[tuple[str, tuple[str, ...]]] = []

    def fake_run(label: str, command: tuple[str, ...]) -> int:
        calls.append((label, command))
        return 0

    stdout = io.StringIO()
    with mock.patch.object(release_check, "run_step", side_effect=fake_run), contextlib.redirect_stdout(stdout):
        exit_code = release_check.main()

    assert exit_code == 0
    assert calls == [(step.label, step.command) for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE]


def test_main_stops_on_first_failing_step() -> None:
    first = validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE[0]

    with mock.patch.object(release_check, "run_step", return_value=7) as run_step:
        exit_code = release_check.main()

    assert exit_code == 7
    run_step.assert_called_once_with(first.label, first.command)
