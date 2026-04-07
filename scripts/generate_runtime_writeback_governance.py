#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TARGETS_PATH = REPO_ROOT / "generated" / "runtime_writeback_targets.min.json"
INTAKE_PATH = REPO_ROOT / "generated" / "runtime_writeback_intake.min.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "runtime_writeback_governance.min.json"


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


def _load_targets(path: Path) -> dict[str, dict[str, object]]:
    payload = read_json(path)
    if not isinstance(payload, dict) or not isinstance(payload.get("targets"), list):
        raise SystemExit(f"[error] {path.relative_to(REPO_ROOT).as_posix()} must contain targets")
    loaded: dict[str, dict[str, object]] = {}
    for item in payload["targets"]:
        if not isinstance(item, dict):
            continue
        runtime_surface = item.get("runtime_surface")
        if isinstance(runtime_surface, str):
            loaded[runtime_surface] = item
    return loaded


def build_runtime_writeback_governance_payload() -> dict[str, object]:
    targets_by_surface = _load_targets(TARGETS_PATH)
    intake_by_surface = _load_targets(INTAKE_PATH)

    runtime_surfaces = sorted(set(targets_by_surface) | set(intake_by_surface))
    entries: list[dict[str, object]] = []
    for runtime_surface in runtime_surfaces:
        target_entry = targets_by_surface.get(runtime_surface)
        intake_entry = intake_by_surface.get(runtime_surface)

        target_kind = target_entry.get("target_kind") if isinstance(target_entry, dict) else None
        writeback_class = target_entry.get("writeback_class") if isinstance(target_entry, dict) else None
        requires_human_review = (
            target_entry.get("requires_human_review") if isinstance(target_entry, dict) else None
        )
        review_state_default = (
            target_entry.get("review_state_default") if isinstance(target_entry, dict) else None
        )
        intake_posture = intake_entry.get("intake_posture") if isinstance(intake_entry, dict) else None

        blockers: list[str] = []
        if target_entry is None:
            blockers.append("missing_writeback_target")
        if intake_entry is None:
            blockers.append("missing_writeback_intake")
        if isinstance(target_entry, dict) and isinstance(intake_entry, dict):
            for field_name in (
                "target_kind",
                "writeback_class",
                "requires_human_review",
                "review_state_default",
            ):
                if target_entry.get(field_name) != intake_entry.get(field_name):
                    blockers.append(f"intake_mismatch:{field_name}")
            if not isinstance(intake_posture, str) or not intake_posture:
                blockers.append("missing_intake_posture")

        entries.append(
            {
                "runtime_surface": runtime_surface,
                "target_kind": target_kind,
                "writeback_class": writeback_class,
                "requires_human_review": requires_human_review,
                "review_state_default": review_state_default,
                "intake_posture": intake_posture,
                "in_writeback_targets": target_entry is not None,
                "in_writeback_intake": intake_entry is not None,
                "governance_passed": not blockers,
                "blockers": blockers,
            }
        )

    return {
        "schema_version": 1,
        "layer": "aoa-memo",
        "scope": "runtime-writeback",
        "source_of_truth": {
            "runtime_writeback_targets": "generated/runtime_writeback_targets.min.json",
            "runtime_writeback_intake": "generated/runtime_writeback_intake.min.json",
        },
        "targets": entries,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact runtime writeback governance surface.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_runtime_writeback_governance_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/runtime_writeback_governance.min.json is out of date; "
                "run scripts/generate_runtime_writeback_governance.py"
            )
        print("[ok] generated/runtime_writeback_governance.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/runtime_writeback_governance.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
