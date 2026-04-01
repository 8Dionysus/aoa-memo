#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TARGETS_PATH = REPO_ROOT / "generated" / "runtime_writeback_targets.min.json"
CONTRACT_PATH = REPO_ROOT / "examples" / "checkpoint_to_memory_contract.example.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "runtime_writeback_intake.min.json"


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


def build_runtime_writeback_intake_payload() -> dict[str, object]:
    targets_payload = read_json(TARGETS_PATH)
    contract_payload = read_json(CONTRACT_PATH)
    if not isinstance(targets_payload, dict):
        raise SystemExit("[error] generated/runtime_writeback_targets.min.json must contain an object")
    if not isinstance(contract_payload, dict):
        raise SystemExit("[error] examples/checkpoint_to_memory_contract.example.json must contain an object")

    targets = targets_payload.get("targets")
    if not isinstance(targets, list):
        raise SystemExit("[error] generated/runtime_writeback_targets.min.json must contain targets")

    contract_rules = contract_payload.get("mapping_rules")
    if not isinstance(contract_rules, list):
        raise SystemExit("[error] examples/checkpoint_to_memory_contract.example.json must contain mapping_rules")

    rules_by_surface = {
        rule.get("runtime_surface"): rule
        for rule in contract_rules
        if isinstance(rule, dict) and isinstance(rule.get("runtime_surface"), str)
    }

    intake_targets: list[dict[str, object]] = []
    for item in targets:
        if not isinstance(item, dict):
            raise SystemExit("[error] generated/runtime_writeback_targets.min.json target entries must be objects")
        runtime_surface = item.get("runtime_surface")
        if not isinstance(runtime_surface, str):
            raise SystemExit("[error] generated/runtime_writeback_targets.min.json target entries must include runtime_surface")

        contract_rule = rules_by_surface.get(runtime_surface)
        if contract_rule is None:
            raise SystemExit(
                f"[error] generated/runtime_writeback_targets.min.json references unknown runtime_surface {runtime_surface!r}"
            )

        owner_review_refs = [
            ref
            for ref in item.get("runtime_refs", [])
            if isinstance(ref, str) and ref and not ref.startswith("repo:")
        ]
        owner_review_refs.extend(
            [
                "docs/RUNTIME_WRITEBACK_SEAM.md",
                "docs/QUEST_EVIDENCE_WRITEBACK.md",
            ]
        )
        deduped_owner_review_refs: list[str] = []
        for ref in owner_review_refs:
            if ref not in deduped_owner_review_refs:
                deduped_owner_review_refs.append(ref)

        requires_human_review = item.get("requires_human_review") is True
        writeback_class = item.get("writeback_class")
        if writeback_class == "reviewed_candidate":
            intake_posture = "review_candidate_only"
        elif requires_human_review:
            intake_posture = "review_before_writeback"
        else:
            intake_posture = "capturable_runtime_export"

        intake_targets.append(
            {
                "runtime_surface": runtime_surface,
                "target_kind": item.get("target_kind"),
                "writeback_class": writeback_class,
                "requires_human_review": item.get("requires_human_review"),
                "review_state_default": item.get("review_state_default"),
                "runtime_refs": contract_rule.get("runtime_refs"),
                "owner_review_refs": deduped_owner_review_refs,
                "intake_posture": intake_posture,
            }
        )

    intake_targets.sort(key=lambda item: str(item["runtime_surface"]))

    return {
        "schema_version": 1,
        "layer": "aoa-memo",
        "source_of_truth": {
            "runtime_writeback_targets": "generated/runtime_writeback_targets.min.json",
            "checkpoint_to_memory_contract": "examples/checkpoint_to_memory_contract.example.json",
            "runtime_writeback_seam": "docs/RUNTIME_WRITEBACK_SEAM.md",
            "quest_evidence_writeback": "docs/QUEST_EVIDENCE_WRITEBACK.md",
        },
        "targets": intake_targets,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact runtime writeback intake targets.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_runtime_writeback_intake_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/runtime_writeback_intake.min.json is out of date; "
                "run scripts/generate_runtime_writeback_intake.py"
            )
        print("[ok] generated/runtime_writeback_intake.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/runtime_writeback_intake.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
