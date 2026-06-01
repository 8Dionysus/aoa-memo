#!/usr/bin/env python3
"""Land a reviewed local memo export as an aoa-memo corpus object bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

from reviewed_intake_landing_common import (
    KIND_DIRS,
    ROOT,
    LandingError,
    object_schema_errors,
    support_schema_errors,
)
from reviewed_intake_landing_inputs import load_landing_inputs
from reviewed_intake_landing_io import plan_summary, write_landing_plan
from reviewed_intake_landing_plan import build_landing_plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Land a reviewed local memo export into memo/objects.")
    parser.add_argument("--port", required=True, help="Path to the origin repository memo port.")
    parser.add_argument("--export", required=True, help="Export packet path relative to the memo port export dir.")
    parser.add_argument("--output-root", default=str(ROOT), help="Repository root to write into; defaults to aoa-memo.")
    parser.add_argument("--object-kind", choices=sorted(KIND_DIRS), help="Memory object kind to create.")
    parser.add_argument("--slug", help="Object slug; defaults to export id slug.")
    parser.add_argument("--title", help="Object title; defaults to first candidate claim.")
    parser.add_argument("--summary", help="Object summary; defaults to candidate claim summary.")
    parser.add_argument("--object-id", help="Object id; defaults to memo.<kind>.<date>.<slug>.")
    parser.add_argument("--reviewed-at", help="RFC3339 UTC-ish landing time; defaults to now.")
    parser.add_argument("--reviewed-by", default="aoa-memo:reviewed-intake-landing")
    parser.add_argument("--current-recall-status", default="allowed", choices=["preferred", "allowed", "historical", "withdrawn"])
    parser.add_argument("--temperature", default="cool", choices=["warm", "cool", "cold", "frozen"])
    parser.add_argument("--confidence", default=0.85, type=float)
    parser.add_argument("--write", action="store_true", help="Write the planned landing files.")
    parser.add_argument("--replace", action="store_true", help="Replace existing landing files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        inputs = load_landing_inputs(args.port, args.export)
        plan = build_landing_plan(
            inputs,
            output_root=Path(args.output_root),
            object_kind=args.object_kind,
            slug=args.slug,
            title=args.title,
            summary=args.summary,
            object_id=args.object_id,
            reviewed_at=args.reviewed_at,
            reviewed_by=args.reviewed_by,
            current_recall_status=args.current_recall_status,
            temperature=args.temperature,
            confidence=args.confidence,
        )
        if args.write:
            write_landing_plan(plan, output_root=Path(args.output_root), replace=args.replace)
            print(f"[OK]   landed reviewed intake as {plan.object_rel_path}")
        else:
            print(json.dumps(plan_summary(plan), indent=2, ensure_ascii=False))
            print("[OK]   reviewed intake landing plan is valid")
        return 0
    except (LandingError, OSError, json.JSONDecodeError, shutil.Error) as exc:
        print(f"[FAIL] reviewed intake landing: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
