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


def validate(repo_root: Path) -> list[str]:
    issues: list[str] = []
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
