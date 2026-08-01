from __future__ import annotations

import base64
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def _urlsafe(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _sign(payload: dict[str, object], private_key: Path, root: Path, reviewer: Any) -> str:
    statement = root / "statement.json"
    signature = root / "signature.bin"
    statement.write_bytes(reviewer._canonical_json_bytes(payload))
    subprocess.run(
        [
            "openssl",
            "pkeyutl",
            "-sign",
            "-inkey",
            str(private_key),
            "-rawin",
            "-in",
            str(statement),
            "-out",
            str(signature),
        ],
        check=True,
        capture_output=True,
    )
    return _urlsafe(signature.read_bytes())


def attested_capture(
    tmp_path: Path, reviewer: Any, owner_payload: dict[str, object]
) -> tuple[Path, Path, bytes, str]:
    capture_root = tmp_path / "capture"
    record_dir = capture_root / "records" / "aoa-memo"
    result_dir = capture_root / "results" / "aoa-memo"
    record_dir.mkdir(parents=True, mode=0o700)
    result_dir.mkdir(parents=True, mode=0o700)
    for path in (capture_root, capture_root / "records", capture_root / "results"):
        os.chmod(path, 0o700)

    private_key = tmp_path / "capture-key.pem"
    public_der = tmp_path / "capture-public.der"
    subprocess.run(
        ["openssl", "genpkey", "-algorithm", "ED25519", "-out", str(private_key)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "openssl",
            "pkey",
            "-in",
            str(private_key),
            "-pubout",
            "-outform",
            "DER",
            "-out",
            str(public_der),
        ],
        check=True,
        capture_output=True,
    )
    public_key = public_der.read_bytes()[-32:]
    signer_id = reviewer._raw_digest(public_key)
    observed = datetime.now(timezone.utc)
    expires = observed + timedelta(minutes=10)
    result_digest = reviewer._digest(owner_payload)
    artifact_body = {
        "schema_version": reviewer.RESULT_ARTIFACT_SCHEMA,
        "attestation_algorithm": "ed25519",
        "canary_route": "runbook://mcp-canary/aoa-memo/read",
        "claim_limit": "capture only",
        "contains_secrets": False,
        "content_trust": "untrusted_data",
        "instruction_authority": "none",
        "issuer": "abyss-stack",
        "observed_at": observed.isoformat(),
        "organ_id": "aoa-memo",
        "owner_payload": owner_payload,
        "policy_family": "read",
        "result_digest": result_digest,
        "result_schema_identity": reviewer.RESULT_SCHEMA,
        "service_id": "aoa-memo-mcp",
        "signer_id": signer_id,
        "tool_arguments_digest": "sha256:" + "1" * 64,
        "tool_name": "aoa_memo_brief",
    }
    artifact = {**artifact_body, "artifact_id": reviewer._digest(artifact_body)}
    artifact["attestation"] = _sign(artifact, private_key, tmp_path, reviewer)
    artifact_path = result_dir / (result_digest.removeprefix("sha256:") + ".json")
    artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
    os.chmod(artifact_path, 0o600)

    receipt_body = {
        "schema_version": reviewer.CAPTURE_RECEIPT_SCHEMA,
        "attestation_algorithm": "ed25519",
        "call_succeeded": True,
        "canary_route": "runbook://mcp-canary/aoa-memo/read",
        "claim_limit": "capture only",
        "consumer_id": "abyss-stack-mcp-canary",
        "contains_secrets": False,
        "content_trust": "untrusted_data",
        "expires_at": expires.isoformat(),
        "instruction_authority": "none",
        "issuer": "abyss-stack",
        "observed_at": observed.isoformat(),
        "organ_id": "aoa-memo",
        "policy_family": "read",
        "reason_codes": [],
        "result_artifact_ref": artifact_path.relative_to(capture_root).as_posix(),
        "result_contract_matched": True,
        "result_digest": result_digest,
        "result_schema_identity": reviewer.RESULT_SCHEMA,
        "selected_tool_schema_digest": "sha256:" + "2" * 64,
        "server_schema_digest": "sha256:" + "3" * 64,
        "service_id": "aoa-memo-mcp",
        "signer_id": signer_id,
        "tool_arguments_digest": "sha256:" + "1" * 64,
        "tool_name": "aoa_memo_brief",
    }
    receipt = {**receipt_body, "receipt_id": reviewer._digest(receipt_body)}
    receipt["attestation"] = _sign(receipt, private_key, tmp_path, reviewer)
    receipt_path = record_dir / (receipt["receipt_id"].removeprefix("sha256:") + ".json")
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    os.chmod(receipt_path, 0o600)
    return receipt_path, artifact_path, public_key, signer_id
