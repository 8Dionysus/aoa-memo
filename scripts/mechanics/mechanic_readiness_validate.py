from __future__ import annotations

from typing import Any

from mechanic_readiness_build import build_readiness
from mechanic_readiness_constants import (
    ARTIFACT_INVENTORY_REF,
    CARD_INDEX_REF,
    CONFIG_REF,
    GENERATED_BY,
    LANDING_LOG_INDEX_REF,
    MECHANIC_INDEX_REF,
    OWNER_ROUTE_INDEX_REF,
    READINESS_CHECKS,
    SCHEMA_VERSION,
    SOURCE_OF_TRUTH,
)


def validate_payload(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    expected = build_readiness()

    if payload != expected:
        issues.append("generated/mechanics/memo_mechanic_readiness.min.json is stale; run scripts/mechanics/build_memo_mechanic_readiness.py")

    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must keep schema_version {SCHEMA_VERSION}")
    if payload.get("source_of_truth") != SOURCE_OF_TRUTH:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must route source_of_truth to {SOURCE_OF_TRUTH}")
    if payload.get("config_ref") != CONFIG_REF:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must route config_ref to {CONFIG_REF}")
    if payload.get("mechanic_index_ref") != MECHANIC_INDEX_REF:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must route mechanic_index_ref to {MECHANIC_INDEX_REF}")
    if payload.get("artifact_inventory_ref") != ARTIFACT_INVENTORY_REF:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must route artifact_inventory_ref to {ARTIFACT_INVENTORY_REF}")
    if payload.get("card_index_ref") != CARD_INDEX_REF:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must route card_index_ref to {CARD_INDEX_REF}")
    if payload.get("owner_route_index_ref") != OWNER_ROUTE_INDEX_REF:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must route owner_route_index_ref to {OWNER_ROUTE_INDEX_REF}")
    if payload.get("landing_log_index_ref") != LANDING_LOG_INDEX_REF:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must route landing_log_index_ref to {LANDING_LOG_INDEX_REF}")
    if payload.get("generated_by") != GENERATED_BY:
        issues.append(f"generated/mechanics/memo_mechanic_readiness.min.json must name {GENERATED_BY}")

    packages = payload.get("packages")
    if not isinstance(packages, list):
        issues.append("generated/mechanics/memo_mechanic_readiness.min.json packages must be a list")
        return issues

    for package in packages:
        if not isinstance(package, dict):
            issues.append("generated/mechanics/memo_mechanic_readiness.min.json package entries must be objects")
            continue
        slug = package.get("slug", "<missing>")
        if not package.get("ready"):
            issues.append(f"mechanics/{slug}: readiness contract is not complete")
        checks = package.get("checks")
        if not isinstance(checks, dict):
            issues.append(f"mechanics/{slug}: checks must be an object")
            continue
        for check in READINESS_CHECKS:
            if checks.get(check) is not True:
                issues.append(f"mechanics/{slug}: readiness check failed: {check}")
        if checks.get("artifact-test-coverage") is not True:
            issues.append(
                f"mechanics/{slug}: package-local non-test artifacts require at least one package-local test"
            )
        if checks.get("local-test-route") is not True:
            issues.append(
                f"mechanics/{slug}: package-local tests must be named in validation route"
            )
        owner_refs = package.get("stronger_owner_refs")
        if not isinstance(owner_refs, list) or len(owner_refs) < 3:
            issues.append(f"mechanics/{slug}: must name at least three stronger owner refs")
        stop_line_terms = package.get("stop_line_terms")
        if (
            not isinstance(stop_line_terms, list)
            or not {"proof", "runtime"}.issubset(set(stop_line_terms))
            or not bool({"role", "route", "source owner", "authority"} & set(stop_line_terms))
        ):
            issues.append(
                f"mechanics/{slug}: stop-lines must name proof, runtime, and one authority boundary"
            )

    counts = payload.get("counts")
    if isinstance(counts, dict) and counts.get("ready_packages") != counts.get("packages"):
        issues.append("generated/mechanics/memo_mechanic_readiness.min.json ready_packages must equal packages")

    return issues
