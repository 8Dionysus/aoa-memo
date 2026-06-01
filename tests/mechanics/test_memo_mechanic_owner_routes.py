from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "mechanics"))

import validation_lanes  # noqa: E402
from memo_mechanic_owner_routes_common import build_owner_routes, validate_payload  # noqa: E402


def release_command_text() -> str:
    return "\n".join(" ".join(step.command) for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE)


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


def test_memo_mechanic_owner_routes_are_current_and_valid() -> None:
    run_script("scripts/mechanics/build_memo_mechanic_owner_routes.py", "--check")
    run_script("scripts/mechanics/validate_memo_mechanic_owner_routes.py")
    payload = json.loads((REPO_ROOT / "generated" / "mechanics" / "memo_mechanic_owner_routes.min.json").read_text())
    assert validate_payload(payload) == []
    assert payload == build_owner_routes()


def test_memo_mechanic_owner_routes_cover_cards_and_owner_maps() -> None:
    payload = json.loads((REPO_ROOT / "generated" / "mechanics" / "memo_mechanic_owner_routes.min.json").read_text())
    assert payload["schema_version"] == "aoa_memo_mechanic_owner_routes_v1"
    assert payload["source_of_truth"] == "mechanics package OWNER_MAP.md and README mechanic cards"
    assert payload["config_ref"] == "config/mechanics/memo_mechanics.json"
    assert payload["card_index_ref"] == "generated/mechanics/memo_mechanic_cards.min.json"
    assert payload["counts"]["packages"] == 15
    assert payload["counts"]["owners"] >= 8
    assert payload["counts"]["stronger_owner_entries"] >= 45

    packages = {package["slug"]: package for package in payload["packages"]}
    for slug, package in packages.items():
        assert package["owner_map_ref"] == f"mechanics/{slug}/OWNER_MAP.md"
        assert all(package["checks"].values())
        assert set(package["card_owner_refs"]).issubset(set(package["owner_map_refs"]))
        assert any(route["route_kind"] == "memo-owner" for route in package["owner_routes"])
        assert sum(1 for route in package["owner_routes"] if route["route_kind"] == "stronger-owner") >= 3

    for owner_ref in ("aoa-evals", "abyss-stack", "aoa-agents", "aoa-routing"):
        assert owner_ref in payload["owners"]


def test_release_check_runs_memo_mechanic_owner_route_gate() -> None:
    text = release_command_text()
    for snippet in (
        "scripts/mechanics/build_memo_mechanic_owner_routes.py",
        "scripts/mechanics/validate_memo_mechanic_owner_routes.py",
    ):
        assert snippet in text
