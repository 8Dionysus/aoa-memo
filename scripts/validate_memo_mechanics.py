#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import re
from pathlib import Path

from memo_mechanics_common import (
    PACKAGE_REQUIRED_FILES,
    README_HEADINGS,
    REPO_ROOT,
    load_config,
)


SKIP_SUFFIXES = (".pyc",)
SKIP_PATH_PARTS = {".git", ".pytest_cache", "__pycache__"}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ("git", "-C", str(REPO_ROOT), "ls-files", "-z"),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")
    return [REPO_ROOT / raw for raw in result.stdout.split("\0") if raw]


def is_text_candidate(path: Path) -> bool:
    relative_parts = set(path.relative_to(REPO_ROOT).parts)
    if relative_parts & SKIP_PATH_PARTS:
        return False
    return not path.name.endswith(SKIP_SUFFIXES)


def validate() -> list[str]:
    config = load_config()
    issues: list[str] = []

    for root_file in ("mechanics/AGENTS.md", "mechanics/README.md", "mechanics/ARTIFACT_TOPOLOGY.md"):
        if not (REPO_ROOT / root_file).is_file():
            issues.append(f"{root_file} is missing")

    docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    root_readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    mechanics_readme = (REPO_ROOT / "mechanics" / "README.md").read_text(encoding="utf-8")

    all_former_flat_paths: list[str] = []
    for package in config["packages"]:
        slug = package["slug"]
        package_root = REPO_ROOT / "mechanics" / slug
        docs_root = package_root / "docs"
        operation = package.get("operation")
        os_abyss_role = package.get("os_abyss_role")

        if not isinstance(operation, str) or not operation.strip():
            issues.append(f"config/memo_mechanics.json: {slug} must name an operation")
        if not isinstance(os_abyss_role, str) or not os_abyss_role.strip():
            issues.append(f"config/memo_mechanics.json: {slug} must name its OS Abyss role")

        if f"[{slug}]" not in mechanics_readme:
            issues.append(f"mechanics/README.md must route to {slug}")
        if f"mechanics/{slug}/" not in docs_readme:
            issues.append(f"docs/README.md must route to mechanics/{slug}/")
        if f"mechanics/{slug}/" not in root_readme:
            issues.append(f"README.md must route to mechanics/{slug}/")

        for relative in PACKAGE_REQUIRED_FILES:
            if not (package_root / relative).is_file():
                issues.append(f"mechanics/{slug}/{relative} is missing")

        readme_path = package_root / "README.md"
        if readme_path.is_file():
            readme = readme_path.read_text(encoding="utf-8")
            for heading in README_HEADINGS:
                if heading not in readme:
                    issues.append(f"mechanics/{slug}/README.md must include {heading!r}")
            if isinstance(operation, str) and operation.strip() and operation not in readme:
                issues.append(f"mechanics/{slug}/README.md must cite its configured operation")

        expected_docs = set(package["docs"])
        present_docs = {
            path.name
            for path in docs_root.glob("*.md")
            if path.name not in {"AGENTS.md", "README.md"}
        } if docs_root.is_dir() else set()
        if present_docs != expected_docs:
            missing = sorted(expected_docs - present_docs)
            extra = sorted(present_docs - expected_docs)
            if missing:
                issues.append(f"mechanics/{slug}/docs is missing docs: " + ", ".join(missing))
            if extra:
                issues.append(f"mechanics/{slug}/docs has unregistered docs: " + ", ".join(extra))

        parts_text = (package_root / "PARTS.md").read_text(encoding="utf-8") if (package_root / "PARTS.md").is_file() else ""
        legacy_text = (package_root / "legacy" / "INDEX.md").read_text(encoding="utf-8") if (package_root / "legacy" / "INDEX.md").is_file() else ""
        for filename in sorted(expected_docs):
            if filename not in parts_text:
                issues.append(f"mechanics/{slug}/PARTS.md must list {filename}")
            active_path = f"mechanics/{slug}/docs/{filename}"
            if active_path not in legacy_text:
                issues.append(f"mechanics/{slug}/legacy/INDEX.md must map {active_path}")

        all_former_flat_paths.extend(package["former_flat_paths"])
        for former_path in package["former_flat_paths"]:
            if (REPO_ROOT / former_path).exists():
                issues.append(f"former flat path still exists: {former_path}")

    forbidden_subdirs = (
        "docs/antifragility",
        "docs/agon",
        "docs/titan",
        "docs/adoption",
        "docs/governance",
        "docs/writeback",
        "docs/retention",
    )
    for forbidden in forbidden_subdirs:
        if (REPO_ROOT / forbidden).exists():
            issues.append(f"{forbidden} should not exist; use mechanics/<slug>/")

    allowed_provenance_refs = {
        f"mechanics/{package['slug']}/legacy/INDEX.md" for package in config["packages"]
    }
    allowed_provenance_refs.update(
        f"mechanics/{package['slug']}/PROVENANCE.md" for package in config["packages"]
    )
    allowed_provenance_refs.add("config/memo_mechanics.json")
    allowed_provenance_refs.add("generated/mechanic_artifacts.min.json")
    allowed_provenance_refs.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "docs" / "decisions").glob("*.md")
    )
    stale_patterns = {
        former_path: re.compile(rf"(?<![A-Za-z0-9_./-]){re.escape(former_path)}")
        for former_path in all_former_flat_paths
    }

    allowed_legacy_prefixes = tuple(
        f"mechanics/{package['slug']}/legacy/" for package in config["packages"]
    )

    for path in tracked_files():
        if not is_text_candidate(path):
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for former_path, pattern in stale_patterns.items():
            if (
                pattern.search(text)
                and rel not in allowed_provenance_refs
                and not rel.startswith(allowed_legacy_prefixes)
            ):
                issues.append(f"{rel}: contains stale flat mechanics source ref {former_path}")

    return issues


def main() -> int:
    try:
        issues = validate()
    except RuntimeError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    if issues:
        print("Memo mechanics validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] memo mechanics topology is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
