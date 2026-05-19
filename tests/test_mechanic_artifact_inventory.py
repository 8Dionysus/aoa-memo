from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from mechanic_artifact_inventory_common import ARTIFACT_DIRS, build_inventory  # noqa: E402
from validate_mechanic_artifact_inventory import validate  # noqa: E402


def test_mechanic_artifact_inventory_is_current() -> None:
    assert validate() == []


def test_mechanic_artifact_inventory_covers_package_local_artifacts() -> None:
    inventory = build_inventory()

    assert inventory["artifact_dirs"] == list(ARTIFACT_DIRS)
    assert inventory["schema_version"] == "aoa_memo_mechanic_artifact_inventory_v2"
    assert inventory["counts"]["packages_with_artifacts"] >= 10
    assert inventory["counts"]["artifacts"] > 100
    assert any(package["slug"] == "agon" and package["artifact_count"] > 0 for package in inventory["packages"])
    assert any(package["slug"] == "writeback" and package["artifact_count"] > 0 for package in inventory["packages"])
    agon = next(package for package in inventory["packages"] if package["slug"] == "agon")
    assert any(artifact["scope"] == "part" for artifact in agon["artifacts"])
    assert {
        artifact["part_slug"]
        for artifact in agon["artifacts"]
        if artifact.get("scope") == "part"
    } >= {"prebinding-and-candidate-intake", "bridge-and-evidence-seams"}
    titan = next(package for package in inventory["packages"] if package["slug"] == "titan")
    assert {artifact["scope"] for artifact in titan["artifacts"]} == {"part"}
    assert {
        artifact["part_slug"]
        for artifact in titan["artifacts"]
        if artifact.get("scope") == "part"
    } == {"core-memory-posture", "closeout-and-digest-posture", "specialized-policy"}
    adoption = next(package for package in inventory["packages"] if package["slug"] == "adoption")
    assert {artifact["scope"] for artifact in adoption["artifacts"]} == {"part"}
    assert {
        artifact["part_slug"]
        for artifact in adoption["artifacts"]
        if artifact.get("scope") == "part"
    } == {
        "adoption-boundary",
        "revision-and-retention-pressure",
        "scar-and-routing-adoption",
    }
    retention = next(package for package in inventory["packages"] if package["slug"] == "retention")
    assert {artifact["scope"] for artifact in retention["artifacts"]} == {"part"}
    assert {
        artifact["part_slug"]
        for artifact in retention["artifacts"]
        if artifact.get("scope") == "part"
    } == {
        "cross-repo-and-governance-retention",
        "office-markers",
        "post-release-retention",
    }
