#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_NESTED_AGENTS = {
    REPO_ROOT / "schemas" / "AGENTS.md": {
        "min_lines": 20,
        "required_tokens": (
            "memory_object.schema.json",
            "recall_contract.schema.json",
            "memory_object_surface_manifest.schema.json",
            "memory_chunk_face.schema.json",
            "memory_graph_face.schema.json",
            "Schema edits are contract edits",
            "nearest `VALIDATION.md` route",
        ),
    },
    REPO_ROOT / "examples" / "AGENTS.md": {
        "min_lines": 20,
        "required_tokens": (
            "memory_object_surface_manifest.json",
            "recall_contract.router.semantic.json",
            "recall_contract.object.working.json",
            "mechanics/writeback/parts/<part>/examples/",
            "mechanics/recurrence-support/parts/witness-trace-contract/examples/",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/",
            "sanitized",
            "public",
            "nearest `VALIDATION.md` route",
        ),
    },
    REPO_ROOT / "scripts" / "AGENTS.md": {
        "min_lines": 20,
        "required_tokens": (
            "validate_nested_agents.py",
            "deterministic",
            "hidden runtime infrastructure",
            "nearest `VALIDATION.md` route",
        ),
    },
    REPO_ROOT / "scripts" / "memory" / "validators" / "AGENTS.md": {
        "min_lines": 20,
        "required_tokens": (
            "scripts/memory/validators/",
            "docs/validation/VALIDATOR_TOPOLOGY.md",
            "config/validation_lanes.json",
            "schema",
            "memory-context",
            "runtime",
            "handoff",
            "eval",
            "hidden source of memory meaning",
            "nearest `VALIDATION.md` route",
        ),
    },
    REPO_ROOT / "generated" / "AGENTS.md": {
        "min_lines": 20,
        "required_tokens": (
            "memo_registry.min.json",
            "memory_catalog.json",
            "memory_sections.full.json",
            "memory_object_catalog.json",
            "memory_object_sections.full.json",
            "Do not hand-edit",
            "nearest `VALIDATION.md` route",
        ),
    },
}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required nested AGENTS doc: {display_path(path)}")


def route_residue_issues(repo_root: Path) -> list[str]:
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
                continue
            cursor = index + 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if cursor >= len(lines) or re.match(r"^#{1,6}\s+", lines[cursor]):
                issues.append(f"{path.relative_to(repo_root)}:{index + 1}: dangling validation lead-in")
    return issues


def validate_nested_agents_docs() -> None:
    issues = route_residue_issues(REPO_ROOT)
    if issues:
        fail("route residue detected: " + "; ".join(issues))
    for path, contract in REQUIRED_NESTED_AGENTS.items():
        text = read_text(path)
        stripped = text.strip()
        if not stripped.startswith("# AGENTS.md"):
            fail(f"{display_path(path)} must start with a '# AGENTS.md' heading")

        lines = stripped.splitlines()
        min_lines = int(contract["min_lines"])
        if len(lines) < min_lines:
            fail(f"{display_path(path)} must contain at least {min_lines} lines of guidance")

        for token in contract["required_tokens"]:
            if token not in text:
                fail(f"{display_path(path)} must mention '{token}' explicitly")


def main() -> int:
    try:
        validate_nested_agents_docs()
    except ValidationError as exc:
        print(f"[error] {exc}")
        return 1

    print("[ok] validated nested AGENTS docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
