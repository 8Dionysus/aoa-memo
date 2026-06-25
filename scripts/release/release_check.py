#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validation_lanes

REPO_ROOT = Path(__file__).resolve().parents[2]


def _env() -> dict[str, str]:
    env = os.environ.copy()
    for env_var, repo_name in (
        ("AOA_AGENTS_ROOT", "aoa-agents"),
        ("AOA_EVALS_ROOT", "aoa-evals"),
        ("ABYSS_MACHINE_REPO_ROOT", "abyss-machine"),
    ):
        candidates = [
            env.get(env_var),
            str((REPO_ROOT / ".deps" / repo_name).resolve()),
            str((REPO_ROOT.parent / repo_name).resolve()),
        ]
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                env[env_var] = str(Path(candidate).resolve())
                break
    return env


RELEASE_CHECK_COMMAND_SEQUENCE = validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE
COMMANDS = tuple((step.label, step.command) for step in RELEASE_CHECK_COMMAND_SEQUENCE)


def resolve_command(command: Sequence[str]) -> tuple[str, ...]:
    if command and command[0] == "python":
        return (sys.executable, *command[1:])
    return tuple(command)


def run_step(label: str, command: Sequence[str]) -> int:
    resolved = resolve_command(command)
    print(f"[run] {label}: {subprocess.list2cmdline(resolved)}", flush=True)
    completed = subprocess.run(resolved, cwd=REPO_ROOT, env=_env(), check=False)
    if completed.returncode != 0:
        print(f"[error] {label} failed with exit code {completed.returncode}", flush=True)
        return completed.returncode
    print(f"[ok] {label}", flush=True)
    return 0


def main() -> int:
    for label, command in COMMANDS:
        exit_code = run_step(label, command)
        if exit_code != 0:
            return exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
