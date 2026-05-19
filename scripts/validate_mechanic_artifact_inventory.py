#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from mechanic_artifact_inventory_common import (
    ARTIFACT_DIRS,
    CONFIG_REF,
    GENERATED_PATH,
    REPO_ROOT,
    SCHEMA_VERSION,
    SOURCE_OF_TRUTH,
    build_inventory,
    render_inventory,
)


def validate_payload(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} must keep schema_version {SCHEMA_VERSION}")
    if payload.get("source_of_truth") != SOURCE_OF_TRUTH:
        issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} must route source_of_truth to {SOURCE_OF_TRUTH}")
    if payload.get("config_ref") != CONFIG_REF:
        issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} must route config_ref to {CONFIG_REF}")
    if payload.get("generated_by") != "scripts/build_mechanic_artifact_inventory.py":
        issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} must name its builder")
    if payload.get("artifact_dirs") != list(ARTIFACT_DIRS):
        issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} must preserve artifact_dirs order")

    packages = payload.get("packages")
    if not isinstance(packages, list):
        issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} packages must be a list")
        return issues

    seen_paths: set[str] = set()
    for package in packages:
        if not isinstance(package, dict):
            issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} package entries must be objects")
            continue
        slug = package.get("slug")
        package_path = package.get("path")
        if not isinstance(slug, str) or not slug:
            issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} package must name slug")
            continue
        if package_path != f"mechanics/{slug}":
            issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} package {slug} has invalid path")
        artifacts = package.get("artifacts")
        if not isinstance(artifacts, list):
            issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} package {slug} artifacts must be a list")
            continue
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} package {slug} artifact entries must be objects")
                continue
            path_ref = artifact.get("path")
            district = artifact.get("district")
            package_ref = artifact.get("package_path")
            scope = artifact.get("scope")
            if not isinstance(path_ref, str) or not path_ref:
                issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} package {slug} artifact must name path")
                continue
            if path_ref in seen_paths:
                issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} duplicates artifact path {path_ref}")
            seen_paths.add(path_ref)
            parts = Path(path_ref).parts
            if len(parts) < 4 or parts[0] != "mechanics" or parts[1] != slug:
                issues.append(f"{path_ref}: artifact path must stay under mechanics/{slug}/")
                continue
            if district not in ARTIFACT_DIRS:
                issues.append(f"{path_ref}: artifact has unsupported district {district!r}")
            if scope not in {"package", "part"}:
                issues.append(f"{path_ref}: artifact must name scope package or part")
                continue
            if scope == "package":
                if parts[2] != district:
                    issues.append(f"{path_ref}: package artifact district must match path")
                if artifact.get("owner_path") != f"mechanics/{slug}":
                    issues.append(f"{path_ref}: package artifact owner_path must be mechanics/{slug}")
                if "part_slug" in artifact or "part_path" in artifact:
                    issues.append(f"{path_ref}: package artifact must not name part fields")
            elif scope == "part":
                if len(parts) < 6 or parts[2] != "parts" or parts[4] != district:
                    issues.append(f"{path_ref}: part artifact must live under mechanics/{slug}/parts/<part>/{district}/")
                    continue
                part_slug = parts[3]
                if artifact.get("part_slug") != part_slug:
                    issues.append(f"{path_ref}: part_slug must match path")
                if artifact.get("part_path") != f"parts/{part_slug}":
                    issues.append(f"{path_ref}: part_path must match path")
                if artifact.get("owner_path") != f"mechanics/{slug}/parts/{part_slug}":
                    issues.append(f"{path_ref}: part artifact owner_path must match part path")
                part_root = REPO_ROOT / "mechanics" / slug / "parts" / part_slug
                for required in ("README.md", "CONTRACT.md", "VALIDATION.md"):
                    if not (part_root / required).is_file():
                        issues.append(f"{path_ref}: part artifact owner missing {required}")
            if package_ref != "/".join(parts[2:]):
                issues.append(f"{path_ref}: package_path must be path relative to mechanics/{slug}/")
            if not (REPO_ROOT / path_ref).is_file():
                issues.append(f"{path_ref}: inventoried artifact is missing")

    expected = build_inventory()
    if payload != expected:
        issues.append(
            f"{GENERATED_PATH.relative_to(REPO_ROOT)} is stale; run scripts/build_mechanic_artifact_inventory.py"
        )

    return issues


def validate() -> list[str]:
    if not GENERATED_PATH.exists():
        return [f"{GENERATED_PATH.relative_to(REPO_ROOT)} is missing; run scripts/build_mechanic_artifact_inventory.py"]
    try:
        payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{GENERATED_PATH.relative_to(REPO_ROOT)} is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return [f"{GENERATED_PATH.relative_to(REPO_ROOT)} must be a JSON object"]

    issues = validate_payload(payload)
    rendered = render_inventory(payload)
    current = GENERATED_PATH.read_text(encoding="utf-8")
    if current != rendered:
        issues.append(f"{GENERATED_PATH.relative_to(REPO_ROOT)} must use compact deterministic rendering")
    return issues


def main() -> int:
    issues = validate()
    if issues:
        print("Mechanic artifact inventory validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] mechanic artifact inventory is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
