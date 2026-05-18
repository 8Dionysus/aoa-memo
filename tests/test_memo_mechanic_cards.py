from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from memo_mechanic_cards_common import build_cards, validate_payload  # noqa: E402


def run_script(*args: str) -> None:
    completed = subprocess.run(
        (sys.executable, *args),
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (
        f"{' '.join(args)} failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
    )


def test_memo_mechanic_cards_are_current_and_valid() -> None:
    run_script("scripts/build_memo_mechanic_cards.py", "--check")
    run_script("scripts/validate_memo_mechanic_cards.py")
    payload = json.loads((REPO_ROOT / "generated" / "memo_mechanic_cards.min.json").read_text())
    assert validate_payload(payload) == []
    assert payload == build_cards()


def test_memo_mechanic_cards_make_route_cards_machine_readable() -> None:
    payload = json.loads((REPO_ROOT / "generated" / "memo_mechanic_cards.min.json").read_text())
    assert payload["schema_version"] == "aoa_memo_mechanic_cards_v1"
    assert payload["source_of_truth"] == "mechanics package README mechanic cards"
    assert payload["config_ref"] == "config/memo_mechanics.json"
    assert payload["counts"]["packages"] == 15
    assert payload["counts"]["landed_packages"] == payload["counts"]["packages"]
    assert payload["counts"]["must_not_claims"] >= 45

    packages = {package["slug"]: package for package in payload["packages"]}
    for slug, package in packages.items():
        assert package["status"] == package["configured_status"] == "landed"
        assert package["operation"] == package["configured_operation"]
        assert package["card_ref"] == f"mechanics/{slug}/README.md#mechanic-card"
        assert all(package["checks"].values())
        assert len(package["card"]["stronger_owner_split"]) >= 3
        assert len(package["card"]["must_not_claim"]) >= 3
        assert len(package["owner_refs"]) >= 3
        assert {"proof", "runtime"}.issubset(set(package["stop_line_terms"]))
        assert {"role", "route", "source owner", "authority", "owner acceptance"} & set(
            package["stop_line_terms"]
        )


def test_release_check_runs_memo_mechanic_card_gate() -> None:
    text = (REPO_ROOT / "scripts" / "release_check.py").read_text(encoding="utf-8")
    for snippet in (
        "scripts/build_memo_mechanic_cards.py",
        "scripts/validate_memo_mechanic_cards.py",
    ):
        assert snippet in text
