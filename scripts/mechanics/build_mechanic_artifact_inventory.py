#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from mechanic_artifact_inventory_common import GENERATED_PATH, build_inventory, render_inventory


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact mechanic artifact inventory.")
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()

    rendered = render_inventory(build_inventory())

    if args.check:
        current = GENERATED_PATH.read_text(encoding="utf-8") if GENERATED_PATH.exists() else ""
        if current != rendered:
            print(
                "[error] generated/mechanics/mechanic_artifacts.min.json is out of date; "
                "run scripts/mechanics/build_mechanic_artifact_inventory.py",
                file=sys.stderr,
            )
            return 1
        print("[ok] generated/mechanics/mechanic_artifacts.min.json is current")
        return 0

    GENERATED_PATH.write_text(rendered, encoding="utf-8")
    print("[ok] wrote generated/mechanics/mechanic_artifacts.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
