#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from mechanic_artifact_family_contracts import (
    validate_config_family_contracts,
    validate_example_family_contracts,
    validate_generated_family_contracts,
    validate_manifest_policy_contract,
    validate_schema_family_contracts,
    validate_script_family_contracts,
    validate_test_family_contracts,
)
from mechanic_artifact_topology_common import (
    FORBIDDEN_ROOT_PREFIXES,
    REPO_ROOT,
    ROOT_DISTRICTS_SCHEMA_VERSION,
    ROOT_TECHNICAL_DISTRICTS,
    load_root_districts_config,
    root_files,
)


def _validate_district_config(district: str, config: dict[str, object], issues: list[str]) -> None:
    if not isinstance(config.get("root_role"), str) or not config.get("root_role"):
        issues.append(f"config/root-topology/root_technical_districts.json: {district} must name root_role")
    allowed_files = config.get("allowed_files")
    if not isinstance(allowed_files, list) or not all(isinstance(item, str) for item in allowed_files):
        issues.append(f"config/root-topology/root_technical_districts.json: {district}.allowed_files must be a string array")
        return

    duplicate_paths = sorted({item for item in allowed_files if allowed_files.count(item) > 1})
    for duplicate_path in duplicate_paths:
        issues.append(f"config/root-topology/root_technical_districts.json: duplicate allowed path {duplicate_path}")

    allowed = set(allowed_files)
    for allowed_path in allowed:
        parts = Path(allowed_path).parts
        if not parts or parts[0] != district:
            issues.append(f"config/root-topology/root_technical_districts.json: {allowed_path} is outside district {district}")
        if Path(allowed_path).name == "AGENTS.md":
            issues.append(f"config/root-topology/root_technical_districts.json: {allowed_path} should rely on the route-card exception, not allowed_files")

    actual = {path.relative_to(REPO_ROOT).as_posix() for path in root_files(district)}
    for missing in sorted(allowed - actual):
        issues.append(f"{missing}: allowed root technical artifact is missing")
    for unexpected in sorted(actual - allowed):
        issues.append(
            f"{unexpected}: root technical artifact must be listed in config/root-topology/root_technical_districts.json or moved under mechanics/<slug>/"
        )


def validate_root_district_allowlist() -> list[str]:
    issues: list[str] = []
    payload, config_errors = load_root_districts_config()
    issues.extend(config_errors)
    if payload is None:
        return issues

    if payload.get("schema_version") != ROOT_DISTRICTS_SCHEMA_VERSION:
        issues.append(f"config/root-topology/root_technical_districts.json must keep schema_version {ROOT_DISTRICTS_SCHEMA_VERSION}")
    if payload.get("source_of_truth") != "mechanics/ARTIFACT_TOPOLOGY.md":
        issues.append("config/root-topology/root_technical_districts.json must route source_of_truth to mechanics/ARTIFACT_TOPOLOGY.md")

    districts = payload.get("districts")
    if not isinstance(districts, dict):
        issues.append("config/root-topology/root_technical_districts.json: districts must be an object")
        return issues

    missing_districts = sorted(set(ROOT_TECHNICAL_DISTRICTS) - set(districts))
    extra_districts = sorted(set(districts) - set(ROOT_TECHNICAL_DISTRICTS))
    for district in missing_districts:
        issues.append(f"config/root-topology/root_technical_districts.json: missing district {district}")
    for district in extra_districts:
        issues.append(f"config/root-topology/root_technical_districts.json: unsupported district {district}")

    for district in ROOT_TECHNICAL_DISTRICTS:
        config = districts.get(district)
        if not isinstance(config, dict):
            if district in districts:
                issues.append(f"config/root-topology/root_technical_districts.json: {district} must be an object")
            continue
        _validate_district_config(district, config, issues)

    issues.extend(validate_generated_family_contracts(payload, districts))
    issues.extend(validate_script_family_contracts(payload, districts))
    issues.extend(validate_test_family_contracts(payload, districts))
    issues.extend(validate_schema_family_contracts(payload, districts))
    issues.extend(validate_example_family_contracts(payload, districts))
    issues.extend(validate_config_family_contracts(payload, districts))
    issues.extend(validate_manifest_policy_contract(payload, districts))
    return issues


def validate() -> list[str]:
    issues = validate_root_district_allowlist()

    for directory, prefixes in FORBIDDEN_ROOT_PREFIXES.items():
        for path in root_files(directory):
            if path.name.startswith(prefixes):
                relative = path.relative_to(REPO_ROOT).as_posix()
                issues.append(f"{relative}: single-mechanic artifact must live under mechanics/<slug>/")

    for path in root_files("manifests"):
        relative = path.relative_to(REPO_ROOT).as_posix()
        issues.append(f"{relative}: root manifests are reserved for shared manifests only")

    return issues


def main() -> int:
    issues = validate()
    if issues:
        print("Mechanic artifact topology validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] mechanic artifact topology is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
