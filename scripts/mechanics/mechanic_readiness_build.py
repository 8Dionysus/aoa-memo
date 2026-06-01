from __future__ import annotations

from pathlib import Path
from typing import Any

from mechanic_artifact_inventory_common import ARTIFACT_DIRS, build_inventory
from mechanic_readiness_constants import (
    ARTIFACT_INVENTORY_REF,
    CARD_INDEX_REF,
    CONFIG_REF,
    CORE_OWNER_REFS,
    GENERATED_BY,
    KNOWN_STRONGER_OWNER_REFS,
    LANDING_LOG_INDEX_REF,
    MECHANIC_INDEX_REF,
    NON_TEST_ARTIFACT_DIRS,
    OWNER_ROUTE_INDEX_REF,
    PACKAGE_SURFACES,
    READINESS_CHECKS,
    REQUIRED_VALIDATION_REFS,
    SCHEMA_VERSION,
    SOURCE_OF_TRUTH,
    SUPPORTING_VALIDATION_REFS,
)
from memo_mechanics_common import README_HEADINGS, REPO_ROOT, load_config


def _read(relative: str) -> str:
    path = REPO_ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _text_has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def _section_terms(text: str) -> list[str]:
    lower = text.lower()
    terms = []
    for term in ("proof", "runtime", "role", "route", "source owner", "authority"):
        if term in lower:
            terms.append(term)
    return terms


def _artifact_map() -> dict[str, dict[str, Any]]:
    return {package["slug"]: package for package in build_inventory()["packages"]}


def _local_test_dirs(artifact_entries: list[Any]) -> list[str]:
    test_dirs: set[str] = set()
    for artifact in artifact_entries:
        if not isinstance(artifact, dict):
            continue
        if artifact.get("district") != "tests" or not isinstance(artifact.get("path"), str):
            continue
        path = Path(artifact["path"])
        if path.suffix == ".py" and path.name.startswith("test"):
            test_dirs.add(str(path.parent))
    return sorted(test_dirs)


def _has_runnable_local_test_routes(validation_text: str, test_dirs: list[str]) -> bool:
    if not test_dirs:
        return False
    covered: set[str] = set()
    for raw_line in validation_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("python -m pytest -q "):
            continue
        args = line.split()[4:]
        for test_dir in test_dirs:
            if any(arg == test_dir or arg.startswith(f"{test_dir}/") for arg in args):
                covered.add(test_dir)
    return all(test_dir in covered for test_dir in test_dirs)


def _present_docs(slug: str) -> list[str]:
    docs_root = REPO_ROOT / "mechanics" / slug / "docs"
    if not docs_root.is_dir():
        return []
    return sorted(
        path.name
        for path in docs_root.glob("*.md")
        if path.name not in {"AGENTS.md", "README.md"}
    )


def build_package_readiness(package: dict[str, Any], artifacts: dict[str, Any]) -> dict[str, Any]:
    slug = package["slug"]
    package_root = f"mechanics/{slug}"
    readme = _read(f"{package_root}/README.md")
    agents = _read(f"{package_root}/AGENTS.md")
    owner_map = _read(f"{package_root}/OWNER_MAP.md")
    parts = _read(f"{package_root}/PARTS.md")
    provenance = _read(f"{package_root}/PROVENANCE.md")
    landing_log = _read(f"{package_root}/LANDING_LOG.md")
    legacy_index = _read(f"{package_root}/legacy/INDEX.md")

    expected_docs = sorted(package["docs"])
    present_docs = _present_docs(slug)
    missing_docs = sorted(set(expected_docs) - set(present_docs))
    extra_docs = sorted(set(present_docs) - set(expected_docs))

    package_files = {
        relative: (REPO_ROOT / package_root / relative).is_file()
        for relative in PACKAGE_SURFACES
    }
    readme_headings = [heading for heading in README_HEADINGS if heading in readme]
    validation_text = "\n".join((agents, landing_log, readme))
    validation_refs = [
        ref
        for ref in (*REQUIRED_VALIDATION_REFS, *SUPPORTING_VALIDATION_REFS)
        if ref in validation_text
    ]
    route_text = "\n".join((readme, owner_map))
    owner_refs = [
        ref
        for ref in KNOWN_STRONGER_OWNER_REFS
        if _text_has(route_text, ref)
    ]
    stop_line_terms = _section_terms("\n".join((readme, owner_map, landing_log)))
    artifact_counts_raw = artifacts.get("artifact_counts", {})
    if not isinstance(artifact_counts_raw, dict):
        artifact_counts_raw = {}
    artifact_counts = {
        district: int(artifact_counts_raw.get(district, 0) or 0)
        for district in ARTIFACT_DIRS
    }
    artifact_count = int(artifacts.get("artifact_count", 0))
    artifact_districts = sorted(
        district for district, count in artifact_counts.items() if count > 0
    )
    non_test_artifact_count = sum(artifact_counts[district] for district in NON_TEST_ARTIFACT_DIRS)
    test_artifact_count = artifact_counts["tests"]
    artifact_entries = artifacts.get("artifacts", [])
    if not isinstance(artifact_entries, list):
        artifact_entries = []
    test_dirs = _local_test_dirs(artifact_entries)
    local_test_refs = [f"python -m pytest -q {test_dir}" for test_dir in test_dirs]

    checks = {
        "package-surfaces": all(package_files.values()),
        "readme-card": (
            len(readme_headings) == len(README_HEADINGS)
            and isinstance(package.get("operation"), str)
            and package["operation"] in readme
        ),
        "docs-index": not missing_docs and not extra_docs,
        "parts-interface": (
            "## Active Parts" in parts
            and "## Interface" in parts
            and all(doc in parts for doc in expected_docs)
        ),
        "owner-map": "aoa-memo" in owner_map and all(ref in route_text for ref in CORE_OWNER_REFS),
        "legacy-bridge": all(f"{package_root}/docs/{doc}" in legacy_index for doc in expected_docs),
        "provenance": (
            (
                "Use active surfaces first" in provenance
                or "## Active Placement" in provenance
                or "## Active source" in provenance
            )
            and (
                "legacy/INDEX.md" in provenance
                or "Former Placement" in provenance
                or "Former flat source" in provenance
                or "Former active paths" in provenance
            )
        ),
        "landing-log": "python scripts/release/release_check.py" in landing_log or "python scripts/release/release_check.py" in agents,
        "validation-route": all(ref in validation_refs for ref in REQUIRED_VALIDATION_REFS),
        "artifact-test-coverage": non_test_artifact_count == 0 or bool(test_dirs),
        "local-test-route": test_artifact_count == 0 or _has_runnable_local_test_routes(
            validation_text,
            test_dirs,
        ),
        "stronger-owner-stop-lines": (
            {"proof", "runtime"}.issubset(set(stop_line_terms))
            and bool({"role", "route", "source owner", "authority"} & set(stop_line_terms))
        ),
    }

    return {
        "slug": slug,
        "title": package["title"],
        "status": package["status"],
        "operation": package["operation"],
        "os_abyss_role": package["os_abyss_role"],
        "package_path": package_root,
        "docs": {
            "expected": expected_docs,
            "present": present_docs,
            "missing": missing_docs,
            "extra": extra_docs,
        },
        "artifacts": {
            "count": artifact_count,
            "counts": artifact_counts,
            "districts": artifact_districts,
            "non_test_count": non_test_artifact_count,
            "test_count": test_artifact_count,
            "test_dirs": test_dirs,
        },
        "package_files": package_files,
        "readme_headings": readme_headings,
        "validation_refs": validation_refs,
        "local_test_refs": local_test_refs,
        "stronger_owner_refs": owner_refs,
        "stop_line_terms": stop_line_terms,
        "checks": checks,
        "ready": all(checks.values()),
    }


def build_readiness() -> dict[str, Any]:
    config = load_config()
    artifacts = _artifact_map()
    packages = [
        build_package_readiness(package, artifacts.get(package["slug"], {"artifacts": [], "artifact_count": 0}))
        for package in config["packages"]
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "source_of_truth": SOURCE_OF_TRUTH,
        "config_ref": CONFIG_REF,
        "mechanic_index_ref": MECHANIC_INDEX_REF,
        "artifact_inventory_ref": ARTIFACT_INVENTORY_REF,
        "card_index_ref": CARD_INDEX_REF,
        "owner_route_index_ref": OWNER_ROUTE_INDEX_REF,
        "landing_log_index_ref": LANDING_LOG_INDEX_REF,
        "generated_by": GENERATED_BY,
        "contract": {
            "package_surfaces": list(PACKAGE_SURFACES),
            "readme_headings": list(README_HEADINGS),
            "readiness_checks": list(READINESS_CHECKS),
            "core_owner_refs": list(CORE_OWNER_REFS),
            "required_validation_refs": list(REQUIRED_VALIDATION_REFS),
            "supporting_validation_refs": list(SUPPORTING_VALIDATION_REFS),
        },
        "counts": {
            "packages": len(packages),
            "ready_packages": sum(1 for package in packages if package["ready"]),
            "docs": sum(len(package["docs"]["expected"]) for package in packages),
            "package_local_artifacts": sum(package["artifacts"]["count"] for package in packages),
        },
        "packages": packages,
    }
