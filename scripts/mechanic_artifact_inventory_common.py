from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "memo_mechanics.json"
GENERATED_PATH = REPO_ROOT / "generated" / "mechanic_artifacts.min.json"

SCHEMA_VERSION = "aoa_memo_mechanic_artifact_inventory_v2"
SOURCE_OF_TRUTH = "mechanics/ARTIFACT_TOPOLOGY.md"
CONFIG_REF = "config/memo_mechanics.json"

ARTIFACT_DIRS = (
    "config",
    "examples",
    "generated",
    "manifests",
    "schemas",
    "scripts",
    "tests",
)

KIND_BY_DIR = {
    "config": "config",
    "examples": "example",
    "generated": "generated",
    "manifests": "manifest",
    "schemas": "schema",
    "scripts": "script",
    "tests": "test",
}

SKIP_PARTS = {"__pycache__"}


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def tracked_relative_paths() -> list[str]:
    result = subprocess.run(
        ("git", "-C", str(REPO_ROOT), "ls-files", "-z"),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")
    return sorted(path for path in result.stdout.split("\0") if path)


def package_artifacts(slug: str, tracked_paths: list[str]) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    package_prefix = f"mechanics/{slug}/"

    for path_ref in tracked_paths:
        if not path_ref.startswith(package_prefix):
            continue
        parts = Path(path_ref).parts
        if len(parts) < 4:
            continue
        if set(parts) & SKIP_PARTS:
            continue
        artifact: dict[str, str] | None = None
        district = parts[2]
        if district in ARTIFACT_DIRS:
            artifact = {
                "kind": KIND_BY_DIR[district],
                "district": district,
                "scope": "package",
                "owner_path": f"mechanics/{slug}",
                "path": path_ref,
                "package_path": "/".join(parts[2:]),
            }
        elif len(parts) >= 6 and parts[2] == "parts" and parts[4] in ARTIFACT_DIRS:
            part_slug = parts[3]
            district = parts[4]
            artifact = {
                "kind": KIND_BY_DIR[district],
                "district": district,
                "scope": "part",
                "part_slug": part_slug,
                "part_path": f"parts/{part_slug}",
                "owner_path": f"mechanics/{slug}/parts/{part_slug}",
                "path": path_ref,
                "package_path": "/".join(parts[2:]),
            }
        if artifact is not None:
            artifacts.append(artifact)

    return sorted(artifacts, key=lambda item: (item["district"], item["path"]))


def build_inventory() -> dict[str, Any]:
    config = load_config()
    tracked_paths = tracked_relative_paths()
    packages: list[dict[str, Any]] = []
    total_by_district = {district: 0 for district in ARTIFACT_DIRS}

    for package in config["packages"]:
        slug = package["slug"]
        artifacts = package_artifacts(slug, tracked_paths)
        artifact_counts = {district: 0 for district in ARTIFACT_DIRS}
        for artifact in artifacts:
            artifact_counts[artifact["district"]] += 1
            total_by_district[artifact["district"]] += 1
        packages.append(
            {
                "slug": slug,
                "path": f"mechanics/{slug}",
                "artifact_count": len(artifacts),
                "artifact_counts": artifact_counts,
                "artifacts": artifacts,
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "config_ref": CONFIG_REF,
        "generated_by": "scripts/build_mechanic_artifact_inventory.py",
        "artifact_dirs": list(ARTIFACT_DIRS),
        "counts": {
            "packages": len(packages),
            "packages_with_artifacts": sum(1 for package in packages if package["artifact_count"]),
            "artifacts": sum(total_by_district.values()),
            "by_district": total_by_district,
        },
        "packages": packages,
    }


def render_inventory(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
