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


def require_string(payload: dict[str, object], field_name: str, *, context: str) -> str:
    value = payload.get(field_name)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"[error] {context}.{field_name} must be a non-empty string")
    return value


def require_bool(payload: dict[str, object], field_name: str, *, context: str) -> bool:
    value = payload.get(field_name)
    if not isinstance(value, bool):
        raise SystemExit(f"[error] {context}.{field_name} must be a boolean")
    return value


def require_string_list(payload: dict[str, object], field_name: str, *, context: str) -> list[str]:
    value = payload.get(field_name)
    if not isinstance(value, list) or not value:
        raise SystemExit(f"[error] {context}.{field_name} must be a non-empty list")
    normalized = [item for item in value if isinstance(item, str) and item]
    if len(normalized) != len(value):
        raise SystemExit(f"[error] {context}.{field_name} must contain only non-empty strings")
    return normalized


def require_runtime_boundary(payload: dict[str, object]) -> dict[str, object]:
    runtime_boundary = payload.get("runtime_boundary")
    if not isinstance(runtime_boundary, dict):
        raise SystemExit("[error] checkpoint_to_memory_contract.example.json must contain runtime_boundary")
    return {
        "scratchpad_posture": require_string(
            runtime_boundary,
            "scratchpad_posture",
            context="checkpoint_to_memory_contract.example.json.runtime_boundary",
        ),
        "checkpoint_export_kind": require_string(
            runtime_boundary,
            "checkpoint_export_kind",
            context="checkpoint_to_memory_contract.example.json.runtime_boundary",
        ),
        "distillation_review_posture": require_string(
            runtime_boundary,
            "distillation_review_posture",
            context="checkpoint_to_memory_contract.example.json.runtime_boundary",
        ),
        "review_boundary_refs": require_string_list(
            runtime_boundary,
            "review_boundary_refs",
            context="checkpoint_to_memory_contract.example.json.runtime_boundary",
        ),
    }


def build_runtime_writeback_targets_payload() -> dict[str, object]:
    payload = read_json(CONTRACT_PATH)
    if not isinstance(payload, dict):
        raise SystemExit("[error] examples/checkpoint_to_memory_contract.example.json must contain an object")

    mapping_rules = payload.get("mapping_rules")
    if not isinstance(mapping_rules, list):
        raise SystemExit("[error] checkpoint_to_memory_contract.example.json must contain mapping_rules")

    targets: list[dict[str, object]] = []
    for index, item in enumerate(mapping_rules):
        if not isinstance(item, dict):
            raise SystemExit("[error] checkpoint_to_memory_contract.example.json mapping_rules entries must be objects")
        context = f"checkpoint_to_memory_contract.example.json.mapping_rules[{index}]"
        targets.append(
            {
                "runtime_surface": require_string(item, "runtime_surface", context=context),
                "target_kind": require_string(item, "target_kind", context=context),
                "writeback_class": require_string(item, "writeback_class", context=context),
                "requires_human_review": require_bool(item, "requires_human_review", context=context),
                "review_state_default": require_string(item, "review_state_default", context=context),
                "runtime_refs": require_string_list(item, "runtime_refs", context=context),
                "notes": require_string(item, "notes", context=context),
            }
        )

    return {
        "schema_version": 1,
        "layer": "aoa-memo",
        "contract_id": require_string(
            payload,
            "contract_id",
            context="checkpoint_to_memory_contract.example.json",
        ),
        "source_of_truth": "examples/checkpoint_to_memory_contract.example.json",
        "runtime_boundary": require_runtime_boundary(payload),
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
