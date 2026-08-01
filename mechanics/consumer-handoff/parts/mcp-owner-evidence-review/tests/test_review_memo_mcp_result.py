from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from review_capture_test_support import attested_capture  # noqa: E402


SCRIPT = (
    REPO_ROOT
    / "mechanics"
    / "consumer-handoff"
    / "parts"
    / "mcp-owner-evidence-review"
    / "scripts"
    / "review_memo_mcp_result.py"
)
SPEC = importlib.util.spec_from_file_location("review_memo_mcp_result", SCRIPT)
assert SPEC and SPEC.loader
reviewer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reviewer
SPEC.loader.exec_module(reviewer)


def _source_revision() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _brief_payload() -> dict[str, object]:
    catalog = json.loads(
        (REPO_ROOT / reviewer.CATALOG_REF).read_text(encoding="utf-8")
    )
    row = next(
        item
        for item in catalog["memory_objects"]
        if item.get("source_kind") == "reviewed_corpus"
        and item.get("current_recall_status") in {"allowed", "preferred"}
    )
    returned = {field: row[field] for field in reviewer.ROW_FIELDS}
    return {
        "schema": reviewer.RESULT_SCHEMA,
        "repo": "aoa-memo",
        "operation_mode": "read_write_under_review",
        "owner_note": "reviewed memory authority",
        "local_port": {
            "repo": "aoa-memo",
            "memory_role": "reviewed-memory-owner",
            "memory_route_status": "root_memory_route",
            "recommended_port_level": "route_only",
            "ready": False,
        },
        "memory_route": {
            "brief": "aoa_memo_brief",
            "durable_landing": "reviewed source patch, not MCP direct write",
        },
        "central_memory_contracts": [
            {
                "path": "docs/memory/MEMORY_OPERATION_CYCLE.md",
                "abs_path": str(REPO_ROOT / "docs/memory/MEMORY_OPERATION_CYCLE.md"),
                "exists": True,
            }
        ],
        "reviewed_memory": [returned],
    }


def test_ground_payload_binds_exact_reviewed_catalog() -> None:
    watermark, refs = reviewer._ground_payload(
        _brief_payload(), runtime_root=REPO_ROOT, source_revision=_source_revision()
    )

    assert watermark.startswith("aoa-memo-catalog:sha256:")
    assert reviewer.CATALOG_REF in refs
    assert any(ref.startswith("memo/objects/") for ref in refs)


def test_ground_payload_rejects_catalog_row_tamper() -> None:
    payload = _brief_payload()
    payload["reviewed_memory"][0]["summary"] = "fluent but ungrounded"

    with pytest.raises(reviewer.MemoOwnerReviewError, match="differs from current catalog"):
        reviewer._ground_payload(
            payload, runtime_root=REPO_ROOT, source_revision=_source_revision()
        )


def test_ground_payload_preserves_route_only_owner_root() -> None:
    payload = _brief_payload()
    payload["local_port"]["ready"] = True

    with pytest.raises(reviewer.MemoOwnerReviewError, match="local-port boundary"):
        reviewer._ground_payload(
            payload, runtime_root=REPO_ROOT, source_revision=_source_revision()
        )


def test_capture_requires_two_valid_stack_attestations(tmp_path: Path) -> None:
    receipt_path, artifact_path, public_key, signer_id = attested_capture(
        tmp_path, reviewer, _brief_payload()
    )
    receipt, _, _ = reviewer._read_private_json(receipt_path, "receipt")
    artifact, _, _ = reviewer._read_private_json(artifact_path, "artifact")

    payload, _, _, receipt_ref, artifact_ref = reviewer._validate_capture(
        receipt,
        artifact,
        capture_root=tmp_path / "capture",
        receipt_path=receipt_path,
        artifact_path=artifact_path,
        signer_id=signer_id,
        public_key=public_key,
    )

    assert payload["schema"] == reviewer.RESULT_SCHEMA
    assert receipt_ref.startswith("records/aoa-memo/")
    assert artifact_ref.startswith("results/aoa-memo/")


def test_capture_rejects_signed_statement_tamper(tmp_path: Path) -> None:
    receipt_path, artifact_path, public_key, signer_id = attested_capture(
        tmp_path, reviewer, _brief_payload()
    )
    receipt, _, _ = reviewer._read_private_json(receipt_path, "receipt")
    artifact, _, _ = reviewer._read_private_json(artifact_path, "artifact")
    artifact["owner_payload"]["repo"] = "not-aoa-memo"

    with pytest.raises(reviewer.MemoOwnerReviewError, match="content address"):
        reviewer._validate_capture(
            receipt,
            artifact,
            capture_root=tmp_path / "capture",
            receipt_path=receipt_path,
            artifact_path=artifact_path,
            signer_id=signer_id,
            public_key=public_key,
        )


def test_complete_review_satisfies_pinned_sdk_abi(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    receipt_path, artifact_path, public_key, signer_id = attested_capture(
        tmp_path, reviewer, _brief_payload()
    )
    sdk_route = {
        "env": "AOA_SDK_ROOT",
        "pinned_ref": "cbf225627f9f28d0470deb8a962ae12d1fe72375",
        "path": "schemas/organ-access/organ-owner-result-review.schema.json",
    }
    monkeypatch.setenv("AOA_SDK_ROOT", "/srv/AbyssOS/aoa-sdk")
    monkeypatch.setattr(
        reviewer,
        "_load_trust",
        lambda _revision: (signer_id, public_key, sdk_route),
    )
    monkeypatch.setattr(
        reviewer,
        "_require_runtime_owner",
        lambda _root, _revision: REPO_ROOT,
    )
    owner_schema_path = REPO_ROOT / reviewer.OWNER_SCHEMA_REF
    owner_schema_raw = owner_schema_path.read_bytes()
    owner_schema = json.loads(owner_schema_raw)
    monkeypatch.setattr(
        reviewer,
        "_owner_schema",
        lambda _revision: (owner_schema, reviewer._raw_digest(owner_schema_raw)),
    )

    review = reviewer.review_memo_capture(
        capture_root=tmp_path / "capture",
        receipt_path=receipt_path,
        artifact_path=artifact_path,
        source_revision=_source_revision(),
        runtime_owner_root=REPO_ROOT,
    )

    assert review["grounding_state"] == "grounded"
    assert review["freshness_state"] == "exact"
    assert review["owner_accepted"] is False
    assert review["central_proof_asserted"] is False
    assert review["admission_asserted"] is False
    assert review["source_revision"]["digest"] != review["source_revision"]["schema_digest"]
