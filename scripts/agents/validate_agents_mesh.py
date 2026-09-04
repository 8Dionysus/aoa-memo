#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from agents_mesh_common import (
    AgentsMeshError,
    card_contracts,
    canonical_card_paths,
    iter_agents_cards,
    load_mesh_config,
    markdown_headings,
    posix_rel,
    repo_root_from_script,
    top_level_exemptions,
)


def route_residue_issues(repo_root: Path) -> list[str]:
    """Check only validation sections, ignoring fenced design examples."""
    empty = re.compile(r"^#{1,6}\s+(?:Validation|Verify|Verification|Checks?|Testing)\s*$", re.I)
    validation = re.compile(r"(?:validation|verify|verification|checks?|testing)", re.I)
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
                if empty.fullmatch(line):
                    cursor = index + 1
                    while cursor < len(lines) and not lines[cursor].strip():
                        cursor += 1
                    if cursor >= len(lines) or re.match(r"^#{1,6}\s+", lines[cursor]):
                        issues.append(f"{path.relative_to(repo_root)}:{index + 1}: empty validation section")
                continue
            if not validation.search(section) or not stripped.endswith(":"):
                cursor = index + 1
                while cursor < len(lines) and not lines[cursor].strip():
                    cursor += 1
                if (
                    stripped.endswith(":")
                    and
                    re.match(r"^\s*[-*+]\s+", line)
                    and cursor < len(lines)
                    and re.match(r"^\s*[-*+]\s+", lines[cursor])
                    and len(line) - len(line.lstrip())
                    == len(lines[cursor]) - len(lines[cursor].lstrip())
                ):
                    issues.append(f"{path.relative_to(repo_root)}:{index + 1}: empty same-level bullet lead-in")
                continue
            cursor = index + 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            next_line = lines[cursor].strip() if cursor < len(lines) else ""
            if (
                cursor >= len(lines)
                or re.match(r"^#{1,6}\s+", lines[cursor])
                or next_line.endswith(":")
                or "validation route" in next_line.lower()
            ):
                issues.append(f"{path.relative_to(repo_root)}:{index + 1}: dangling validation lead-in")
    return issues


REQUIRED_CONFIG_REFS = (
    "authority_ref",
    "system_design_ref",
    "root_agents_ref",
    "route_contract_ref",
    "generated_ref",
)
STALE_ROOT_SCRIPT_COMMAND_RE = re.compile(
    r"python scripts/(?!(ci_gate\.py|release_check\.py|validation_lanes\.py|memory/|agents/|mechanics/|root-topology/|release/))"
)
ACTIVE_COMMAND_FENCE_RE = re.compile(
    r"^ {0,3}```(?:bash|console|sh|shell|zsh)(?:\s+.*)?$", re.IGNORECASE | re.MULTILINE
)
ACTIVE_COMMAND_LINE_RE = re.compile(
    r"^[ \t]*(?:[-*][ \t]+)?`?(?:python3?(?:[ \t]+-m)?[ \t]+(?:scripts/|mechanics/|tests/|-[A-Za-z]|[A-Za-z0-9_.-]+\.py)|pytest(?=[ \t])|"
    r"uv[ \t]+run[ \t]+pytest\b|git[ \t]+(?:status|diff|push|pull|merge|checkout|switch)\b|"
    r"gh[ \t]+(?:pr|run)\b|aoa[ \t]+release\b)", re.IGNORECASE | re.MULTILINE
)
UNCONDITIONAL_READ_HEADING_RE = re.compile(
    r"^##\s+(?:Start here|Read before editing|Read Before Editing|Reading Order(?: Shape)?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
LEVEL_ONE_HEADING_RE = re.compile(r"^#\s+\S.*$", re.MULTILINE)
AGGREGATED_VALIDATION_MARKER_RE = re.compile(
    r"^(?:<!-- Preserved on-demand procedure from `|#{1,6}\s+Preserved inline procedure from `)",
    re.MULTILINE,
)
VALIDATION_COMMAND_FENCE_RE = re.compile(
    r"^ {0,3}```(?P<language>bash|console|sh|shell|zsh|powershell|pwsh|text|plaintext|terminal)?(?:\s+.*)?$",
    re.IGNORECASE,
)
EXECUTABLE_VALIDATION_LINE_RE = re.compile(
    r"^(?:(?:[A-Za-z_][A-Za-z0-9_]*=[^\s]+)\s+)*(?:"
    r"python3?(?:\s+-m)?\s+|pytest(?:\s|$)|uv\s+run\s+|"
    r"git\s+|gh\s+|aoa\s+|skills-ref\s+|ruff\s+|mypy(?:\s|$)|"
    r"bash\s+|sh\s+)",
    re.IGNORECASE,
)


def tracked_top_level_dirs(repo_root: Path) -> set[str]:
    result = subprocess.run(
        ("git", "-C", str(repo_root), "ls-files", "-z"),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return {
            child.name
            for child in repo_root.iterdir()
            if child.is_dir() and not child.is_symlink()
        }
    tracked_dirs: set[str] = set()
    for raw_path in result.stdout.split("\0"):
        if "/" not in raw_path:
            continue
        top_level = raw_path.split("/", 1)[0]
        if top_level:
            tracked_dirs.add(top_level)
    return tracked_dirs


def tracked_agents_card_paths(repo_root: Path) -> tuple[str, ...]:
    """Return every tracked AGENTS.md card, including preserved legacy cards."""
    result = subprocess.run(
        ("git", "-C", str(repo_root), "ls-files", "-z"),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return tuple(
            sorted(
                rel_path
                for rel_path in result.stdout.split("\0")
                if rel_path and Path(rel_path).name == "AGENTS.md"
            )
        )
    return tuple(
        sorted(
            posix_rel(path, repo_root)
            for path in repo_root.rglob("AGENTS.md")
            if ".git" not in path.parts and ".deps" not in path.parts
        )
    )


def validation_route_issues(
    repo_root: Path, agents_paths: tuple[str, ...]
) -> list[str]:
    """Keep executable procedures local and prevent recursive route aggregates."""
    issues: list[str] = []
    seen_routes: set[str] = set()
    for agents_rel in agents_paths:
        validation_rel = (Path(agents_rel).parent / "VALIDATION.md").as_posix()
        if validation_rel in seen_routes:
            continue
        seen_routes.add(validation_rel)
        validation_path = repo_root / validation_rel
        if not validation_path.is_file() or validation_path.is_symlink():
            issues.append(
                f"{agents_rel}: same-directory on-demand route is missing: {validation_rel}"
            )
            continue
        text = validation_path.read_text(encoding="utf-8")
        level_one_headings = LEVEL_ONE_HEADING_RE.findall(text)
        if len(level_one_headings) != 1:
            issues.append(
                f"{validation_rel}: must contain exactly one level-1 heading, "
                f"found {len(level_one_headings)}"
            )
        marker = AGGREGATED_VALIDATION_MARKER_RE.search(text)
        if marker:
            issues.append(
                f"{validation_rel}: contains embedded validation-route aggregate marker "
                f"{marker.group(0)!r}"
            )
        if re.search(r"AGENTS\.md#validation\b", text, re.IGNORECASE):
            issues.append(
                f"{validation_rel}: executable procedure must not route back to AGENTS.md#validation"
            )
        if "Shared executable routes remain owned by `VALIDATION.md`" in text:
            issues.append(
                f"{validation_rel}: nested validation owner must be an explicit linked path or lane, not bare VALIDATION.md"
            )
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.strip().lower() != "run from the repository root:":
                continue
            cursor = index + 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if cursor >= len(lines) or not lines[cursor].lstrip().startswith("```"):
                issues.append(
                    f"{validation_rel}:{index + 1}: dangling repository-root command lead-in"
                )
    return issues


def _validation_commands(text: str) -> list[tuple[int, str]]:
    """Extract normalized executable invocations from command fences."""
    commands: list[tuple[int, str]] = []
    in_command_fence = False
    buffer: list[str] = []
    start_line = 0

    def flush() -> None:
        nonlocal buffer, start_line
        if not buffer:
            return
        command = " ".join(part.strip().rstrip("\\`").strip() for part in buffer)
        command = re.sub(r"\s+", " ", command).strip()
        if EXECUTABLE_VALIDATION_LINE_RE.match(command):
            commands.append((start_line, command))
        buffer = []
        start_line = 0

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not in_command_fence:
            if VALIDATION_COMMAND_FENCE_RE.match(raw_line):
                in_command_fence = True
            continue
        if stripped.startswith("```"):
            flush()
            in_command_fence = False
            continue
        if not stripped or stripped.startswith("#"):
            flush()
            continue
        line = re.sub(r"^(?:\$|PS>)\s*", "", stripped)
        if buffer:
            buffer.append(line)
            if not line.endswith(("\\", "`")):
                flush()
            continue
        if EXECUTABLE_VALIDATION_LINE_RE.match(line):
            buffer = [line]
            start_line = line_number
            if not line.endswith(("\\", "`")):
                flush()
    flush()
    return commands


def validation_command_ownership_issues(
    repo_root: Path, agents_paths: tuple[str, ...]
) -> list[str]:
    """Reject copied executable invocations across on-demand route owners."""
    occurrences: dict[str, list[tuple[str, int]]] = {}
    validation_paths = {
        (Path(agents_rel).parent / "VALIDATION.md").as_posix()
        for agents_rel in agents_paths
    }
    for validation_rel in sorted(validation_paths):
        path = repo_root / validation_rel
        if not path.is_file() or path.is_symlink():
            continue
        for line_number, command in _validation_commands(
            path.read_text(encoding="utf-8")
        ):
            occurrences.setdefault(command, []).append(
                (validation_rel, line_number)
            )

    issues: list[str] = []
    for command, locations in sorted(occurrences.items()):
        if len(locations) < 2:
            continue
        rendered = ", ".join(f"{path}:{line}" for path, line in locations)
        issues.append(
            f"validation command has multiple human owners: {command!r} ({rendered})"
        )
    return issues


def validate(repo_root: Path) -> list[str]:
    issues: list[str] = route_residue_issues(repo_root)
    agents_paths = tracked_agents_card_paths(repo_root)
    issues.extend(validation_route_issues(repo_root, agents_paths))
    issues.extend(validation_command_ownership_issues(repo_root, agents_paths))
    config = load_mesh_config(repo_root)

    for key in REQUIRED_CONFIG_REFS:
        value = config.get(key)
        if not isinstance(value, str) or not value:
            issues.append(f"config/agents/agents_mesh.json: {key} must be a non-empty path string")
            continue
        if key != "generated_ref" and not (repo_root / value).is_file():
            issues.append(f"config/agents/agents_mesh.json: {key} target is missing: {value}")

    cards = canonical_card_paths(config)
    if len(cards) != len(set(cards)):
        issues.append("config/agents/agents_mesh.json: canonical_cards contains duplicates")

    discovered = {posix_rel(path, repo_root) for path in iter_agents_cards(repo_root, config)}
    for rel_path in cards:
        if rel_path not in discovered:
            issues.append(f"{rel_path}: canonical AGENTS.md card is not discovered")

    migration_cards = sorted(discovered - set(cards))
    if migration_cards:
        issues.append(
            "config/agents/agents_mesh.json: unregistered AGENTS.md cards exist: "
            + ", ".join(migration_cards)
        )

    active_cards = [repo_root / rel_path for rel_path in discovered]
    design_card = repo_root / "DESIGN.AGENTS.md"
    if design_card.is_file():
        active_cards.append(design_card)
    for path in active_cards:
        rel_path = posix_rel(path, repo_root)
        text = path.read_text(encoding="utf-8")
        if ACTIVE_COMMAND_FENCE_RE.search(text):
            issues.append(f"{rel_path}: active agent guidance must route runnable commands to VALIDATION.md")
        if ACTIVE_COMMAND_LINE_RE.search(text):
            issues.append(f"{rel_path}: active agent guidance contains a runnable command line")
        if UNCONDITIONAL_READ_HEADING_RE.search(text):
            issues.append(f"{rel_path}: unconditional reading inventory must be task-conditional")

    for contract in card_contracts(config):
        rel_path = contract["path"]
        path = repo_root / rel_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        headings = markdown_headings(text)
        if not headings:
            issues.append(f"{rel_path}: must contain at least one markdown heading")
        if not headings[0].startswith("# "):
            issues.append(f"{rel_path}: first heading must be level 1")
        stale_command = STALE_ROOT_SCRIPT_COMMAND_RE.search(text)
        if stale_command:
            issues.append(
                f"{rel_path}: contains stale flat root script command {stale_command.group(0)!r}"
            )
        line_count = len(text.strip().splitlines())
        if line_count < contract["min_lines"]:
            issues.append(
                f"{rel_path}: must contain at least {contract['min_lines']} lines of guidance"
            )
        for snippet in contract["required_snippets"]:
            if snippet not in text:
                issues.append(f"{rel_path}: missing required snippet {snippet!r}")

    exemptions = top_level_exemptions(config)
    for name in sorted(tracked_top_level_dirs(repo_root)):
        if name in exemptions:
            continue
        local_card = repo_root / name / "AGENTS.md"
        if not local_card.is_file():
            issues.append(f"{name}/: tracked top-level directory lacks AGENTS.md")

    boundary_rules = config.get("neighbor_doc_boundaries", ())
    if not isinstance(boundary_rules, list):
        issues.append("config/agents/agents_mesh.json: neighbor_doc_boundaries must be a list")
    else:
        for rule in boundary_rules:
            if not isinstance(rule, dict):
                issues.append("config/agents/agents_mesh.json: neighbor_doc_boundaries entries must be objects")
                continue
            rel_path = rule.get("path")
            if not isinstance(rel_path, str) or not rel_path:
                issues.append("config/agents/agents_mesh.json: neighbor_doc_boundaries path must be a string")
                continue
            path = repo_root / rel_path
            if not path.is_file():
                issues.append(f"{rel_path}: neighbor doc boundary target is missing")
                continue
            text = path.read_text(encoding="utf-8")
            required = rule.get("required_snippets", ())
            forbidden = rule.get("forbidden_snippets", ())
            if not isinstance(required, list):
                issues.append(f"{rel_path}: required_snippets must be a list")
                required = ()
            if not isinstance(forbidden, list):
                issues.append(f"{rel_path}: forbidden_snippets must be a list")
                forbidden = ()
            for snippet in required:
                if str(snippet) not in text:
                    issues.append(f"{rel_path}: missing required neighbor-boundary snippet {snippet!r}")
            for snippet in forbidden:
                if str(snippet) in text:
                    issues.append(f"{rel_path}: contains AGENTS-owned guidance snippet {snippet!r}")

    return issues


def main() -> int:
    repo_root = repo_root_from_script(Path(__file__))
    try:
        issues = validate(repo_root)
    except AgentsMeshError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    if issues:
        print("AGENTS mesh validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] AGENTS mesh config, card contracts, and top-level coverage are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
