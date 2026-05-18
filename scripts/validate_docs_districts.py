#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

AGON_DOCS = {
    "AGON_DELTA_CHRONICLE_PREBINDING_MODEL.md",
    "AGON_EPISTEMIC_MEMORY_BOUNDARY.md",
    "AGON_EPISTEMIC_MEMORY_BRIDGE.md",
    "AGON_KAG_MEMO_BOUNDARY.md",
    "AGON_KAG_MEMO_EVIDENCE_PACKAGES.md",
    "AGON_MECHANICAL_TRIAL_MEMO_INTAKES.md",
    "AGON_MEMORY_PREBINDING.md",
    "AGON_MEMO_RECURRENCE_REVIEW_BOUNDARY.md",
    "AGON_RANK_MEMORY_BOUNDARY.md",
    "AGON_RETENTION_CANDIDATE_BOUNDARY.md",
    "AGON_RETENTION_CANDIDATE_INTAKE.md",
    "AGON_RETENTION_MEMORY_BRIDGE.md",
    "AGON_SCAR_CANDIDATE_INTAKE_MODEL.md",
    "AGON_SCAR_REQUEST_INTAKE_ALIGNMENT.md",
    "AGON_SLC_MEMORY_BOUNDARY.md",
    "AGON_SLC_MEMORY_BRIDGE.md",
    "AGON_SOPHIAN_MEMO_EVIDENCE.md",
    "AGON_VDS_MEMO_BRIDGE.md",
    "AGON_WAVE11_MEMO_LANDING.md",
    "AGON_WAVE13_MEMO_LANDING.md",
    "AGON_WAVE13_MEMO_STOP_LINES.md",
    "AGON_WAVE14_MEMO_LANDING.md",
    "AGON_WAVE15_MEMO_LANDING.md",
    "AGON_WAVE16_MEMO_LANDING.md",
    "AGON_WAVE17_MEMO_LANDING.md",
    "AGON_WAVE18_MEMO_LANDING.md",
    "AGON_WAVE7_MEMO_LANDING.md",
}

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
    issues: list[str] = []
    docs_root = REPO_ROOT / "docs"
    agon_root = docs_root / "agon"

    if not (agon_root / "AGENTS.md").is_file():
        issues.append("docs/agon/AGENTS.md is missing")
    if not (agon_root / "README.md").is_file():
        issues.append("docs/agon/README.md is missing")

    flat_agon = sorted(path.name for path in docs_root.glob("AGON_*.md"))
    if flat_agon:
        issues.append("flat docs-root Agon files remain: " + ", ".join(flat_agon))

    present_agon = sorted(path.name for path in agon_root.glob("AGON_*.md"))
    if set(present_agon) != AGON_DOCS:
        missing = sorted(AGON_DOCS - set(present_agon))
        extra = sorted(set(present_agon) - AGON_DOCS)
        if missing:
            issues.append("docs/agon/ is missing Agon docs: " + ", ".join(missing))
        if extra:
            issues.append("docs/agon/ has unregistered Agon docs: " + ", ".join(extra))

    docs_readme = (docs_root / "README.md").read_text(encoding="utf-8")
    for snippet in ("docs/agon/", "Agon Memo District", "AGON_*"):
        if snippet not in docs_readme:
            issues.append(f"docs/README.md must mention {snippet!r}")

    agon_readme = (agon_root / "README.md").read_text(encoding="utf-8")
    for filename in sorted(AGON_DOCS):
        if filename not in agon_readme:
            issues.append(f"docs/agon/README.md must list {filename}")

    stale_prefix = "docs/" + "AGON_"
    for path in tracked_files():
        if not is_text_candidate(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(REPO_ROOT).as_posix()
        if stale_prefix in text:
            issues.append(f"{rel}: contains stale flat Agon docs reference")

    return issues


def main() -> int:
    try:
        issues = validate()
    except RuntimeError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    if issues:
        print("Docs district validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] docs districts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
