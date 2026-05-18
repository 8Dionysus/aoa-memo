#!/usr/bin/env python3
from __future__ import annotations

import sys

from memo_mechanics_common import REPO_ROOT, load_config


RETIRED_DOCS_DISTRICTS = ("agon", "titan", "adoption", "writeback", "retention")
RETIRED_README_SNIPPETS = (
    "docs/agon/",
    "docs/titan/",
    "Agon Memo District",
    "Titan Memo District",
)


def validate() -> list[str]:
    issues: list[str] = []
    docs_root = REPO_ROOT / "docs"
    docs_readme = (docs_root / "README.md").read_text(encoding="utf-8")
    mechanics_config = load_config()

    for retired_district in RETIRED_DOCS_DISTRICTS:
        if (docs_root / retired_district).exists():
            issues.append(
                f"docs/{retired_district}/ should not exist; use mechanics/{retired_district}/"
            )

    for package in mechanics_config["packages"]:
        for former_path in package["former_flat_paths"]:
            if former_path.count("/") == 1 and (REPO_ROOT / former_path).exists():
                issues.append(f"flat docs-root file still exists: {former_path}")

    for snippet in RETIRED_README_SNIPPETS:
        if snippet in docs_readme:
            issues.append(f"docs/README.md contains retired docs-district route {snippet!r}")

    return issues


def main() -> int:
    issues = validate()

    if issues:
        print("Docs district validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] retired docs districts are absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
