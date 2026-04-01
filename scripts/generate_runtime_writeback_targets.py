#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "examples" / "checkpoint_to_memory_contract.example.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "runtime_writeback_targets.min.json"


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


def build_runtime_writeback_targets_payload() -> dict[str, object]:
    payload = read_json(CONTRACT_PATH)
    if not isinstance(payload, dict):
        raise SystemExit("[error] examples/checkpoint_to_memory_contract.example.json must contain an object")

    mapping_rules = payload.get("mapping_rules")
    if not isinstance(mapping_rules, list):
        raise SystemExit("[error] checkpoint_to_memory_contract.example.json must contain mapping_rules")

    targets: list[dict[str, object]] = []
    for item in mapping_rules:
        if not isinstance(item, dict):
            raise SystemExit("[error] checkpoint_to_memory_contract.example.json mapping_rules entries must be objects")
        targets.append(
            {
                "runtime_surface": item.get("runtime_surface"),
                "target_kind": item.get("target_kind"),
                "writeback_class": item.get("writeback_class"),
                "requires_human_review": item.get("requires_human_review"),
                "review_state_default": item.get("review_state_default"),
                "runtime_refs": item.get("runtime_refs"),
                "notes": item.get("notes"),
            }
        )

    return {
        "schema_version": 1,
        "layer": "aoa-memo",
        "contract_id": payload.get("contract_id"),
        "source_of_truth": "examples/checkpoint_to_memory_contract.example.json",
        "runtime_boundary": payload.get("runtime_boundary", {}),
        "targets": targets,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact runtime writeback targets.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_runtime_writeback_targets_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/runtime_writeback_targets.min.json is out of date; "
                "run scripts/generate_runtime_writeback_targets.py"
            )
        print("[ok] generated/runtime_writeback_targets.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/runtime_writeback_targets.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
