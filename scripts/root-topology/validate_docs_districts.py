#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS_ROOT / "mechanics") not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT / "mechanics"))

from memo_mechanics_common import REPO_ROOT, load_config


RETIRED_DOCS_DISTRICTS = (
    "antifragility",
    "agon",
    "titan",
    "adoption",
    "governance",
    "writeback",
    "retention",
)
RETIRED_README_SNIPPETS = (
    "docs/agon/",
    "docs/titan/",
    "Agon Memo District",
    "Titan Memo District",
    "`docs/` is still partly flat",
    "Current flat surfaces",
    "flat files remain active surfaces",
)
ALLOWED_DOCS_ROOT_FILES = {
    "AGENTS.md",
    "README.md",
    "RELEASING.md",
}
ALLOWED_DOCS_SUBDIRS = {
    "boundaries",
    "decisions",
    "memory",
    "posture",
    "root",
    "testing",
    "validation",
}
REQUIRED_DOCS_DISTRICT_FILES = {
    "boundaries": {
        "AGENTS.md",
        "BOUNDARIES.md",
        "OPERATIONAL_BOUNDARY.md",
    },
    "memory": {
        "AGENTS.md",
        "MEMORY_MODEL.md",
        "MEMORY_OBJECT_PROFILES.md",
        "NARRATIVE_CORE_CONTRACT.md",
    },
    "posture": {
        "AGENTS.md",
        "AUDIT_EVENTS.md",
        "LIFECYCLE.md",
        "MEMORY_TEMPERATURES.md",
        "MEMORY_TRUST_POSTURE.md",
        "PROVENANCE_THREADS.md",
    },
    "root": {
        "AGENTS.md",
        "AGENTS_ROOT_REFERENCE.md",
        "RELEASING.md",
        "ROOT_SURFACE_LAW.md",
    },
    "testing": {
        "AGENTS.md",
        "TEST_TOPOLOGY.md",
        "test_inventory.json",
    },
    "validation": {
        "AGENTS.md",
        "COMMAND_AUTHORITY.md",
        "VALIDATOR_TOPOLOGY.md",
        "validator_inventory.json",
    },
}


def validate() -> list[str]:
    issues: list[str] = []
    docs_root = REPO_ROOT / "docs"
    docs_readme = (docs_root / "README.md").read_text(encoding="utf-8")
    mechanics_config = load_config()

    root_files = {path.name for path in docs_root.iterdir() if path.is_file()}
    unexpected_root_files = sorted(root_files - ALLOWED_DOCS_ROOT_FILES)
    if unexpected_root_files:
        issues.append(
            "docs/ root has unexpected flat files: " + ", ".join(unexpected_root_files)
        )

    subdirs = {path.name for path in docs_root.iterdir() if path.is_dir()}
    unexpected_subdirs = sorted(subdirs - ALLOWED_DOCS_SUBDIRS)
    if unexpected_subdirs:
        issues.append(
            "docs/ root has unexpected subdirectories: " + ", ".join(unexpected_subdirs)
        )

    for district, required_files in REQUIRED_DOCS_DISTRICT_FILES.items():
        district_root = docs_root / district
        if not district_root.is_dir():
            issues.append(f"docs/{district}/ must exist")
            continue
        missing = sorted(name for name in required_files if not (district_root / name).is_file())
        if missing:
            issues.append(f"docs/{district}/ missing required files: " + ", ".join(missing))

    if not (docs_root / "decisions" / "AGENTS.md").is_file():
        issues.append("docs/decisions/AGENTS.md must exist")
    if not (docs_root / "decisions" / "README.md").is_file():
        issues.append("docs/decisions/README.md must exist")

    for retired_district in RETIRED_DOCS_DISTRICTS:
        if (docs_root / retired_district).exists():
            issues.append(
                f"docs/{retired_district}/ should not exist; use mechanics/{retired_district}/"
            )

    for package in mechanics_config["packages"]:
        for former_path in package["former_flat_paths"]:
            if former_path.count("/") == 1 and (REPO_ROOT / former_path).exists():
                issues.append(f"flat docs-root file still exists: {former_path}")

    for snippet in RETIRED_README_SNIPPETS:
        if snippet in docs_readme:
            issues.append(f"docs/README.md contains retired docs-district route {snippet!r}")

    return issues


def main() -> int:
    issues = validate()

    if issues:
        print("Docs district validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] retired docs districts are absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
