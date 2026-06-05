#!/usr/bin/env python3
"""Build generated lookup indexes for docs/decisions."""

from __future__ import annotations

import argparse
from pathlib import Path

from decision_index_common import (
    REPO_ROOT,
    collect_decision_records,
    load_index_contract,
    render_index_files,
    validate_decision_lane_surfaces,
    validate_decision_index_surfaces,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated decision indexes are missing or stale",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="repository root",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    if args.check:
        issues = validate_decision_index_surfaces(repo_root)
        if issues:
            for location, message in issues:
                print(f"- {location}: {message}")
            return 1
        return 0

    records, issues = collect_decision_records(repo_root)
    issues.extend(validate_decision_lane_surfaces(repo_root))
    issues.extend(load_index_contract(repo_root)[1])
    if issues:
        for location, message in issues:
            print(f"- {location}: {message}")
        return 1

    for relative_path, expected_text in render_index_files(records).items():
        path = repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
