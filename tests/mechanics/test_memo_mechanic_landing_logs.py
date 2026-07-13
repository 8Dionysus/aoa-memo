from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "mechanics"))

import validation_lanes  # noqa: E402
from memo_mechanic_landing_logs_common import build_landing_logs, validate_payload  # noqa: E402


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


def test_memo_mechanic_landing_logs_are_current_and_valid() -> None:
    run_script("scripts/mechanics/build_memo_mechanic_landing_logs.py", "--check")
    run_script("scripts/mechanics/validate_memo_mechanic_landing_logs.py")
    payload = json.loads((REPO_ROOT / "generated" / "mechanics" / "memo_mechanic_landing_logs.min.json").read_text())
    assert validate_payload(payload) == []
    assert payload == build_landing_logs()


def test_memo_mechanic_landing_logs_cover_every_package_receipt() -> None:
    payload = json.loads((REPO_ROOT / "generated" / "mechanics" / "memo_mechanic_landing_logs.min.json").read_text())
    assert payload["schema_version"] == "aoa_memo_mechanic_landing_logs_v2"
    assert payload["source_of_truth"] == "mechanics package LANDING_LOG.md receipts"
    assert payload["config_ref"] == "config/mechanics/memo_mechanics.json"
    assert payload["card_index_ref"] == "generated/mechanics/memo_mechanic_cards.min.json"
    assert payload["owner_route_index_ref"] == "generated/mechanics/memo_mechanic_owner_routes.min.json"
    assert payload["counts"]["packages"] == 15
    assert payload["counts"]["ready_logs"] == payload["counts"]["packages"]
    assert payload["counts"]["dated_logs"] == payload["counts"]["packages"]
    assert payload["counts"]["routed_validation_logs"] == payload["counts"]["packages"]
    assert payload["counts"]["stop_line_logs"] == payload["counts"]["packages"]

    packages = {package["slug"]: package for package in payload["packages"]}
    assert set(packages) == {
        "adoption",
        "agon",
        "antifragility",
        "checkpoint",
        "consumer-handoff",
        "governance",
        "lineage-harvest",
        "operational-gate",
        "questbook",
        "readiness-boundary",
        "recurrence-support",
        "retention",
        "shape-guard",
        "titan",
        "writeback",
    }
    for slug, package in packages.items():
        assert package["landing_log_ref"] == f"mechanics/{slug}/LANDING_LOG.md"
        assert package["card_ref"] == f"mechanics/{slug}/README.md#mechanic-card"
        assert package["owner_map_ref"] == f"mechanics/{slug}/OWNER_MAP.md"
        assert package["ready"] is True
        assert all(package["checks"].values())
        assert "2026-05-18" in package["dates"]
        assert "config/validation_lanes.json" in package["validation_route_refs"]
        assert {"AGENTS.md", "VALIDATION.md"} & set(package["validation_route_refs"])
        assert "validation_refs" not in package
        assert "python_commands" not in package
        assert package["landing_terms"]
        assert {"proof", "runtime"}.issubset(set(package["stop_line_terms"]))
        assert {"role", "route", "source owner", "authority", "owner acceptance"} & set(
            package["stop_line_terms"]
        )


def test_release_check_runs_memo_mechanic_landing_log_gate() -> None:
    text = release_command_text()
    for snippet in (
        "scripts/mechanics/build_memo_mechanic_landing_logs.py",
        "scripts/mechanics/validate_memo_mechanic_landing_logs.py",
    ):
        assert snippet in text
