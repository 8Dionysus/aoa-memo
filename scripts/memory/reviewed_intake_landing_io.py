from __future__ import annotations

from pathlib import Path

from reviewed_intake_landing_common import (
    ROOT,
    JsonDict,
    LandingError,
    LandingPlan,
    relative_to_output,
    write_json,
)


def write_landing_plan(plan: LandingPlan, *, output_root: Path = ROOT, replace: bool = False) -> None:
    output_root = output_root.resolve()
    targets = [
        output_root / plan.copied_intake_rel_path,
        output_root / plan.object_rel_path,
        output_root / plan.memo_rel_path,
        output_root / plan.receipt_rel_path,
    ]
    existing = [path for path in targets if path.exists()]
    if existing and not replace:
        rendered = ", ".join(relative_to_output(output_root, path) for path in existing)
        raise LandingError(f"landing target already exists: {rendered}")

    for path in targets:
        path.parent.mkdir(parents=True, exist_ok=True)

    write_json(output_root / plan.copied_intake_rel_path, plan.export_payload)
    write_json(output_root / plan.object_rel_path, plan.object_payload)
    (output_root / plan.memo_rel_path).write_text(plan.memo_markdown, encoding="utf-8")
    write_json(output_root / plan.receipt_rel_path, plan.receipt_payload)


def plan_summary(plan: LandingPlan) -> JsonDict:
    return {
        "repo": plan.repo,
        "object_id": plan.object_id,
        "object_kind": plan.object_kind,
        "object_path": plan.object_rel_path,
        "memo_path": plan.memo_rel_path,
        "copied_intake_ref": plan.copied_intake_rel_path,
        "receipt_path": plan.receipt_rel_path,
        "reviewed_at": plan.reviewed_at,
    }
