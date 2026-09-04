#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from root_technical_districts_common import (
    CONFIG_REF,
    DISTRICT_ORDER,
    GENERATED_BY,
    GENERATED_PATH,
    REPO_ROOT,
    SCHEMA_VERSION,
    SOURCE_OF_TRUTH,
    build_index,
    load_config,
    render_index,
)


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def validate_payload(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    expected = build_index()
    config = load_config()

    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"{_rel(GENERATED_PATH)} must keep schema_version {SCHEMA_VERSION}")
    if payload.get("source_of_truth") != SOURCE_OF_TRUTH:
        issues.append(f"{_rel(GENERATED_PATH)} must route source_of_truth to {SOURCE_OF_TRUTH}")
    if payload.get("config_ref") != CONFIG_REF:
        issues.append(f"{_rel(GENERATED_PATH)} must route config_ref to {CONFIG_REF}")
    if payload.get("generated_by") != GENERATED_BY:
        issues.append(f"{_rel(GENERATED_PATH)} must name its builder")
    if payload.get("route_card_exception") != config.get("route_card_exception"):
        issues.append(f"{_rel(GENERATED_PATH)} must mirror route_card_exception from {CONFIG_REF}")
    if payload.get("validation_companion_exception") != config.get(
        "validation_companion_exception"
    ):
        issues.append(
            f"{_rel(GENERATED_PATH)} must mirror validation_companion_exception "
            f"from {CONFIG_REF}"
        )
    if payload.get("district_order") != list(DISTRICT_ORDER):
        issues.append(f"{_rel(GENERATED_PATH)} must preserve root district order")

    districts = payload.get("districts")
    if not isinstance(districts, dict):
        issues.append(f"{_rel(GENERATED_PATH)} districts must be an object")
        return issues

    for district in DISTRICT_ORDER:
        entry = districts.get(district)
        if not isinstance(entry, dict):
            issues.append(f"{_rel(GENERATED_PATH)} missing district {district}")
            continue
        route_card = entry.get("route_card")
        if not isinstance(route_card, str) or not (REPO_ROOT / route_card).is_file():
            issues.append(f"{_rel(GENERATED_PATH)} district {district} route_card is missing")
        if entry.get("path") != f"{district}/":
            issues.append(f"{_rel(GENERATED_PATH)} district {district} path must be {district}/")
        if entry.get("root_role") != config["districts"][district]["root_role"]:
            issues.append(f"{_rel(GENERATED_PATH)} district {district} root_role is stale")
        if entry.get("allowed_count") != len(config["districts"][district]["allowed_files"]):
            issues.append(f"{_rel(GENERATED_PATH)} district {district} allowed_count is stale")
        family_ids = entry.get("family_ids")
        if not isinstance(family_ids, list) or not all(isinstance(item, str) for item in family_ids):
            issues.append(f"{_rel(GENERATED_PATH)} district {district} family_ids must be a string array")

    if payload != expected:
        issues.append(f"{_rel(GENERATED_PATH)} is stale; run scripts/root-topology/build_root_technical_districts_index.py")

    return issues


def validate() -> list[str]:
    if not GENERATED_PATH.exists():
        return [f"{_rel(GENERATED_PATH)} is missing; run scripts/root-topology/build_root_technical_districts_index.py"]
    try:
        payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{_rel(GENERATED_PATH)} is invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return [f"{_rel(GENERATED_PATH)} must be a JSON object"]

    issues = validate_payload(payload)
    current = GENERATED_PATH.read_text(encoding="utf-8")
    if current != render_index(payload):
        issues.append(f"{_rel(GENERATED_PATH)} must use compact deterministic rendering")
    return issues


def main() -> int:
    issues = validate()
    if issues:
        print("Root technical districts index validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] root technical districts index is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
