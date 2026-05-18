#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _env() -> dict[str, str]:
    env = os.environ.copy()
    for env_var, repo_name in (("AOA_AGENTS_ROOT", "aoa-agents"), ("AOA_EVALS_ROOT", "aoa-evals")):
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


COMMANDS = [
    ("check generated quest surfaces", [sys.executable, "scripts/build_quest_surfaces.py", "--check"]),
    ("validate memo", [sys.executable, "scripts/validate_memo.py"]),
    ("validate Agon memo prebindings", [sys.executable, "mechanics/agon/scripts/validate_agon_memo_prebindings.py"]),
    ("validate Agon epistemic memo bridge", [sys.executable, "mechanics/agon/scripts/validate_agon_epistemic_memo_bridge.py"]),
    ("validate Agon KAG memo evidence package registry", [sys.executable, "mechanics/agon/scripts/validate_agon_kag_memo_evidence_package_registry.py"]),
    ("validate Agon mechanical trial memo intakes", [sys.executable, "mechanics/agon/scripts/validate_agon_mechanical_trial_memo_intakes.py"]),
    ("validate Agon retention-rank memo bridge", [sys.executable, "mechanics/agon/scripts/validate_agon_retention_rank_memo_bridge.py"]),
    ("validate Agon SLC memo bridge registry", [sys.executable, "mechanics/agon/scripts/validate_agon_slc_memo_bridge_registry.py"]),
    ("validate Agon Sophian memo evidence registry", [sys.executable, "mechanics/agon/scripts/validate_agon_sophian_memo_evidence_registry.py"]),
    ("validate Agon VDS memo bridge", [sys.executable, "mechanics/agon/scripts/validate_agon_vds_memo_bridge.py"]),
    ("validate memory surfaces", [sys.executable, "scripts/validate_memory_surfaces.py"]),
    ("validate memory object surfaces", [sys.executable, "scripts/validate_memory_object_surfaces.py"]),
    ("validate lifecycle audit examples", [sys.executable, "scripts/validate_lifecycle_audit_examples.py"]),
    ("validate AGENTS mesh", [sys.executable, "scripts/validate_agents_mesh.py"]),
    ("check AGENTS mesh index", [sys.executable, "scripts/build_agents_mesh_index.py", "--check"]),
    ("validate AGENTS mesh index", [sys.executable, "scripts/validate_agents_mesh_index.py"]),
    ("validate docs districts", [sys.executable, "scripts/validate_docs_districts.py"]),
    ("validate memo mechanics", [sys.executable, "scripts/validate_memo_mechanics.py"]),
    ("check memo mechanics index", [sys.executable, "scripts/build_memo_mechanics_index.py", "--check"]),
    ("validate memo mechanics index", [sys.executable, "scripts/validate_memo_mechanics_index.py"]),
    ("run tests", [sys.executable, "-m", "pytest", "-q"]),
]


def run_step(label: str, command: list[str]) -> int:
    print(f"[run] {label}: {subprocess.list2cmdline(command)}", flush=True)
    completed = subprocess.run(command, cwd=REPO_ROOT, env=_env(), check=False)
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
