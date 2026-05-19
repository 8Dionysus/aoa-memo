from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CONFIG = ROOT / "mechanics/agon/parts/bridge-and-evidence-seams/config/agon_vds_memo_bridge.source.json"
OUTPUT = ROOT / "mechanics/agon/parts/bridge-and-evidence-seams/generated/agon_vds_memo_bridge_registry.min.json"


def compact(obj: dict) -> str:
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


def build_registry() -> dict:
    source = json.loads(CONFIG.read_text(encoding="utf-8"))
    return {
        "registry_id": source["registry_id"],
        "version": source["version"],
        "stage": source["stage"],
        "status": source["status"],
        "live_protocol": source["live_protocol"],
        "runtime_effect": source["runtime_effect"],
        "intake_count": len(source["intakes"]),
        "intakes": source["intakes"],
        "stop_lines": source["stop_lines"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = compact(build_registry())

    if args.check:
        if not OUTPUT.exists():
            print(f"missing {OUTPUT}", file=sys.stderr)
            return 1
        if OUTPUT.read_text(encoding="utf-8") != rendered:
            print(
                "generated agon_vds_memo_bridge_registry.min.json is stale",
                file=sys.stderr,
            )
            return 1
        print("agon_vds_memo_bridge_registry.min.json is up to date")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
