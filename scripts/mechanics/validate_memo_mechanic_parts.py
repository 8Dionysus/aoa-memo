#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

from memo_mechanics_common import REPO_ROOT, load_config


ACTIVE_PARTS_HEADING = "## Active Parts"
INTERFACE_HEADING = "## Interface"
ALLOWED_HEADERS = {
    ("Part", "Source Docs", "Contract"),
    ("Part", "Source Surface", "Contract"),
}
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def part_slug(part_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", part_name.lower()).strip("-")
    return slug or "part"


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def active_parts_table(lines: list[str]) -> tuple[int | None, list[str]]:
    for index, line in enumerate(lines):
        if line.strip() == ACTIVE_PARTS_HEADING:
            for table_index in range(index + 1, len(lines)):
                candidate = lines[table_index].strip()
                if not candidate:
                    continue
                if candidate.startswith("|"):
                    rows: list[str] = []
                    for row in lines[table_index:]:
                        stripped = row.strip()
                        if stripped.startswith("## ") and rows:
                            break
                        if stripped.startswith("|"):
                            rows.append(stripped)
                    return table_index, rows
                if candidate.startswith("## "):
                    return None, []
    return None, []


def local_link_path(target: str) -> str | None:
    if target.startswith(("http://", "https://", "#")):
        return None
    path = target.split("#", 1)[0].split("?", 1)[0]
    return path or None


def validate_source_links(parts_path: Path, source_cell: str) -> list[str]:
    issues: list[str] = []
    for target in LINK_PATTERN.findall(source_cell):
        path = local_link_path(target)
        if path is None:
            continue
        target_path = (parts_path.parent / path).resolve()
        try:
            target_path.relative_to(REPO_ROOT)
        except ValueError:
            issues.append(f"{parts_path.relative_to(REPO_ROOT)} links outside repo: {target}")
            continue
        if not target_path.exists():
            issues.append(f"{parts_path.relative_to(REPO_ROOT)} links missing source: {target}")
    return issues


def validate_markdown_links(markdown_path: Path) -> list[str]:
    if not markdown_path.is_file():
        return [f"{markdown_path.relative_to(REPO_ROOT)} is missing"]
    return validate_source_links(markdown_path, markdown_path.read_text(encoding="utf-8"))


def validate_parts_tree(slug: str, rows: list[str]) -> list[str]:
    issues: list[str] = []
    package_root = REPO_ROOT / "mechanics" / slug
    parts_root = package_root / "parts"
    rel_root = parts_root.relative_to(REPO_ROOT).as_posix()

    root_agents = parts_root / "AGENTS.md"
    root_readme = parts_root / "README.md"
    for path in (root_agents, root_readme):
        if not path.is_file():
            issues.append(f"{path.relative_to(REPO_ROOT).as_posix()} is missing")
        else:
            issues.extend(validate_markdown_links(path))

    root_readme_text = root_readme.read_text(encoding="utf-8") if root_readme.is_file() else ""

    for row in rows:
        cells = split_table_row(row)
        if len(cells) != 3:
            continue
        part, _source_cell, contract = cells
        slug_part = part_slug(part)
        part_root = parts_root / slug_part
        rel_part = part_root.relative_to(REPO_ROOT).as_posix()

        if not part_root.is_dir():
            issues.append(f"{rel_part}/ is missing for Active Parts row {part!r}")
            continue

        if f"{slug_part}/README.md" not in root_readme_text:
            issues.append(f"{rel_root}/README.md must link part {slug_part}/README.md")

        readme = part_root / "README.md"
        contract_path = part_root / "CONTRACT.md"
        validation = part_root / "VALIDATION.md"
        for path in (readme, contract_path, validation):
            if not path.is_file():
                issues.append(f"{path.relative_to(REPO_ROOT).as_posix()} is missing")
                continue
            issues.extend(validate_markdown_links(path))

        if readme.is_file():
            readme_text = readme.read_text(encoding="utf-8")
            first_line = readme_text.splitlines()[0] if readme_text.splitlines() else ""
            if not first_line.startswith("# ") or part.lower() not in first_line.lower():
                issues.append(f"{rel_part}/README.md title must name part {part!r}")
            for required in ("CONTRACT.md", "VALIDATION.md"):
                if required not in readme_text:
                    issues.append(f"{rel_part}/README.md must link {required}")

        if contract_path.is_file():
            contract_text = contract_path.read_text(encoding="utf-8")
            for heading in ("## Contract", "## Stop-lines"):
                if heading not in contract_text:
                    issues.append(f"{rel_part}/CONTRACT.md must include {heading}")
            if contract not in contract_text:
                issues.append(f"{rel_part}/CONTRACT.md must preserve the PARTS.md contract text")

        if validation.is_file():
            validation_text = validation.read_text(encoding="utf-8")
            if "../../VALIDATION.md" not in validation_text:
                issues.append(
                    f"{rel_part}/VALIDATION.md must link the package validation owner"
                )

    return issues


def validate_parts_file(slug: str, docs: list[str]) -> list[str]:
    issues: list[str] = []
    parts_path = REPO_ROOT / "mechanics" / slug / "PARTS.md"
    if not parts_path.is_file():
        return [f"mechanics/{slug}/PARTS.md is missing"]

    text = parts_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    rel = parts_path.relative_to(REPO_ROOT).as_posix()

    if not lines or lines[0].strip() != f"# {slug.replace('-', ' ').title()} Parts":
        issues.append(f"{rel} must start with a package Parts title")
    if ACTIVE_PARTS_HEADING not in text:
        issues.append(f"{rel} must include {ACTIVE_PARTS_HEADING}")
    if INTERFACE_HEADING not in text:
        issues.append(f"{rel} must include {INTERFACE_HEADING}")

    _, rows = active_parts_table(lines)
    if len(rows) < 3:
        issues.append(f"{rel} must include a non-empty Active Parts table")
        return issues

    header = tuple(split_table_row(rows[0]))
    if header not in ALLOWED_HEADERS:
        issues.append(f"{rel} Active Parts table must use Part, Source Docs/Surface, Contract columns")
    if not re.fullmatch(r"\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|", rows[1]):
        issues.append(f"{rel} Active Parts table must use a markdown separator row")

    seen_parts: set[str] = set()
    for row in rows[2:]:
        cells = split_table_row(row)
        if len(cells) != 3:
            issues.append(f"{rel} Active Parts row must have exactly three cells: {row}")
            continue
        part, source_cell, contract = cells
        if not part:
            issues.append(f"{rel} Active Parts row has empty part name")
        if part in seen_parts:
            issues.append(f"{rel} duplicates Active Parts row {part!r}")
        seen_parts.add(part)
        if not source_cell:
            issues.append(f"{rel} Active Parts row {part!r} has empty source cell")
        if not contract:
            issues.append(f"{rel} Active Parts row {part!r} has empty contract cell")
        issues.extend(validate_source_links(parts_path, source_cell))

    for doc in docs:
        if doc not in text:
            issues.append(f"{rel} must route active doc {doc}")

    issues.extend(validate_parts_tree(slug, rows[2:]))

    return issues


def validate() -> list[str]:
    config = load_config()
    issues: list[str] = []
    for package in config["packages"]:
        issues.extend(validate_parts_file(package["slug"], package["docs"]))
    return issues


def main() -> int:
    issues = validate()
    if issues:
        print("Memo mechanic parts validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("[ok] memo mechanic parts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
