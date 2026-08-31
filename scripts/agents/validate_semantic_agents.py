#!/usr/bin/env python3
"""Validate Pack 4 semantic-layer AGENTS.md guidance for aoa-memo."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AgentsDocSpec:
    path: Path
    required_snippets: tuple[str, ...]


REQUIRED_DOCS: tuple[AgentsDocSpec, ...] = (
    AgentsDocSpec(
        Path('skills/AGENTS.md'),
        (
            'canonical `aoa-memo/skills/` home',
            'managed OS user-profile copy',
            'Manual isolated',
            'Green output',
            'makes no outcome claim.',
            'skills-ref validate',
        ),
    ),
    AgentsDocSpec(
        Path('config/AGENTS.md'),
        (
            'guardrail-support',
            'memory truth',
            'public-safe',
            'provenance drift',
            'nearest `VALIDATION.md` route',
        ),
    ),
    AgentsDocSpec(
        Path('docs/AGENTS.md'),
        (
            'memory models',
            'memory is not proof',
            'temporal relevance',
            'downstream owner repo',
            'nearest `VALIDATION.md` route',
        ),
    ),
    AgentsDocSpec(
        Path('tests/AGENTS.md'),
        (
            'memory schemas',
            'recall contracts',
            'provenance loss',
            'public-safe',
            'nearest `VALIDATION.md` route',
        ),
    ),
)


def _display(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


_EMPTY_SECTION_RE = re.compile(
    r"^#{1,6}\s+(?:Validation|Verify|Verification|Checks?|Testing)\s*$",
    re.IGNORECASE,
)
_VALIDATION_SECTION_RE = re.compile(
    r"(?:validation|verify|verification|checks?|testing)",
    re.IGNORECASE,
)


def route_residue_issues(repo_root: Path) -> list[str]:
    """Check only validation sections, ignoring fenced design examples."""
    issues: list[str] = []
    paths = sorted(repo_root.rglob("AGENTS.md")) + sorted(repo_root.rglob("DESIGN.AGENTS.md"))
    for path in paths:
        if ".git" in path.parts or ".deps" in path.parts:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        fenced = False
        section = ""
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if heading:
                section = heading.group(1)
                if _EMPTY_SECTION_RE.fullmatch(line):
                    cursor = index + 1
                    while cursor < len(lines) and not lines[cursor].strip():
                        cursor += 1
                    if cursor >= len(lines) or re.match(r"^#{1,6}\s+", lines[cursor]):
                        issues.append(f"{path.relative_to(repo_root)}:{index + 1}: empty validation section")
                continue
            if not _VALIDATION_SECTION_RE.search(section) or not stripped.endswith(":"):
                continue
            cursor = index + 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if cursor >= len(lines) or re.match(r"^#{1,6}\s+", lines[cursor]):
                issues.append(f"{path.relative_to(repo_root)}:{index + 1}: dangling validation lead-in")
    return issues


def validate(repo_root: Path = REPO_ROOT) -> list[str]:
    issues: list[str] = []
    issues.extend(route_residue_issues(repo_root))
    issues.extend(route_residue_issues(repo_root))
    for spec in REQUIRED_DOCS:
        path = repo_root / spec.path
        if not path.is_file():
            issues.append(f"{spec.path.as_posix()}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip().startswith("# AGENTS.md"):
            issues.append(f"{spec.path.as_posix()}: must start with '# AGENTS.md'")
        for snippet in spec.required_snippets:
            if snippet not in text:
                issues.append(
                    f"{spec.path.as_posix()}: missing required snippet {snippet!r}"
                )
    return issues


def main() -> int:
    issues = validate(REPO_ROOT)
    if issues:
        print("Pack 4 semantic AGENTS validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print(f"[ok] Pack 4 semantic AGENTS docs are present and shaped: {len(REQUIRED_DOCS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
