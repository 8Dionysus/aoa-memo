#!/usr/bin/env python3
"""Run named validation lanes or bounded local edit feedback for aoa-memo."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Sequence

import validation_lanes


REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_TOPOLOGY_PATH = Path("config/root-topology/root_technical_districts.json")
TEST_INVENTORY_PATH = Path("docs/testing/test_inventory.json")


class FeedbackPathError(ValueError):
    """A caller supplied a path that is not a safe repository-relative path."""


_FEEDBACK_BOUNDARY_PATHS = frozenset({
    "scripts/ci_gate.py", "scripts/validation_lanes.py",
    "scripts/release/release_check.py", "scripts/release_check.py",
    "config/root-topology/root_technical_districts.json",
    "docs/testing/test_inventory.json", "docs/testing/TEST_TOPOLOGY.md",
    "docs/validation/COMMAND_AUTHORITY.md", "docs/validation/VALIDATOR_TOPOLOGY.md",
    "docs/validation/validator_inventory.json",
})
_FEEDBACK_ENVIRONMENT_NAMES = frozenset({
    "pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini", "noxfile.py",
    "requirements.txt", "requirements-dev.txt", "Pipfile", "Pipfile.lock",
    "poetry.lock", "uv.lock", ".python-version", ".tool-versions",
    "uv.toml", "setup.py", "mypy.ini", "ruff.toml", ".ruff.toml",
    ".pre-commit-config.yaml", "Dockerfile", "Makefile",
})


def _repo_relative_path(
    raw: object, repo_root: Path, *, label: str, metadata: bool = False,
    require_exists: bool = False,
) -> str:
    error = ValueError if metadata else FeedbackPathError
    if not isinstance(raw, str) or not raw or "\x00" in raw:
        raise error(f"{label} must be a non-empty repository-relative path")
    if any(ord(char) < 0x20 for char in raw) or "\\" in raw:
        raise error(f"{label} must use a safe POSIX repository path: {raw!r}")
    spelling = raw[:-1] if metadata and raw.endswith("/") else raw
    if metadata and raw.endswith("//"):
        raise error(f"{label} must use a canonical repository path: {raw!r}")
    path = PurePosixPath(spelling)
    if (
        path.is_absolute() or raw.startswith("//") or ".." in path.parts
        or not path.parts or path.as_posix() != spelling
        or (len(path.parts[0]) >= 2 and path.parts[0][1] == ":")
    ):
        raise error(f"{label} must be repository-relative: {raw!r}")
    root = repo_root.resolve()
    candidate = (root / path).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise error(f"{label} escapes the repository: {raw!r}") from exc
    if require_exists and not candidate.exists():
        raise ValueError(f"{label} does not exist: {raw!r}")
    return spelling


def _refs(value: object, repo_root: Path, where: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise ValueError(f"{where} must be a non-empty string list")
    return tuple(_repo_relative_path(
        item, repo_root, label=f"{where} reference", metadata=True, require_exists=True,
    ) for item in value)


def _load_feedback_maps(repo_root: Path):
    try:
        topology = json.loads((repo_root / ROOT_TOPOLOGY_PATH).read_text(encoding="utf-8"))
        inventory = json.loads((repo_root / TEST_INVENTORY_PATH).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read feedback metadata: {exc}") from exc
    if not isinstance(topology, dict) or not isinstance(inventory, dict):
        raise ValueError("feedback metadata must contain JSON objects")

    def pairs(value: object, left: str, right: str, where: str):
        if not isinstance(value, list) or not value:
            raise ValueError(f"{where} must be a non-empty list")
        result = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                raise ValueError(f"{where}[{index}] is malformed")
            result.append((
                _refs(item.get(left), repo_root, f"{where}[{index}].{left}"),
                _refs(item.get(right), repo_root, f"{where}[{index}].{right}"),
            ))
        return result

    scripts = pairs(topology.get("script_families"), "scripts", "covered_by", "script_families")
    families = pairs(topology.get("test_families"), "protects", "tests", "test_families")
    entries = []
    known: set[str] = set()
    raw_entries = inventory.get("entries")
    if not isinstance(raw_entries, list) or not raw_entries:
        raise ValueError("test_inventory.entries must be a non-empty list")
    for index, item in enumerate(raw_entries):
        if not isinstance(item, dict) or not isinstance(item.get("owner_surface"), str):
            raise ValueError(f"test_inventory.entries[{index}] is malformed")
        owner = item["owner_surface"].split("#", 1)[0]
        _repo_relative_path(owner, repo_root, label="test_inventory owner", metadata=True, require_exists=True)
        paths = _refs(item.get("paths"), repo_root, f"test_inventory.entries[{index}].paths")
        entries.append((owner, paths))
        known.update(path for path in paths if _is_test_path(path))
    for _, covered_by in scripts:
        known.update(path for path in covered_by if _is_test_path(path))
    for _, tests in families:
        known.update(path for path in tests if _is_test_path(path))
    return scripts, families, entries, known


def _is_test_path(path: str) -> bool:
    parsed = PurePosixPath(path)
    return parsed.suffix == ".py" and parsed.name.startswith("test")


def _matches(changed: str, reference: str) -> bool:
    return changed == reference or changed.startswith(reference.rstrip("/") + "/")


def _boundary_reason(path: str) -> str | None:
    parsed = PurePosixPath(path)
    if path in _FEEDBACK_BOUNDARY_PATHS:
        return "runner or selection metadata changed"
    if parsed.parts and parsed.parts[0] == "config":
        return "configuration/mapping input changed"
    if parsed.parts[:2] == ("scripts", "release"):
        return "release runner input changed"
    if parsed.parts and parsed.parts[0] == ".github":
        return "CI/environment input changed"
    if parsed.name == "conftest.py":
        return "pytest fixture/collection input changed"
    if parsed.parts[:1] in (("requirements",), ("constraints",)):
        return "test environment input changed"
    if parsed.name.startswith(("requirements", "constraints")):
        return "test environment input changed"
    if parsed.name in _FEEDBACK_ENVIRONMENT_NAMES or parsed.name.startswith(".env"):
        return "test environment input changed"
    return None


def _mechanic_tests(path: str, repo_root: Path, known: set[str]) -> tuple[str, ...] | None:
    parts = PurePosixPath(path).parts
    if not parts or parts[0] != "mechanics":
        return ()
    if len(parts) < 2:
        return None
    package = repo_root / "mechanics" / parts[1]
    if not package.is_dir():
        return None
    if len(parts) >= 3 and parts[2] != "parts":
        if len(parts) != 3 or parts[2] not in {"README.md", "AGENTS.md"}:
            return None
    part = repo_root / PurePosixPath(*parts[:4]) if len(parts) >= 4 and parts[2] == "parts" else None
    if part is not None and not part.is_dir() and parts[3] not in {"README.md", "AGENTS.md"}:
        return None
    roots = [part / "tests"] if part is not None and part.is_dir() else list(package.glob("parts/*/tests"))
    tests = tuple(sorted(
        candidate.relative_to(repo_root).as_posix()
        for root in roots if root.is_dir()
        for candidate in root.rglob("test*.py") if candidate.is_file()
    ))
    return tests if tests and set(tests) <= known else None


def _feedback_selection(
    changed_paths: Sequence[str], repo_root: Path = REPO_ROOT,
) -> tuple[list[str] | None, str]:
    if not changed_paths:
        raise FeedbackPathError("--feedback requires at least one --changed-path")
    normalized = tuple(dict.fromkeys(
        _repo_relative_path(raw, repo_root, label="changed path") for raw in changed_paths
    ))
    try:
        scripts, families, inventory, known = _load_feedback_maps(repo_root)
    except ValueError as exc:
        return None, f"invalid feedback metadata: {exc}"

    selected: set[str] = set()
    for path in normalized:
        reason = _boundary_reason(path)
        if reason:
            return None, f"{path}: {reason}"
        matched = False
        if path in known:
            matched = True
            selected.add(path)
        owner_matches = [paths for owner, paths in inventory if path == owner]
        family_matches = [tests for protects, tests in families if any(
            _matches(path, ref) for ref in protects
        )]
        script_matches = [covered_by for script_paths, covered_by in scripts if any(
            _matches(path, ref) for ref in script_paths
        )]
        if (
            len(owner_matches) > 1 or len(family_matches) > 1
            or len(script_matches) > 1 or (family_matches and script_matches)
        ):
            return None, f"{path}: shared or ambiguous mapping surface"
        for paths in owner_matches:
            matched = True
            selected.update(ref for ref in paths if _is_test_path(ref))
        for tests in family_matches:
            matched = True
            selected.update(ref for ref in tests if _is_test_path(ref))
        for covered_by in script_matches:
            matched = True
            selected.update(ref for ref in covered_by if _is_test_path(ref))

        tests = _mechanic_tests(path, repo_root, known)
        if tests is None:
            if path.startswith("mechanics/"):
                return None, f"{path}: mechanic territory is unknown or uncovered"
        elif tests:
            matched = True
            selected.update(tests)
        if not matched:
            return None, f"{path}: unknown or uncovered surface"
    return (sorted(selected), "") if selected else (None, "no registered affected tests")


def _env(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    env = os.environ.copy()
    for env_var, repo_name in (("AOA_AGENTS_ROOT", "aoa-agents"), ("AOA_EVALS_ROOT", "aoa-evals")):
        candidates = [
            env.get(env_var),
            str((repo_root / ".deps" / repo_name).resolve()),
            str((repo_root.parent / repo_name).resolve()),
        ]
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                env[env_var] = str(Path(candidate).resolve())
                break
    return env


def resolve_command(command: Sequence[str]) -> tuple[str, ...]:
    if command and command[0] == "python":
        return (sys.executable, *command[1:])
    return tuple(command)


def run_command(
    label: str,
    command: Sequence[str],
    repo_root: Path = REPO_ROOT,
    *,
    feedback: bool = False,
) -> None:
    resolved = resolve_command(command)
    printable = subprocess.list2cmdline(resolved)
    print(f"[ci-gate] {label}: {printable}", flush=True)
    env = _env(repo_root)
    if feedback:
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    subprocess.run(resolved, cwd=repo_root, env=env, check=True)


def run_sequence(sequence_name: str, repo_root: Path = REPO_ROOT) -> None:
    for step in validation_lanes.command_sequence(sequence_name):
        run_command(step.label, step.command, repo_root=repo_root)


def run_mode(mode: str, repo_root: Path = REPO_ROOT) -> None:
    run_sequence(validation_lanes.ci_mode_sequence_name(mode), repo_root=repo_root)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run validation lanes or bounded local edit feedback for aoa-memo."
    )
    route = parser.add_mutually_exclusive_group(required=True)
    route.add_argument("--mode", choices=validation_lanes.ci_modes())
    route.add_argument(
        "--feedback",
        action="store_true",
        help="Run affected owner tests only; uncertain surfaces use the full release lane.",
    )
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument(
        "--lf",
        "--last-failed",
        action="store_true",
        dest="last_failed",
        help="For feedback only, let ordinary pytest retry its cached last failures.",
    )
    args = parser.parse_args(argv)
    if args.feedback:
        if not args.changed_path:
            parser.error("--feedback requires at least one --changed-path")
    elif args.changed_path or args.last_failed:
        parser.error("--changed-path and --lf require --feedback")
    return args


def run_feedback(
    changed_paths: Sequence[str],
    *,
    last_failed: bool = False,
    repo_root: Path = REPO_ROOT,
) -> None:
    tests, reason = _feedback_selection(changed_paths, repo_root)
    changed = ", ".join(dict.fromkeys(changed_paths))
    if tests is None:
        print(
            f"[ci-gate] feedback: full release fallback for {changed}: {reason}",
            flush=True,
        )
        if last_failed:
            print(
                "[ci-gate] feedback: --lf ignored on full fallback; this remains the existing release lane",
                flush=True,
            )
        run_mode("release", repo_root=repo_root)
        return

    print(
        f"[ci-gate] feedback: selected {len(tests)} test files for {changed}; "
        "local advisory only",
        flush=True,
    )
    command: list[str] = ["python", "-m", "pytest", "-q"]
    if last_failed:
        print(
            "[ci-gate] feedback: --lf retries only pytest's cached failures; "
            "run without --lf for the complete affected set",
            flush=True,
        )
        command.append("--lf")
    command.extend(("--", *tests))
    run_command("feedback selected tests", command, repo_root=repo_root, feedback=True)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.feedback:
            run_feedback(
                args.changed_path,
                last_failed=args.last_failed,
                repo_root=REPO_ROOT,
            )
        else:
            run_mode(args.mode)
    except FeedbackPathError as exc:
        print(f"[ci-gate] invalid feedback path: {exc}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"[ci-gate] command failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
