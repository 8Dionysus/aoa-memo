#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from mechanic_readiness_common import GENERATED_PATH, render_readiness, validate_payload


def main() -> int:
    if not GENERATED_PATH.is_file():
        print(
            "[error] generated/mechanics/memo_mechanic_readiness.min.json is missing; "
            "run scripts/mechanics/build_memo_mechanic_readiness.py",
            file=sys.stderr,
        )
        return 1

    try:
        payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[error] generated/mechanics/memo_mechanic_readiness.min.json is invalid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(payload, dict):
        print("[error] generated/mechanics/memo_mechanic_readiness.min.json must be a JSON object", file=sys.stderr)
        return 1

    issues = validate_payload(payload)
    if GENERATED_PATH.read_text(encoding="utf-8") != render_readiness(payload):
        issues.append("generated/mechanics/memo_mechanic_readiness.min.json must use compact deterministic rendering")

    if issues:
        print("Memo mechanic readiness validation failed.", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("[ok] memo mechanic readiness is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
