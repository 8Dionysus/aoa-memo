#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FAILURE_EXAMPLE_PATH = REPO_ROOT / "examples" / "failure_lesson_memory.lineage.example.json"
RECOVERY_EXAMPLE_PATH = REPO_ROOT / "examples" / "recovery_pattern_memory.lineage.example.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "growth_refinery_writeback_lanes.min.json"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"[error] missing required file: {path.relative_to(REPO_ROOT).as_posix()}")


def read_json(path: Path) -> object:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[error] invalid JSON in {path.relative_to(REPO_ROOT).as_posix()}: {exc}")


def require_string(payload: dict[str, object], field_name: str, *, context: str) -> str:
    value = payload.get(field_name)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"[error] {context}.{field_name} must be a non-empty string")
    return value


def require_string_list(payload: dict[str, object], field_name: str, *, context: str) -> list[str]:
    value = payload.get(field_name)
    if not isinstance(value, list) or not value:
        raise SystemExit(f"[error] {context}.{field_name} must be a non-empty list")
    normalized = [item for item in value if isinstance(item, str) and item]
    if len(normalized) != len(value):
        raise SystemExit(f"[error] {context}.{field_name} must contain only non-empty strings")
    return normalized


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def build_failure_lesson_lane() -> dict[str, object]:
    payload = read_json(FAILURE_EXAMPLE_PATH)
    if not isinstance(payload, dict):
        raise SystemExit("[error] examples/failure_lesson_memory.lineage.example.json must contain an object")
    context = "examples/failure_lesson_memory.lineage.example.json"
    if require_string(payload, "schema_version", context=context) != "failure_lesson_memory_v1":
        raise SystemExit("[error] failure lesson lineage example must keep schema_version failure_lesson_memory_v1")
    if require_string(payload, "object_kind", context=context) != "failure_lesson":
        raise SystemExit("[error] failure lesson lineage example must keep object_kind failure_lesson")

    required_evidence_refs = dedupe(
        require_string_list(payload, "source_receipt_refs", context=context)
        + require_string_list(payload, "adaptation_delta_refs", context=context)
        + require_string_list(payload, "evidence_refs", context=context)
    )

    return {
        "lane_ref": "growth_refinery_failure_lesson",
        "target_kind": "failure_lesson",
        "object_ref_kind": "support_memory",
        "writeback_class": "growth_refinery_memory",
        "review_status": require_string(payload, "review_status", context=context),
        "memory_id": require_string(payload, "memory_id", context=context),
        "source_path": "examples/failure_lesson_memory.lineage.example.json",
        "primary_ref": "repo:aoa-memo/examples/failure_lesson_memory.lineage.example.json",
        "required_evidence_refs": required_evidence_refs,
        "optional_evidence_refs": [],
    }


def build_recovery_pattern_lane() -> dict[str, object]:
    payload = read_json(RECOVERY_EXAMPLE_PATH)
    if not isinstance(payload, dict):
        raise SystemExit("[error] examples/recovery_pattern_memory.lineage.example.json must contain an object")
    context = "examples/recovery_pattern_memory.lineage.example.json"
    if require_string(payload, "schema_version", context=context) != "recovery_pattern_memory_v1":
        raise SystemExit("[error] recovery pattern lineage example must keep schema_version recovery_pattern_memory_v1")
    if require_string(payload, "object_kind", context=context) != "recovery_pattern":
        raise SystemExit("[error] recovery pattern lineage example must keep object_kind recovery_pattern")

    optional_evidence_refs: list[str] = []
    route_hint_refs = payload.get("route_hint_refs")
    if isinstance(route_hint_refs, list):
        optional_evidence_refs.extend(item for item in route_hint_refs if isinstance(item, str) and item)
    native_pattern_ref = payload.get("native_pattern_ref")
    if isinstance(native_pattern_ref, str) and native_pattern_ref:
        optional_evidence_refs.append(native_pattern_ref)

    required_evidence_refs = dedupe(
        require_string_list(payload, "source_receipt_refs", context=context)
        + require_string_list(payload, "eval_report_refs", context=context)
        + require_string_list(payload, "stats_summary_refs", context=context)
    )

    return {
        "lane_ref": "growth_refinery_recovery_pattern",
        "target_kind": "recovery_pattern",
        "object_ref_kind": "support_memory",
        "writeback_class": "growth_refinery_memory",
        "review_status": require_string(payload, "review_status", context=context),
        "memory_id": require_string(payload, "memory_id", context=context),
        "source_path": "examples/recovery_pattern_memory.lineage.example.json",
        "primary_ref": "repo:aoa-memo/examples/recovery_pattern_memory.lineage.example.json",
        "required_evidence_refs": required_evidence_refs,
        "optional_evidence_refs": dedupe(optional_evidence_refs),
    }


def build_growth_refinery_writeback_lanes_payload() -> dict[str, object]:
    lanes = [build_failure_lesson_lane(), build_recovery_pattern_lane()]
    lanes.sort(key=lambda item: str(item["lane_ref"]))
    return {
        "schema_version": 1,
        "layer": "aoa-memo",
        "scope": "growth-refinery-writeback",
        "source_of_truth": {
            "growth_refinery_writeback": "docs/GROWTH_REFINERY_WRITEBACK.md",
            "failure_lesson_example": "examples/failure_lesson_memory.lineage.example.json",
            "recovery_pattern_example": "examples/recovery_pattern_memory.lineage.example.json",
        },
        "lanes": lanes,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate compact growth-refinery writeback lanes from reviewed support-memory examples."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_growth_refinery_writeback_lanes_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/growth_refinery_writeback_lanes.min.json is out of date; "
                "run scripts/generate_growth_refinery_writeback_lanes.py"
            )
        print("[ok] generated/growth_refinery_writeback_lanes.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/growth_refinery_writeback_lanes.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
