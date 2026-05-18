#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path

import validate_memo

ROOT = Path(__file__).resolve().parents[1]
ProjectionBuilder = Callable[[], list[dict[str, object]]]

OUTPUTS: tuple[tuple[Path, ProjectionBuilder], ...] = (
    (validate_memo.QUEST_CATALOG_PATH, validate_memo.build_quest_catalog_projection),
    (validate_memo.QUEST_CATALOG_EXAMPLE_PATH, validate_memo.build_quest_catalog_projection),
    (validate_memo.QUEST_DISPATCH_PATH, validate_memo.build_quest_dispatch_projection),
    (validate_memo.QUEST_DISPATCH_EXAMPLE_PATH, validate_memo.build_quest_dispatch_projection),
)


def render_payload(payload: list[dict[str, object]]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact quest projection surfaces.")
    parser.add_argument("--check", action="store_true", help="fail if generated outputs are stale")
    args = parser.parse_args()

    mismatches: list[str] = []
    for path, builder in OUTPUTS:
        rendered = render_payload(builder())
        relative = path.relative_to(ROOT)
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != rendered:
                mismatches.append(str(relative))
            continue
        path.write_text(rendered, encoding="utf-8")
        print(f"[ok] wrote {relative}")

    if mismatches:
        for relative in mismatches:
            print(
                f"[error] {relative} is out of date; run scripts/build_quest_surfaces.py",
                file=sys.stderr,
            )
        return 1

    if args.check:
        print("[ok] generated quest surfaces are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
