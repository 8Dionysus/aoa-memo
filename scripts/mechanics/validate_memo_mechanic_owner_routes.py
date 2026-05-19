#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from memo_mechanic_owner_routes_common import GENERATED_PATH, validate_payload


def main() -> int:
    if not GENERATED_PATH.is_file():
        print("[error] generated/mechanics/memo_mechanic_owner_routes.min.json is missing", file=sys.stderr)
        return 1
    payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    issues = validate_payload(payload)
    if issues:
        print("Memo mechanic owner-route validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("[ok] generated memo mechanic owner-route matrix is valid and current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
