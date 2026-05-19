from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "mechanics" / "questbook" / "scripts"))

import validate_quest_store  # noqa: E402


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


def test_agon_lane_rejects_yaml_sources() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        quests = root / "quests"
        (quests / "agon" / "active").mkdir(parents=True)
        (quests / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
        (quests / "README.md").write_text("# Quests\n", encoding="utf-8")
        (quests / "agon" / "README.md").write_text("# Agon\n", encoding="utf-8")
        (quests / "agon" / "active" / "AOM-Q-AGON-0001.yaml").write_text(
            "id: AOM-Q-AGON-0001\nstate: active\npublic_safe: true\n",
            encoding="utf-8",
        )

        with patch.object(validate_quest_store, "ROOT", root):
            with patch.object(validate_quest_store, "QUESTS", quests):
                problems = validate_quest_store.validate()

    assert any("agon quest sources must be Markdown, not YAML" in problem for problem in problems)
