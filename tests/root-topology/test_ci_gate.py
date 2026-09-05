from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

import pytest


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


def test_parse_args_accepts_repeated_feedback_paths() -> None:
    args = ci_gate.parse_args(["--feedback", "--changed-path", "a", "--changed-path", "b", "--lf"])

    assert args.changed_path == ["a", "b"]
    assert args.last_failed is True


PART_SCHEMA = (
    "mechanics/adoption/parts/adoption-boundary/schemas/"
    "adoption_memory_writeback_v1.json"
)
PART_TEST = "mechanics/adoption/parts/adoption-boundary/tests/test_adoption_boundary_contracts.py"


def test_feedback_unions_part_tests_and_protecting_root_family() -> None:
    paths, _ = ci_gate._feedback_selection([PART_SCHEMA])

    assert paths is not None
    assert PART_TEST in paths
    assert "tests/mechanics/test_cross_mechanic_candidate_contracts.py" in paths
    assert len(paths) == len(set(paths))


def test_feedback_uses_script_family_and_owner_inventory() -> None:
    paths, _ = ci_gate._feedback_selection(["scripts/memory/validate_memo.py"])

    assert paths is not None
    assert "tests/memory/test_memo_schema_contracts.py" in paths
    assert "tests/memory/test_memo_memory_context_boundaries.py" in paths
    assert len(paths) == len(set(paths))


def test_feedback_unions_multiple_changed_surfaces_from_actual_maps() -> None:
    paths, _ = ci_gate._feedback_selection([PART_SCHEMA, "scripts/memory/validate_memo.py"])

    assert paths is not None
    assert PART_TEST in paths
    assert "tests/mechanics/test_cross_mechanic_candidate_contracts.py" in paths
    assert "tests/memory/test_memo_schema_contracts.py" in paths
    assert "tests/memory/test_memo_memory_context_boundaries.py" in paths
    assert len(paths) == len(set(paths))


def test_feedback_known_surface_plus_unknown_surface_falls_back() -> None:
    paths, reason = ci_gate._feedback_selection([PART_SCHEMA, "unknown/new.py"])

    assert paths is None
    assert "unknown/new.py" in reason


@pytest.mark.parametrize(
    "path",
    [
        "unknown/new.py",
        "scripts/ci_gate.py",
        "config/validation_lanes.json",
        "pytest.ini",
        "conftest.py",
        ".github/workflows/repo-validation.yml",
        "requirements/base.txt",
        "mechanics/adoption/unknown/new_source.py",
        "scripts/memory/build_local_memo_port_index.py",
    ],
)
def test_feedback_expands_uncertain_surfaces_to_full_release(path: str) -> None:
    assert ci_gate._feedback_selection([path])[0] is None


@pytest.mark.parametrize(
    "path",
    [
        "",
        "../outside.py",
        "/tmp/outside.py",
        "bad\\path.py",
        "foo/./bar.py",
        "foo//bar.py",
        "bad\x00path.py",
    ],
)
def test_feedback_rejects_unsafe_changed_paths(path: str) -> None:
    with pytest.raises(ci_gate.FeedbackPathError):
        ci_gate._feedback_selection([path])


@pytest.mark.parametrize("path", ["../outside.py", "foo//bar.py", "bad\\path.py"])
def test_feedback_rejects_unsafe_metadata_references(path: str) -> None:
    with pytest.raises(ValueError):
        ci_gate._repo_relative_path(
            path, ci_gate.REPO_ROOT, label="metadata reference", metadata=True,
        )


def test_feedback_last_failed_is_only_added_to_targeted_pytest(monkeypatch) -> None:
    calls: list[tuple[str, list[str]]] = []

    def fake_run(
        label: str,
        command: list[str],
        repo_root: Path = ci_gate.REPO_ROOT,
        *,
        feedback: bool = False,
    ) -> None:
        calls.append((label, command))

    monkeypatch.setattr(ci_gate, "run_command", fake_run)
    ci_gate.run_feedback([PART_SCHEMA], last_failed=True)

    assert calls == [
        (
            "feedback selected tests",
            [
                "python",
                "-m",
                "pytest",
                "-q",
                "--lf",
                "--",
                PART_TEST,
                "tests/mechanics/test_cross_mechanic_candidate_contracts.py",
            ],
        )
    ]


def test_feedback_uses_bounded_pytest_environment(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_run(*args, **kwargs) -> None:
        captured.update(kwargs)

    monkeypatch.setattr(ci_gate.subprocess, "run", fake_run)
    ci_gate.run_command("feedback", ["python", "-m", "pytest", "-q"], feedback=True)

    assert captured["env"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] == "1"


def test_feedback_fallback_uses_existing_release_mode(monkeypatch) -> None:
    calls: list[tuple[str, Path]] = []

    def fake_mode(mode: str, repo_root: Path = ci_gate.REPO_ROOT) -> None:
        calls.append((mode, repo_root))

    monkeypatch.setattr(ci_gate, "run_mode", fake_mode)
    ci_gate.run_feedback(["unknown/new.py"], last_failed=True)

    assert calls == [("release", ci_gate.REPO_ROOT)]


def test_feedback_metadata_failure_falls_back_closed(monkeypatch) -> None:
    def broken_maps(_repo_root: Path):
        raise ValueError("test metadata failure")

    monkeypatch.setattr(ci_gate, "_load_feedback_maps", broken_maps)
    paths, reason = ci_gate._feedback_selection([PART_SCHEMA])

    assert paths is None
    assert "invalid feedback metadata" in reason
