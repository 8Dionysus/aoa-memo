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


def test_quest_generated_views_part_names_root_outputs_and_builder() -> None:
    completed = run_script("mechanics/questbook/scripts/validate_quest_store.py")
    assert completed.returncode == 0, completed.stderr or completed.stdout

    contract = (
        REPO_ROOT
        / "mechanics"
        / "questbook"
        / "parts"
        / "generated-views"
        / "CONTRACT.md"
    ).read_text(encoding="utf-8")
    assert "generated/quest_catalog.min.json" in contract
    assert "generated/quest_dispatch.min.json" in contract
    assert "mechanics/questbook/scripts/build_quest_surfaces.py" in contract
