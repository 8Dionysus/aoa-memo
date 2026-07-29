from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = REPO_ROOT / "scripts" / "memory"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


rejection = load_script(
    "reject_reviewed_intake_candidate",
    REPO_ROOT / "scripts" / "memory" / "reject_reviewed_intake_candidate.py",
)
landing = load_script(
    "land_reviewed_memo_intake",
    REPO_ROOT / "scripts" / "memory" / "land_reviewed_memo_intake.py",
)

EXAMPLE_CANDIDATE = (
    REPO_ROOT
    / "examples"
    / "memory-ports"
    / "example-port"
    / "candidates"
    / "20260520T171200Z.codex-plane-memory-route.candidate.json"
)


def candidate_payload() -> dict:
    candidate = json.loads(EXAMPLE_CANDIDATE.read_text(encoding="utf-8"))
    candidate["guardrails"]["requires_reviewed_intake"] = True
    return candidate


def evaluation_payload() -> dict:
    return {
        "eval_name": "aoa-organ-access-admission-integrity",
        "verdict": "supported_bounded; packet_result=insufficient_evidence",
        "claim_scope": "bundle_scoped",
        "report_ref": "private://task/eval/report.json",
        "interpretation_bound": (
            "The evaluation supports only the bounded packet contract and "
            "does not establish owner acceptance."
        ),
    }


def test_candidate_can_be_explicitly_rejected_without_creating_memory(
    tmp_path: Path,
) -> None:
    local_receipt, landing_receipt = rejection.build_rejection(
        candidate=candidate_payload(),
        candidate_ref="private://task/memo-candidate.json",
        evaluation=evaluation_payload(),
        evaluation_ref="private://task/eval/eval-result-receipt.json",
        local_receipt_ref="private://task/memo/rejection-receipt.json",
        reason_codes=["insufficient_evidence_for_durable_memory"],
        reviewed_at="2026-07-29T03:00:00Z",
        reviewed_by="test-suite",
        required_evaluation_verdict=(
            "supported_bounded; packet_result=insufficient_evidence"
        ),
    )

    local_path = tmp_path / "receipts" / "rejection-receipt.json"
    landing_path = tmp_path / "receipts" / "landing-rejection.json"
    rejection.write_private_json(local_path, local_receipt)
    rejection.write_private_json(landing_path, landing_receipt)

    assert local_receipt["result"] == "rejected"
    assert landing_receipt["result"] == "rejected"
    assert landing_receipt["object_ref"].startswith("not-created://")
    assert landing_receipt["object_path"].startswith("not-created://")
    assert not (tmp_path / "memo" / "objects").exists()
    assert local_path.stat().st_mode & 0o777 == 0o600
    assert landing_path.stat().st_mode & 0o777 == 0o600
    assert (
        landing.support_schema_errors(
            landing_receipt,
            "reviewed_intake_landing_receipt.schema.json",
        )
        == []
    )


def test_rejection_requires_candidate_to_forbid_direct_durable_write() -> None:
    candidate = candidate_payload()
    candidate["guardrails"]["direct_durable_write"] = True

    try:
        rejection.build_rejection(
            candidate=candidate,
            candidate_ref="private://task/memo-candidate.json",
            evaluation=evaluation_payload(),
            evaluation_ref="private://task/eval/eval-result-receipt.json",
            local_receipt_ref="private://task/memo/rejection-receipt.json",
            reason_codes=["insufficient_evidence_for_durable_memory"],
            reviewed_at="2026-07-29T03:00:00Z",
            reviewed_by="test-suite",
        )
    except rejection.LandingError as exc:
        assert "forbid direct durable writes" in str(exc)
    else:
        raise AssertionError("direct-durable-write candidate was rejected as safe")
