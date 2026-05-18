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

TITAN_DOCS = {
    "TITAN_AUDIT_MEMORY_POLICY.md",
    "TITAN_BRIDGE_MEMORY_POSTURE.md",
    "TITAN_CLOSEOUT_MEMORY_POSTURE.md",
    "TITAN_CONSOLE_MEMORY_DIGEST.md",
    "TITAN_MEMORY_LOOM_POSTURE.md",
    "TITAN_MEMORY_POSTURE.md",
    "TITAN_PERSONALITY_MEMORY_POLICY.md",
    "TITAN_RECALL_CANDIDATE_POLICY.md",
    "TITAN_REMEMBRANCE_SOURCE_REF_POLICY.md",
    "TITAN_SWARM_MEMORY_POLICY.md",
}

DISTRICTS = {
    "agon": {
        "docs": AGON_DOCS,
        "pattern": "AGON_*.md",
        "readme_snippets": ("docs/agon/", "Agon Memo District", "AGON_*"),
    },
    "titan": {
        "docs": TITAN_DOCS,
        "pattern": "TITAN_*.md",
        "readme_snippets": ("docs/titan/", "Titan Memo District", "TITAN_*"),
    },
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


def validate_district(
    issues: list[str],
    docs_root: Path,
    docs_readme: str,
    name: str,
    expected_docs: set[str],
    pattern: str,
    readme_snippets: tuple[str, ...],
) -> None:
    district_root = docs_root / name

    if not (district_root / "AGENTS.md").is_file():
        issues.append(f"docs/{name}/AGENTS.md is missing")
    if not (district_root / "README.md").is_file():
        issues.append(f"docs/{name}/README.md is missing")

    flat_docs = sorted(filename for filename in expected_docs if (docs_root / filename).exists())
    if flat_docs:
        issues.append(
            f"flat docs-root {name} files remain: " + ", ".join(flat_docs)
        )

    present_docs = sorted(path.name for path in district_root.glob(pattern))
    present_docs = [
        filename
        for filename in present_docs
        if filename not in {"AGENTS.md", "README.md"}
    ]
    if set(present_docs) != expected_docs:
        missing = sorted(expected_docs - set(present_docs))
        extra = sorted(set(present_docs) - expected_docs)
        if missing:
            issues.append(f"docs/{name}/ is missing docs: " + ", ".join(missing))
        if extra:
            issues.append(f"docs/{name}/ has unregistered docs: " + ", ".join(extra))

    for snippet in readme_snippets:
        if snippet not in docs_readme:
            issues.append(f"docs/README.md must mention {snippet!r}")

    if (district_root / "README.md").is_file():
        district_readme = (district_root / "README.md").read_text(encoding="utf-8")
        for filename in sorted(expected_docs):
            if filename not in district_readme:
                issues.append(f"docs/{name}/README.md must list {filename}")


def validate() -> list[str]:
    issues: list[str] = []
    docs_root = REPO_ROOT / "docs"
    docs_readme = (docs_root / "README.md").read_text(encoding="utf-8")
    for retired_district in ("adoption", "writeback", "retention"):
        if (docs_root / retired_district).exists():
            issues.append(
                f"docs/{retired_district}/ should not exist; use mechanics/{retired_district}/"
            )
    for name, district in DISTRICTS.items():
        validate_district(
            issues,
            docs_root,
            docs_readme,
            name,
            district["docs"],
            district["pattern"],
            district["readme_snippets"],
        )

    moved_doc_names = sorted(
        filename for district in DISTRICTS.values() for filename in district["docs"]
    )
    stale_paths = tuple("docs/" + filename for filename in moved_doc_names)
    for path in tracked_files():
        if not is_text_candidate(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(REPO_ROOT).as_posix()
        for stale_path in stale_paths:
            if stale_path in text:
                issues.append(f"{rel}: contains stale flat docs-root reference")

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
