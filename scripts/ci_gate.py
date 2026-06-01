#!/usr/bin/env python3
"""Run named validation lanes for aoa-memo."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

import validation_lanes


REPO_ROOT = Path(__file__).resolve().parents[1]


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


def run_command(label: str, command: Sequence[str], repo_root: Path = REPO_ROOT) -> None:
    resolved = resolve_command(command)
    printable = subprocess.list2cmdline(resolved)
    print(f"[ci-gate] {label}: {printable}", flush=True)
    subprocess.run(resolved, cwd=repo_root, env=_env(repo_root), check=True)


def run_sequence(sequence_name: str) -> None:
    for step in validation_lanes.command_sequence(sequence_name):
        run_command(step.label, step.command)


def run_mode(mode: str) -> None:
    run_sequence(validation_lanes.ci_mode_sequence_name(mode))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run validation lanes for aoa-memo.")
    parser.add_argument("--mode", choices=validation_lanes.ci_modes(), required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        run_mode(args.mode)
    except subprocess.CalledProcessError as exc:
        print(f"[ci-gate] command failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
