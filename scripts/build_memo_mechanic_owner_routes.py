#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from memo_mechanic_owner_routes_common import GENERATED_PATH, build_owner_routes, render_owner_routes


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact memo mechanic owner-route matrix.")
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()

    rendered = render_owner_routes(build_owner_routes())

    if args.check:
        current = GENERATED_PATH.read_text(encoding="utf-8") if GENERATED_PATH.exists() else ""
        if current != rendered:
            print(
                "[error] generated/memo_mechanic_owner_routes.min.json is out of date; "
                "run scripts/build_memo_mechanic_owner_routes.py",
                file=sys.stderr,
            )
            return 1
        print("[ok] generated/memo_mechanic_owner_routes.min.json is current")
        return 0

    GENERATED_PATH.write_text(rendered, encoding="utf-8")
    print("[ok] wrote generated/memo_mechanic_owner_routes.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
