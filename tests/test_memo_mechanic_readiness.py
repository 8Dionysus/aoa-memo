from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from mechanic_readiness_common import build_readiness, validate_payload  # noqa: E402


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


def test_memo_mechanic_readiness_is_current_and_valid() -> None:
    run_script("scripts/build_memo_mechanic_readiness.py", "--check")
    run_script("scripts/validate_memo_mechanic_readiness.py")
    payload = json.loads((REPO_ROOT / "generated" / "memo_mechanic_readiness.min.json").read_text())
    assert validate_payload(payload) == []
    assert payload == build_readiness()


def test_memo_mechanic_readiness_covers_all_packages() -> None:
    payload = json.loads((REPO_ROOT / "generated" / "memo_mechanic_readiness.min.json").read_text())
    assert payload["schema_version"] == "aoa_memo_mechanic_readiness_v1"
    assert payload["source_of_truth"] == "mechanics/README.md"
    assert payload["config_ref"] == "config/memo_mechanics.json"
    assert payload["mechanic_index_ref"] == "generated/memo_mechanics.min.json"
    assert payload["artifact_inventory_ref"] == "generated/mechanic_artifacts.min.json"
    assert payload["card_index_ref"] == "generated/memo_mechanic_cards.min.json"
    assert payload["owner_route_index_ref"] == "generated/memo_mechanic_owner_routes.min.json"
    assert payload["landing_log_index_ref"] == "generated/memo_mechanic_landing_logs.min.json"
    assert "artifact-test-coverage" in payload["contract"]["readiness_checks"]
    assert payload["counts"]["packages"] == 15
    assert payload["counts"]["ready_packages"] == payload["counts"]["packages"]
    assert payload["counts"]["docs"] == 102
    assert payload["counts"]["package_local_artifacts"] > 100

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
    for package in packages.values():
        assert package["ready"] is True
        assert all(package["checks"].values())
        artifact_counts = package["artifacts"]["counts"]
        assert package["artifacts"]["count"] == sum(artifact_counts.values())
        assert package["artifacts"]["non_test_count"] == sum(
            count for district, count in artifact_counts.items() if district != "tests"
        )
        assert package["artifacts"]["test_count"] == artifact_counts["tests"]
        if package["artifacts"]["non_test_count"]:
            assert package["artifacts"]["test_count"] > 0
            assert package["checks"]["artifact-test-coverage"] is True
        assert "aoa-evals" in package["stronger_owner_refs"]
        assert "abyss-stack" in package["stronger_owner_refs"]
        stop_line_terms = set(package["stop_line_terms"])
        assert {"proof", "runtime"}.issubset(stop_line_terms)
        assert {"role", "route", "source owner", "authority"} & stop_line_terms


def test_memo_mechanic_readiness_rejects_untested_local_artifacts() -> None:
    payload = build_readiness()
    retention = next(package for package in payload["packages"] if package["slug"] == "retention")

    retention["artifacts"]["counts"]["tests"] = 0
    retention["artifacts"]["test_count"] = 0
    retention["checks"]["artifact-test-coverage"] = False
    retention["ready"] = False
    payload["counts"]["ready_packages"] -= 1

    issues = validate_payload(payload)
    assert "mechanics/retention: readiness check failed: artifact-test-coverage" in issues
    assert (
        "mechanics/retention: package-local non-test artifacts require at least one package-local test"
        in issues
    )
