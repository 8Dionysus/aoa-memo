#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from memo_mechanics_common import GENERATED_PATH, INDEX_SCHEMA_VERSION, build_index


def main() -> int:
    if not GENERATED_PATH.is_file():
        print("[error] generated/mechanics/memo_mechanics.min.json is missing", file=sys.stderr)
        return 1

    generated = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    expected = build_index()
    if generated != expected:
        print("[error] generated memo mechanics index is stale", file=sys.stderr)
        return 1

    if generated.get("schema_version") != INDEX_SCHEMA_VERSION:
        print("[error] generated memo mechanics index has wrong schema_version", file=sys.stderr)
        return 1

    print("[ok] generated memo mechanics index is valid and current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
