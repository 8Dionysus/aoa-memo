#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from memo_mechanic_cards_common import GENERATED_PATH, SCHEMA_VERSION, validate_payload


def main() -> int:
    if not GENERATED_PATH.is_file():
        print("[error] generated/memo_mechanic_cards.min.json is missing", file=sys.stderr)
        return 1
    payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    issues = validate_payload(payload)
    if issues:
        print("Memo mechanic route-card validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    if payload.get("schema_version") != SCHEMA_VERSION:
        print("[error] generated memo mechanic route-card index has wrong schema_version", file=sys.stderr)
        return 1
    print("[ok] generated memo mechanic route-card index is valid and current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
