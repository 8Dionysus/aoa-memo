#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = REPO_ROOT / "examples" / "phase_alpha_writeback_map.example.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "phase_alpha_writeback_map.min.json"


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


def build_phase_alpha_writeback_map_payload() -> dict[str, object]:
    payload = read_json(SOURCE_PATH)
    if not isinstance(payload, dict):
        raise SystemExit("[error] examples/phase_alpha_writeback_map.example.json must contain an object")
    playbooks = payload.get("playbooks")
    if not isinstance(playbooks, list):
        raise SystemExit("[error] examples/phase_alpha_writeback_map.example.json must contain playbooks")

    entries: list[dict[str, object]] = []
    for item in playbooks:
        if not isinstance(item, dict):
            continue
        entries.append(
            {
                "playbook_id": item.get("playbook_id"),
                "playbook_name": item.get("playbook_name"),
                "writeback_kinds": item.get("writeback_kinds"),
                "route_artifacts_retained": item.get("route_artifacts_retained"),
                "pattern_after_second_recurrence": item.get("pattern_after_second_recurrence"),
                "claim_candidate_after_reviewer": item.get("claim_candidate_after_reviewer"),
                "source_refs": item.get("source_refs"),
            }
        )

    return {
        "schema_version": 1,
        "layer": "aoa-memo",
        "phase": "alpha",
        "source_of_truth": {
            "phase_alpha_writeback_map": "examples/phase_alpha_writeback_map.example.json",
            "phase_alpha_recall_contract": "examples/recall_contract.object.working.phase-alpha.json",
        },
        "runtime_boundary": payload.get("runtime_boundary"),
        "playbooks": entries,
        "recall_posture": payload.get("recall_posture"),
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact Phase Alpha writeback map.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_phase_alpha_writeback_map_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/phase_alpha_writeback_map.min.json is out of date; "
                "run scripts/generate_phase_alpha_writeback_map.py"
            )
        print("[ok] generated/phase_alpha_writeback_map.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/phase_alpha_writeback_map.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
