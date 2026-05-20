#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "config" / "memory-ports" / "indexing_vocabulary.json"
OUTPUT = ROOT / "generated" / "memory" / "memo_port_vocabulary.min.json"


def render() -> str:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    output = {
        "schema": "aoa_memo_port_vocabulary_min_v1",
        "source_ref": "config/memory-ports/indexing_vocabulary.json",
        "terms": payload["terms"],
        "extension_law": payload["extension_law"],
    }
    return json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build compact memo port vocabulary.")
    parser.add_argument("--check", action="store_true", help="Check generated output without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = render()
    if args.check:
        if not OUTPUT.exists():
            print(f"{OUTPUT} is missing", file=sys.stderr)
            return 1
        if OUTPUT.read_text(encoding="utf-8") != text:
            print(f"{OUTPUT} is not up to date", file=sys.stderr)
            return 1
        print("[ok] memo port vocabulary is up to date")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"[ok] wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

