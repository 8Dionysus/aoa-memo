#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


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
    ("validate quest store", [sys.executable, "mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py"]),
    ("check generated quest surfaces", [sys.executable, "mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py", "--check"]),
    ("validate memo", [sys.executable, "scripts/memory/validate_memo.py"]),
    ("validate memory operations", [sys.executable, "scripts/memory/validate_memory_operations.py"]),
    ("check memo port vocabulary", [sys.executable, "scripts/memory/build_memo_port_vocabulary.py", "--check"]),
    ("validate local memo port example", [sys.executable, "scripts/memory/validate_local_memo_port.py", "--path", "examples/memory-ports/example-port"]),
    ("check local memo port example index", [sys.executable, "scripts/memory/build_local_memo_port_index.py", "--path", "examples/memory-ports/example-port", "--check"]),
    ("validate Agon memo prebindings", [sys.executable, "mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py"]),
    ("validate Agon epistemic memo bridge", [sys.executable, "mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_epistemic_memo_bridge.py"]),
    ("validate Agon KAG memo evidence package registry", [sys.executable, "mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_kag_memo_evidence_package_registry.py"]),
    ("validate Agon mechanical trial memo intakes", [sys.executable, "mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_mechanical_trial_memo_intakes.py"]),
    ("validate Agon retention-rank memo bridge", [sys.executable, "mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_retention_rank_memo_bridge.py"]),
    ("validate Agon SLC memo bridge registry", [sys.executable, "mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_slc_memo_bridge_registry.py"]),
    ("validate Agon Sophian memo evidence registry", [sys.executable, "mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_sophian_memo_evidence_registry.py"]),
    ("validate Agon VDS memo bridge", [sys.executable, "mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_vds_memo_bridge.py"]),
    ("validate memory surfaces", [sys.executable, "scripts/memory/validate_memory_surfaces.py"]),
    ("check generated memory-object surfaces", [sys.executable, "scripts/memory/generate_memory_object_surfaces.py", "--check"]),
    ("validate memory object surfaces", [sys.executable, "scripts/memory/validate_memory_object_surfaces.py"]),
    ("validate lifecycle audit examples", [sys.executable, "scripts/memory/validate_lifecycle_audit_examples.py"]),
    ("validate Spark lane", [sys.executable, ".agents/spark/scripts/validate_spark_lane.py"]),
    ("run Spark lane tests", [sys.executable, "-m", "unittest", "discover", "-s", ".agents/spark/tests", "-p", "test*.py"]),
    ("validate mechanic artifact topology", [sys.executable, "scripts/mechanics/validate_mechanic_artifact_topology.py"]),
    ("check mechanic artifact inventory", [sys.executable, "scripts/mechanics/build_mechanic_artifact_inventory.py", "--check"]),
    ("validate mechanic artifact inventory", [sys.executable, "scripts/mechanics/validate_mechanic_artifact_inventory.py"]),
    ("check root technical districts index", [sys.executable, "scripts/root-topology/build_root_technical_districts_index.py", "--check"]),
    ("validate root technical districts index", [sys.executable, "scripts/root-topology/validate_root_technical_districts_index.py"]),
    ("validate AGENTS mesh", [sys.executable, "scripts/agents/validate_agents_mesh.py"]),
    ("check AGENTS mesh index", [sys.executable, "scripts/agents/build_agents_mesh_index.py", "--check"]),
    ("validate AGENTS mesh index", [sys.executable, "scripts/agents/validate_agents_mesh_index.py"]),
    ("validate semantic AGENTS docs", [sys.executable, "scripts/agents/validate_semantic_agents.py"]),
    ("validate docs districts", [sys.executable, "scripts/root-topology/validate_docs_districts.py"]),
    ("validate memo mechanics", [sys.executable, "scripts/mechanics/validate_memo_mechanics.py"]),
    ("validate memo mechanic parts", [sys.executable, "scripts/mechanics/validate_memo_mechanic_parts.py"]),
    ("check memo mechanics index", [sys.executable, "scripts/mechanics/build_memo_mechanics_index.py", "--check"]),
    ("validate memo mechanics index", [sys.executable, "scripts/mechanics/validate_memo_mechanics_index.py"]),
    ("check memo mechanic cards", [sys.executable, "scripts/mechanics/build_memo_mechanic_cards.py", "--check"]),
    ("validate memo mechanic cards", [sys.executable, "scripts/mechanics/validate_memo_mechanic_cards.py"]),
    ("check memo mechanic owner routes", [sys.executable, "scripts/mechanics/build_memo_mechanic_owner_routes.py", "--check"]),
    ("validate memo mechanic owner routes", [sys.executable, "scripts/mechanics/validate_memo_mechanic_owner_routes.py"]),
    ("check memo mechanic landing logs", [sys.executable, "scripts/mechanics/build_memo_mechanic_landing_logs.py", "--check"]),
    ("validate memo mechanic landing logs", [sys.executable, "scripts/mechanics/validate_memo_mechanic_landing_logs.py"]),
    ("check memo mechanic readiness", [sys.executable, "scripts/mechanics/build_memo_mechanic_readiness.py", "--check"]),
    ("validate memo mechanic readiness", [sys.executable, "scripts/mechanics/validate_memo_mechanic_readiness.py"]),
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
