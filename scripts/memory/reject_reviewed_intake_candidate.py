#!/usr/bin/env python3
"""Issue an aoa-memo rejection without creating durable memory."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

from reviewed_intake_landing_common import (
    LandingError,
    local_port_schema_errors,
    rfc3339_now,
    slugify,
    stamp_from_rfc3339,
    support_schema_errors,
)


JsonDict = dict[str, Any]


def load_object(path: Path, label: str) -> JsonDict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise LandingError(f"{label} must be a JSON object")
    return value


def write_private_json(path: Path, payload: JsonDict) -> None:
    destination = path.expanduser().absolute()
    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    destination.parent.chmod(0o700)
    if destination.is_symlink():
        raise LandingError(f"{destination}: output cannot be a symlink")
    rendered = (
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def _candidate_slug(candidate: JsonDict) -> str:
    candidate_id = str(candidate.get("id") or "")
    raw = candidate_id.rsplit(":", 1)[-1]
    return slugify(raw)


def _repo_slug(repo: str) -> str:
    return slugify(repo)


def build_rejection(
    *,
    candidate: JsonDict,
    candidate_ref: str,
    evaluation: JsonDict,
    evaluation_ref: str,
    local_receipt_ref: str,
    reason_codes: list[str],
    reviewed_at: str,
    reviewed_by: str,
    required_evaluation_verdict: str | None = None,
) -> tuple[JsonDict, JsonDict]:
    candidate_errors = local_port_schema_errors(
        "local_memo_candidate.schema.json",
        candidate,
        Path(candidate_ref),
    )
    if candidate_errors:
        rendered = "\n".join(f"- {error}" for error in candidate_errors)
        raise LandingError(f"candidate validation failed:\n{rendered}")

    guardrails = candidate.get("guardrails")
    if not isinstance(guardrails, dict):
        raise LandingError("candidate guardrails are required")
    if guardrails.get("direct_durable_write") is not False:
        raise LandingError("candidate must forbid direct durable writes")
    if guardrails.get("instructions_treated_as_data") is not True:
        raise LandingError("candidate must treat instructions as data")
    if guardrails.get("requires_reviewed_intake") is not True:
        raise LandingError("candidate must require reviewed intake")

    for field in (
        "eval_name",
        "verdict",
        "claim_scope",
        "report_ref",
        "interpretation_bound",
    ):
        if not isinstance(evaluation.get(field), str) or not evaluation[field]:
            raise LandingError(f"evaluation field {field!r} is required")
    if (
        required_evaluation_verdict is not None
        and evaluation["verdict"] != required_evaluation_verdict
    ):
        raise LandingError("evaluation verdict does not match the required verdict")
    if not reason_codes:
        raise LandingError("at least one rejection reason code is required")
    if any(not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", item) for item in reason_codes):
        raise LandingError("reason codes must use lowercase identifier characters")

    repo = str(candidate["repo"])
    stamp = stamp_from_rfc3339(reviewed_at)
    slug = _candidate_slug(candidate)
    checks = [
        "candidate_schema",
        "candidate_direct_durable_write_false",
        "candidate_instructions_treated_as_data",
        "candidate_requires_reviewed_intake",
        "evaluation_receipt_present",
        "evaluation_interpretation_bound_present",
        "explicit_owner_rejection",
        "durable_object_not_created",
    ]
    local_receipt = {
        "schema": "aoa_local_memo_receipt_v2",
        "id": f"receipt:{repo}:{stamp}:{slug}-rejected",
        "repo": repo,
        "candidate_ref": candidate_ref,
        "result": "rejected",
        "route": "reviewed_intake",
        "checks": checks,
        "errors": reason_codes,
        "created_at": reviewed_at,
        "checked_by": reviewed_by,
        "notes": (
            f"Rejected after {evaluation['eval_name']} reported "
            f"{evaluation['verdict']!r}. No durable memory object was created."
        ),
    }
    local_errors = local_port_schema_errors(
        "local_memo_receipt.schema.json",
        local_receipt,
        Path(local_receipt_ref),
    )
    if local_errors:
        rendered = "\n".join(f"- {error}" for error in local_errors)
        raise LandingError(f"local rejection receipt validation failed:\n{rendered}")

    landing_receipt = {
        "schema": "aoa_memo_reviewed_intake_landing_receipt_v1",
        "id": (
            f"landing-receipt:{repo}:{stamp}:"
            f"{_repo_slug(repo)}-{slug}-rejected"
        ),
        "repo": repo,
        "source_export_ref": candidate_ref,
        "copied_intake_ref": "not-created://reviewed-intake/rejected",
        "candidate_refs": [candidate_ref],
        "receipt_refs": [local_receipt_ref, evaluation_ref],
        "object_ref": f"not-created://memory-object/rejected/{slug}",
        "object_path": "not-created://memory-object/rejected",
        "result": "rejected",
        "checks": checks,
        "errors": reason_codes,
        "landed_at": reviewed_at,
        "landed_by": reviewed_by,
        "notes": (
            "Explicit aoa-memo owner rejection. The candidate, eval result, "
            "and rejection receipts remain evidence; no intake copy or "
            "durable memory object was created."
        ),
    }
    landing_errors = support_schema_errors(
        landing_receipt,
        "reviewed_intake_landing_receipt.schema.json",
    )
    if landing_errors:
        rendered = "\n".join(f"- {error}" for error in landing_errors)
        raise LandingError(f"landing rejection receipt validation failed:\n{rendered}")
    return local_receipt, landing_receipt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--candidate-ref", required=True)
    parser.add_argument("--evaluation", type=Path, required=True)
    parser.add_argument("--evaluation-ref", required=True)
    parser.add_argument("--local-receipt-output", type=Path, required=True)
    parser.add_argument("--local-receipt-ref", required=True)
    parser.add_argument("--landing-receipt-output", type=Path, required=True)
    parser.add_argument("--reason-code", action="append", required=True)
    parser.add_argument("--reviewed-at")
    parser.add_argument(
        "--reviewed-by",
        default="aoa-memo:reviewed-intake-rejection",
    )
    parser.add_argument("--required-evaluation-verdict")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        candidate = load_object(args.candidate, "candidate")
        evaluation = load_object(args.evaluation, "evaluation")
        reviewed_at = args.reviewed_at or rfc3339_now()
        local_receipt, landing_receipt = build_rejection(
            candidate=candidate,
            candidate_ref=args.candidate_ref,
            evaluation=evaluation,
            evaluation_ref=args.evaluation_ref,
            local_receipt_ref=args.local_receipt_ref,
            reason_codes=args.reason_code,
            reviewed_at=reviewed_at,
            reviewed_by=args.reviewed_by,
            required_evaluation_verdict=args.required_evaluation_verdict,
        )
        write_private_json(args.local_receipt_output, local_receipt)
        write_private_json(args.landing_receipt_output, landing_receipt)
        print(
            json.dumps(
                {
                    "candidate_ref": args.candidate_ref,
                    "decision": "rejected",
                    "durable_object_created": False,
                    "landing_receipt": str(
                        args.landing_receipt_output.expanduser().absolute()
                    ),
                    "local_receipt": str(
                        args.local_receipt_output.expanduser().absolute()
                    ),
                    "reason_codes": args.reason_code,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (LandingError, OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] reviewed intake rejection: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
