#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from root_technical_districts_common import GENERATED_PATH, build_index, render_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact root technical district atlas.")
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()

    rendered = render_index(build_index())

    if args.check:
        current = GENERATED_PATH.read_text(encoding="utf-8") if GENERATED_PATH.exists() else ""
        if current != rendered:
            print(
                "[error] generated/root_technical_districts.min.json is out of date; "
                "run scripts/build_root_technical_districts_index.py",
                file=sys.stderr,
            )
            return 1
        print("[ok] generated/root_technical_districts.min.json is current")
        return 0

    GENERATED_PATH.write_text(rendered, encoding="utf-8")
    print("[ok] wrote generated/root_technical_districts.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
