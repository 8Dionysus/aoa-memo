#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

from memo_mechanics_common import GENERATED_PATH, build_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact memo mechanics index.")
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()

    payload = build_index()
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"

    if args.check:
        current = GENERATED_PATH.read_text(encoding="utf-8") if GENERATED_PATH.exists() else ""
        if current != rendered:
            print(
                "[error] generated/memo_mechanics.min.json is out of date; "
                "run scripts/build_memo_mechanics_index.py",
                file=sys.stderr,
            )
            return 1
        print("[ok] generated/memo_mechanics.min.json is current")
        return 0

    GENERATED_PATH.write_text(rendered, encoding="utf-8")
    print("[ok] wrote generated/memo_mechanics.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
