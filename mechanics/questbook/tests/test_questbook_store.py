from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, *args),
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_quest_store_validator_passes() -> None:
    completed = run_script("mechanics/questbook/scripts/validate_quest_store.py")
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_quest_surface_builder_check_passes() -> None:
    completed = run_script("mechanics/questbook/scripts/build_quest_surfaces.py", "--check")
    assert completed.returncode == 0, completed.stderr or completed.stdout
