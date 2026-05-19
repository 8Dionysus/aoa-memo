#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from mechanic_readiness_common import GENERATED_PATH, build_readiness, render_readiness


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact memo mechanic readiness matrix.")
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()

    rendered = render_readiness(build_readiness())

    if args.check:
        current = GENERATED_PATH.read_text(encoding="utf-8") if GENERATED_PATH.exists() else ""
        if current != rendered:
            print(
                "[error] generated/mechanics/memo_mechanic_readiness.min.json is out of date; "
                "run scripts/mechanics/build_memo_mechanic_readiness.py",
                file=sys.stderr,
            )
            return 1
        print("[ok] generated/mechanics/memo_mechanic_readiness.min.json is current")
        return 0

    GENERATED_PATH.write_text(rendered, encoding="utf-8")
    print("[ok] wrote generated/mechanics/memo_mechanic_readiness.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
