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


def validate_source_links(parts_path: Path, source_cell: str) -> list[str]:
    issues: list[str] = []
    for target in LINK_PATTERN.findall(source_cell):
        if target.startswith(("http://", "https://", "#")):
            continue
        target_path = (parts_path.parent / target).resolve()
        try:
            target_path.relative_to(REPO_ROOT)
        except ValueError:
            issues.append(f"{parts_path.relative_to(REPO_ROOT)} links outside repo: {target}")
            continue
        if not target_path.exists():
            issues.append(f"{parts_path.relative_to(REPO_ROOT)} links missing source: {target}")
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
