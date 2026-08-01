#!/usr/bin/env python3
"""Review one private stack-captured aoa_memo_brief as the memo owner."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import stat
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = Path(__file__).resolve().parents[1]
TRUST_REF = (
    "mechanics/consumer-handoff/parts/mcp-owner-evidence-review/"
    "config/review_trust.json"
)
CATALOG_REF = "generated/memory-objects/memory_object_catalog.min.json"
OWNER_SCHEMA_REF = (
    "mechanics/consumer-handoff/parts/mcp-owner-evidence-review/"
    "schemas/aoa-memo-brief-review.schema.json"
)
CAPTURE_RECEIPT_SCHEMA = "abyss_stack_mcp_canary_receipt_v2"
RESULT_ARTIFACT_SCHEMA = "abyss_stack_mcp_canary_result_artifact_v2"
REVIEW_SCHEMA = "aoa_organ_owner_result_review_v1"
RESULT_SCHEMA = "aoa_memo_brief_v1"
CAPABILITY_ID = "memory-recall"
PRIMITIVE_ID = "brief-memory"
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_REVIEW_TTL_SECONDS = 300
GIT = ("git", "--no-replace-objects")
ROW_FIELDS = (
    "id",
    "kind",
    "title",
    "summary",
    "current_recall_status",
    "source_kind",
    "source_path",
)
CLAIM_LIMIT = (
    "This owner-issued review proves only the named owner's schema grounding "
    "and freshness assessment for one content-addressed captured result. It "
    "does not prove owner acceptance, central proof, admission, cross-organ "
    "benefit, execution authorization, or rollback."
)


class MemoOwnerReviewError(ValueError):
    """The capture cannot support an owner-bounded memo review."""


def _canonical_json_bytes(value: Any, *, ensure_ascii: bool = False) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=ensure_ascii,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any, *, ensure_ascii: bool = False) -> str:
    return "sha256:" + hashlib.sha256(
        _canonical_json_bytes(value, ensure_ascii=ensure_ascii)
    ).hexdigest()


def _raw_digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _aware_time(value: str | datetime, label: str) -> datetime:
    try:
        parsed = (
            value
            if isinstance(value, datetime)
            else datetime.fromisoformat(value.replace("Z", "+00:00"))
        )
    except ValueError as exc:
        raise MemoOwnerReviewError(f"{label} is not a valid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise MemoOwnerReviewError(f"{label} must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _read_private_json(
    path: Path, label: str
) -> tuple[dict[str, Any], bytes, tuple[int, int, int, int, int]]:
    absolute = path.expanduser().absolute()
    for component in (*reversed(absolute.parents), absolute):
        if component.is_symlink():
            raise MemoOwnerReviewError(f"{label} cannot traverse a symlink")
    try:
        descriptor = os.open(absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise MemoOwnerReviewError(f"{label} must be a regular file")
            if stat.S_IMODE(before.st_mode) & 0o077:
                raise MemoOwnerReviewError(f"{label} must not be group/world accessible")
            if not 1 <= before.st_size <= MAX_INPUT_BYTES:
                raise MemoOwnerReviewError(f"{label} has an invalid bounded size")
            chunks: list[bytes] = []
            total = 0
            while total <= MAX_INPUT_BYTES:
                chunk = os.read(descriptor, min(65536, MAX_INPUT_BYTES + 1 - total))
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        raw = b"".join(chunks)
        identity = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        )
        if identity != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ):
            raise MemoOwnerReviewError(f"{label} changed while being read")
        if len(raw) != before.st_size:
            raise MemoOwnerReviewError(f"{label} changed while being read")
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise MemoOwnerReviewError(f"{label} is unavailable or invalid JSON") from exc
    if not isinstance(payload, dict):
        raise MemoOwnerReviewError(f"{label} must be a JSON object")
    return payload, raw, identity


def _require_unchanged(
    path: Path,
    label: str,
    expected_raw: bytes,
    expected_identity: tuple[int, int, int, int, int],
) -> None:
    _, raw, identity = _read_private_json(path, label)
    if raw != expected_raw or identity != expected_identity:
        raise MemoOwnerReviewError(f"{label} changed after verification")


def _git_output(repo: Path, *args: str, text: bool = False) -> bytes | str:
    try:
        return subprocess.run(
            [*GIT, *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=text,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise MemoOwnerReviewError(f"git {' '.join(args)} failed") from exc


def _git_revision(repo: Path) -> str:
    return str(_git_output(repo, "rev-parse", "HEAD", text=True)).strip()


def _read_committed_json(
    repo: Path, revision: str, relative_path: str, label: str
) -> tuple[dict[str, Any], bytes]:
    resolved = str(
        _git_output(repo, "rev-parse", f"{revision}^{{commit}}", text=True)
    ).strip()
    if resolved != revision:
        raise MemoOwnerReviewError(f"{label} revision is not an exact commit")
    raw = _git_output(repo, "show", f"{revision}:{relative_path}")
    assert isinstance(raw, bytes)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise MemoOwnerReviewError(f"{label} is invalid at source revision") from exc
    if not isinstance(payload, dict):
        raise MemoOwnerReviewError(f"{label} must be an object at source revision")
    return payload, raw


def _read_committed_bytes(repo: Path, revision: str, relative_path: str) -> bytes:
    raw = _git_output(repo, "show", f"{revision}:{relative_path}")
    assert isinstance(raw, bytes)
    return raw


def _committed_exists(repo: Path, revision: str, relative_path: str) -> bool:
    try:
        result = subprocess.run(
            [*GIT, "cat-file", "-e", f"{revision}:{relative_path}"],
            cwd=repo,
            check=False,
            capture_output=True,
        )
    except OSError as exc:
        raise MemoOwnerReviewError("git cat-file is unavailable") from exc
    return result.returncode == 0


def _load_trust(source_revision: str) -> tuple[str, bytes, dict[str, str]]:
    trust, _ = _read_committed_json(
        REPO_ROOT, source_revision, TRUST_REF, "memo MCP review trust"
    )
    if trust.get("schema_version") != "aoa_memo_mcp_owner_review_trust_v1":
        raise MemoOwnerReviewError("memo MCP review trust schema is unsupported")
    issuers = trust.get("capture_issuers")
    matches = [
        item
        for item in issuers if isinstance(item, dict)
        and item.get("issuer") == "abyss-stack"
        and item.get("purpose") == "mcp-canary-capture"
        and item.get("state") == "active"
    ] if isinstance(issuers, list) else []
    if len(matches) != 1:
        raise MemoOwnerReviewError("exactly one active stack capture signer is required")
    signer = matches[0]
    encoded = signer.get("public_key_base64url")
    signer_id = signer.get("signer_id")
    if signer.get("attestation_algorithm") != "ed25519" or not isinstance(
        encoded, str
    ) or not isinstance(signer_id, str):
        raise MemoOwnerReviewError("stack capture signer is malformed")
    try:
        public_key = base64.b64decode(
            encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True
        )
    except (ValueError, binascii.Error) as exc:
        raise MemoOwnerReviewError("stack capture public key is malformed") from exc
    if len(public_key) != 32 or signer_id != _raw_digest(public_key):
        raise MemoOwnerReviewError("stack capture signer identity does not match")
    sdk = trust.get("sdk_review_schema")
    if not isinstance(sdk, dict) or not all(
        isinstance(sdk.get(key), str) and sdk[key] for key in ("env", "pinned_ref", "path")
    ):
        raise MemoOwnerReviewError("pinned SDK review schema route is malformed")
    return signer_id, public_key, {key: str(sdk[key]) for key in ("env", "pinned_ref", "path")}


def _verify_attestation(
    payload: dict[str, Any],
    *,
    identity: str,
    label: str,
    signer_id: str,
    public_key: bytes,
) -> None:
    if payload.get("signer_id") != signer_id or payload.get(
        "attestation_algorithm"
    ) != "ed25519":
        raise MemoOwnerReviewError(f"{label} signer is not trusted")
    encoded = payload.get("attestation")
    if not isinstance(encoded, str):
        raise MemoOwnerReviewError(f"{label} attestation is unavailable")
    try:
        signature = base64.b64decode(
            encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True
        )
    except (ValueError, binascii.Error) as exc:
        raise MemoOwnerReviewError(f"{label} attestation is malformed") from exc
    if len(signature) != 64 or identity not in payload:
        raise MemoOwnerReviewError(f"{label} attestation is malformed")
    statement = dict(payload)
    statement.pop("attestation", None)
    public_der = bytes.fromhex("302a300506032b6570032100") + public_key
    with tempfile.TemporaryDirectory(prefix="aoa-memo-capture-verify-") as directory:
        root = Path(directory)
        (root / "public.der").write_bytes(public_der)
        (root / "statement.json").write_bytes(_canonical_json_bytes(statement))
        (root / "signature.bin").write_bytes(signature)
        try:
            result = subprocess.run(
                [
                    "openssl", "pkeyutl", "-verify", "-pubin", "-inkey",
                    str(root / "public.der"), "-keyform", "DER", "-rawin",
                    "-in", str(root / "statement.json"), "-sigfile",
                    str(root / "signature.bin"),
                ],
                check=False,
                capture_output=True,
            )
        except OSError as exc:
            raise MemoOwnerReviewError("openssl verifier is unavailable") from exc
    if result.returncode != 0:
        raise MemoOwnerReviewError(f"{label} attestation does not verify")


def _assert_content_address(payload: dict[str, Any], identity: str, label: str) -> None:
    body = dict(payload)
    claimed = body.pop(identity, None)
    body.pop("attestation", None)
    if claimed != _digest(body):
        raise MemoOwnerReviewError(f"{label} content address does not match")


def _relative_ref(root: Path, path: Path, label: str) -> str:
    try:
        return path.expanduser().resolve(strict=True).relative_to(
            root.expanduser().resolve(strict=True)
        ).as_posix()
    except (OSError, ValueError) as exc:
        raise MemoOwnerReviewError(f"{label} is outside the capture root") from exc


def _validate_capture(
    receipt: dict[str, Any],
    artifact: dict[str, Any],
    *,
    capture_root: Path,
    receipt_path: Path,
    artifact_path: Path,
    signer_id: str,
    public_key: bytes,
) -> tuple[dict[str, Any], datetime, datetime, str, str]:
    expected_receipt = {
        "schema_version": CAPTURE_RECEIPT_SCHEMA,
        "issuer": "abyss-stack",
        "consumer_id": "abyss-stack-mcp-canary",
        "organ_id": "aoa-memo",
        "policy_family": "read",
        "service_id": "aoa-memo-mcp",
        "tool_name": "aoa_memo_brief",
        "call_succeeded": True,
        "result_contract_matched": True,
        "result_schema_identity": RESULT_SCHEMA,
        "contains_secrets": False,
        "content_trust": "untrusted_data",
        "instruction_authority": "none",
    }
    for field, expected in expected_receipt.items():
        if receipt.get(field) != expected:
            raise MemoOwnerReviewError(f"capture receipt {field} does not match")
    if receipt.get("reason_codes") not in ([], ()):
        raise MemoOwnerReviewError("successful capture carries failure reasons")
    _assert_content_address(receipt, "receipt_id", "capture receipt")
    _verify_attestation(
        receipt,
        identity="receipt_id",
        label="capture receipt",
        signer_id=signer_id,
        public_key=public_key,
    )

    expected_artifact = {
        "schema_version": RESULT_ARTIFACT_SCHEMA,
        "issuer": "abyss-stack",
        "organ_id": "aoa-memo",
        "policy_family": "read",
        "service_id": "aoa-memo-mcp",
        "canary_route": receipt.get("canary_route"),
        "tool_name": "aoa_memo_brief",
        "tool_arguments_digest": receipt.get("tool_arguments_digest"),
        "observed_at": receipt.get("observed_at"),
        "result_schema_identity": RESULT_SCHEMA,
        "result_digest": receipt.get("result_digest"),
        "contains_secrets": False,
        "content_trust": "untrusted_data",
        "instruction_authority": "none",
    }
    for field, expected in expected_artifact.items():
        if artifact.get(field) != expected:
            raise MemoOwnerReviewError(f"result artifact {field} does not match")
    _assert_content_address(artifact, "artifact_id", "result artifact")
    _verify_attestation(
        artifact,
        identity="artifact_id",
        label="result artifact",
        signer_id=signer_id,
        public_key=public_key,
    )
    owner_payload = artifact.get("owner_payload")
    if not isinstance(owner_payload, dict) or _digest(owner_payload) != receipt.get(
        "result_digest"
    ):
        raise MemoOwnerReviewError("owner payload digest does not match")

    receipt_ref = _relative_ref(capture_root, receipt_path, "capture receipt")
    artifact_ref = _relative_ref(capture_root, artifact_path, "result artifact")
    if receipt.get("result_artifact_ref") != artifact_ref:
        raise MemoOwnerReviewError("result artifact path does not match receipt")
    if not receipt_ref.startswith("records/aoa-memo/") or not artifact_ref.startswith(
        "results/aoa-memo/"
    ):
        raise MemoOwnerReviewError("capture paths are outside aoa-memo lanes")
    observed_at = _aware_time(str(receipt.get("observed_at") or ""), "observed_at")
    expires_at = _aware_time(str(receipt.get("expires_at") or ""), "expires_at")
    if expires_at <= observed_at:
        raise MemoOwnerReviewError("capture expiry is invalid")
    return owner_payload, observed_at, expires_at, receipt_ref, artifact_ref


def _safe_relative(value: Any, *, prefix: str | None = None) -> str:
    if not isinstance(value, str) or not value or value.startswith("/"):
        raise MemoOwnerReviewError("owner payload contains an unsafe source path")
    path = Path(value)
    if ".." in path.parts or (prefix is not None and not value.startswith(prefix)):
        raise MemoOwnerReviewError("owner payload contains an unsafe source path")
    return path.as_posix()


def _require_runtime_owner(runtime_root: Path, source_revision: str) -> Path:
    root = runtime_root.expanduser().resolve(strict=True)
    if _git_revision(root) != source_revision:
        raise MemoOwnerReviewError("runtime memo checkout revision does not match")
    status = str(
        _git_output(root, "status", "--porcelain", "--untracked-files=no", text=True)
    )
    if status.strip():
        raise MemoOwnerReviewError("runtime memo checkout has tracked source drift")
    return root


def _ground_payload(
    payload: dict[str, Any], *, runtime_root: Path, source_revision: str
) -> tuple[str, list[str]]:
    if payload.get("schema") != RESULT_SCHEMA or payload.get("repo") != "aoa-memo":
        raise MemoOwnerReviewError("memo brief identity does not match")
    if payload.get("operation_mode") != "read_write_under_review":
        raise MemoOwnerReviewError("memo operation mode drifted")
    local_port = payload.get("local_port")
    expected_port = {
        "repo": "aoa-memo",
        "memory_role": "reviewed-memory-owner",
        "memory_route_status": "root_memory_route",
        "recommended_port_level": "route_only",
        "ready": False,
    }
    if not isinstance(local_port, dict) or any(
        local_port.get(key) != value for key, value in expected_port.items()
    ):
        raise MemoOwnerReviewError("memo root local-port boundary drifted")
    memory_route = payload.get("memory_route")
    if not isinstance(memory_route, dict) or memory_route.get("brief") != "aoa_memo_brief":
        raise MemoOwnerReviewError("memo access route drifted")
    if "not MCP direct write" not in str(memory_route.get("durable_landing") or ""):
        raise MemoOwnerReviewError("memo durable-write stop-line is absent")

    catalog, committed_catalog_raw = _read_committed_json(
        REPO_ROOT, source_revision, CATALOG_REF, "memo compact object catalog"
    )
    runtime_catalog_path = runtime_root / CATALOG_REF
    try:
        runtime_catalog_raw = runtime_catalog_path.read_bytes()
    except OSError as exc:
        raise MemoOwnerReviewError("runtime memo catalog is unavailable") from exc
    if runtime_catalog_raw != committed_catalog_raw:
        raise MemoOwnerReviewError("runtime memo catalog differs from committed source")
    identity = catalog.get("artifact_identity")
    if (
        catalog.get("source_of_truth") != "aoa-memo-object-read-models-v2"
        or catalog.get("catalog_kind") != "min"
        or not isinstance(identity, dict)
        or identity.get("owner_repo") != "aoa-memo"
    ):
        raise MemoOwnerReviewError("memo compact catalog identity is malformed")
    rows = catalog.get("memory_objects")
    if not isinstance(rows, list):
        raise MemoOwnerReviewError("memo compact catalog rows are unavailable")
    by_id = {
        item["id"]: item
        for item in rows
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    central = payload.get("central_memory_contracts")
    if not isinstance(central, list) or not central:
        raise MemoOwnerReviewError("memo brief has no central contracts")
    evidence_refs = [CATALOG_REF]
    for item in central:
        if not isinstance(item, dict) or item.get("exists") is not True:
            raise MemoOwnerReviewError("memo brief central contract is unavailable")
        relative = _safe_relative(item.get("path"))
        if item.get("abs_path") != str(runtime_root / relative):
            raise MemoOwnerReviewError("memo brief central contract path drifted")
        if not _committed_exists(REPO_ROOT, source_revision, relative):
            raise MemoOwnerReviewError("memo brief central contract is not committed")
        if (runtime_root / relative).read_bytes() != _read_committed_bytes(
            REPO_ROOT, source_revision, relative
        ):
            raise MemoOwnerReviewError("runtime central contract differs from source")
        evidence_refs.append(relative)

    returned = payload.get("reviewed_memory")
    if not isinstance(returned, list) or not returned:
        raise MemoOwnerReviewError("memo brief returned no reviewed memory")
    seen: set[str] = set()
    for item in returned:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise MemoOwnerReviewError("memo brief reviewed-memory row is malformed")
        item_id = item["id"]
        if item_id in seen or item_id not in by_id:
            raise MemoOwnerReviewError("memo brief reviewed-memory identity is invalid")
        seen.add(item_id)
        canonical = by_id[item_id]
        if canonical.get("source_kind") != "reviewed_corpus":
            raise MemoOwnerReviewError("memo brief returned non-reviewed corpus data")
        if canonical.get("current_recall_status") not in {"allowed", "preferred"}:
            raise MemoOwnerReviewError("memo brief returned disallowed recall data")
        if any(item.get(field) != canonical.get(field) for field in ROW_FIELDS):
            raise MemoOwnerReviewError("memo brief row differs from current catalog")
        source_path = _safe_relative(canonical.get("source_path"), prefix="memo/objects/")
        if not source_path.endswith("/object.json"):
            raise MemoOwnerReviewError("reviewed memory source is not an object bundle")
        if not _committed_exists(REPO_ROOT, source_revision, source_path):
            raise MemoOwnerReviewError("reviewed memory source object is not committed")
        if (runtime_root / source_path).read_bytes() != _read_committed_bytes(
            REPO_ROOT, source_revision, source_path
        ):
            raise MemoOwnerReviewError("runtime memory object differs from source")
        evidence_refs.append(source_path)
    watermark = "aoa-memo-catalog:" + _raw_digest(committed_catalog_raw)
    return watermark, list(dict.fromkeys(evidence_refs))


def _sdk_schema(route: dict[str, str]) -> dict[str, Any]:
    sdk_root = Path(
        os.environ.get(route["env"], str(REPO_ROOT.parent / "aoa-sdk"))
    ).expanduser().resolve()
    schema, _ = _read_committed_json(
        sdk_root, route["pinned_ref"], route["path"], "pinned SDK owner-review schema"
    )
    Draft202012Validator.check_schema(schema)
    return schema


def _owner_schema(source_revision: str) -> tuple[dict[str, Any], str]:
    schema, raw = _read_committed_json(
        REPO_ROOT, source_revision, OWNER_SCHEMA_REF, "memo brief owner-review schema"
    )
    Draft202012Validator.check_schema(schema)
    return schema, _raw_digest(raw)


def review_memo_capture(
    *,
    capture_root: Path,
    receipt_path: Path,
    artifact_path: Path,
    source_revision: str,
    runtime_owner_root: Path,
) -> dict[str, Any]:
    if source_revision != _git_revision(REPO_ROOT):
        raise MemoOwnerReviewError("requested source revision is not current aoa-memo HEAD")
    runtime_root = _require_runtime_owner(runtime_owner_root, source_revision)
    receipt, receipt_raw, receipt_identity = _read_private_json(
        receipt_path, "capture receipt"
    )
    artifact, artifact_raw, artifact_identity = _read_private_json(
        artifact_path, "result artifact"
    )
    signer_id, public_key, sdk_route = _load_trust(source_revision)
    payload, observed_at, capture_expires_at, receipt_ref, artifact_ref = _validate_capture(
        receipt,
        artifact,
        capture_root=capture_root,
        receipt_path=receipt_path,
        artifact_path=artifact_path,
        signer_id=signer_id,
        public_key=public_key,
    )
    owner_schema, owner_schema_digest = _owner_schema(source_revision)
    schema_errors = sorted(
        Draft202012Validator(owner_schema).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    if schema_errors:
        raise MemoOwnerReviewError("memo brief does not satisfy owner review schema")
    provider_watermark, evidence_refs = _ground_payload(
        payload, runtime_root=runtime_root, source_revision=source_revision
    )
    evidence_refs.insert(0, OWNER_SCHEMA_REF)
    _require_unchanged(receipt_path, "capture receipt", receipt_raw, receipt_identity)
    _require_unchanged(artifact_path, "result artifact", artifact_raw, artifact_identity)
    reviewed_at = _aware_time(_utc_now(), "reviewed_at")
    if reviewed_at < observed_at or reviewed_at >= capture_expires_at:
        raise MemoOwnerReviewError("review time is outside the capture window")
    expires_at = min(
        capture_expires_at, reviewed_at + timedelta(seconds=MAX_REVIEW_TTL_SECONDS)
    )
    catalog_digest = _raw_digest(
        _read_committed_bytes(REPO_ROOT, source_revision, CATALOG_REF)
    )
    statement = {
        "schema_version": REVIEW_SCHEMA,
        "review_owner": "aoa-memo",
        "organ_id": "aoa-memo",
        "capability_id": CAPABILITY_ID,
        "primitive_id": PRIMITIVE_ID,
        "owners": {
            "source_owner": "aoa-memo",
            "access_owner": "aoa-memo",
            "control_owner": "aoa-sdk",
            "runtime_owner": "abyss-stack",
            "proof_owner": "aoa-evals",
            "acceptance_owner": "aoa-memo",
        },
        "capture": {
            "capture_owner": "abyss-stack",
            "capture_receipt_ref": receipt_ref,
            "capture_receipt_id": receipt["receipt_id"],
            "result_artifact_ref": artifact_ref,
            "result_artifact_id": artifact["artifact_id"],
            "organ_id": "aoa-memo",
            "capability_id": CAPABILITY_ID,
            "primitive_id": PRIMITIVE_ID,
            "result_digest": receipt["result_digest"],
            "result_schema_identity": RESULT_SCHEMA,
            "server_schema_digest": receipt["server_schema_digest"],
            "primitive_schema_digest": receipt["selected_tool_schema_digest"],
            "observed_at": observed_at.isoformat(),
            "expires_at": capture_expires_at.isoformat(),
        },
        "source_revision": {
            "revision": source_revision,
            "digest": catalog_digest,
            "schema_digest": owner_schema_digest,
        },
        "owner_payload_schema_ref": "owner://aoa-memo/aoa_memo_brief_v1",
        "owner_payload_schema_digest": owner_schema_digest,
        "reviewed_at": reviewed_at.isoformat(),
        "expires_at": expires_at.isoformat(),
        "grounding_state": "grounded",
        "freshness_state": "exact",
        "freshness_policy": {
            "policy_id": "memo-reviewed-catalog-parity-v1",
            "max_age_seconds": MAX_REVIEW_TTL_SECONDS,
            "stale_readable_seconds": 0,
            "cache_scope": "task",
            "provider_watermark_required": True,
        },
        "provider_watermark": provider_watermark,
        "grounding_evidence": [
            {
                "owner": "aoa-memo",
                "evidence_ref": ref,
                "revision": source_revision,
                "observed_at": reviewed_at.isoformat(),
                "expires_at": expires_at.isoformat(),
            }
            for ref in evidence_refs
        ],
        "reason_codes": [],
        "owner_accepted": False,
        "central_proof_asserted": False,
        "admission_asserted": False,
        "cross_organ_proven": False,
        "rollback_proven": False,
        "contains_secrets": False,
        "self_report_is_security_authority": False,
        "claim_limit": CLAIM_LIMIT,
    }
    review = {**statement, "review_id": _digest(statement, ensure_ascii=True)}
    errors = sorted(
        Draft202012Validator(_sdk_schema(sdk_route)).iter_errors(review),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise MemoOwnerReviewError("produced review does not satisfy pinned SDK ABI")
    _require_unchanged(receipt_path, "capture receipt", receipt_raw, receipt_identity)
    _require_unchanged(artifact_path, "result artifact", artifact_raw, artifact_identity)
    if _utc_now() >= expires_at:
        raise MemoOwnerReviewError("owner review expired before completion")
    return review


def _write_private_json(path: Path, payload: dict[str, Any]) -> None:
    absolute = path.expanduser().absolute()
    for component in reversed(absolute.parents):
        if component.is_symlink():
            raise MemoOwnerReviewError("review output cannot traverse a symlink")
    absolute.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if stat.S_IMODE(absolute.parent.stat().st_mode) & 0o077:
        raise MemoOwnerReviewError("review output directory must be private")
    descriptor, name = tempfile.mkstemp(prefix=f".{absolute.name}.", dir=absolute.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, absolute)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--runtime-owner-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    resolved = {
        args.receipt.expanduser().resolve(strict=False),
        args.result.expanduser().resolve(strict=False),
        args.output.expanduser().resolve(strict=False),
    }
    if len(resolved) != 3:
        raise MemoOwnerReviewError("receipt, result, and output paths must be distinct")
    review = review_memo_capture(
        capture_root=args.capture_root,
        receipt_path=args.receipt,
        artifact_path=args.result,
        source_revision=args.source_revision,
        runtime_owner_root=args.runtime_owner_root,
    )
    _write_private_json(args.output, review)
    print(
        json.dumps(
            {
                "review_id": review["review_id"],
                "grounding_state": review["grounding_state"],
                "freshness_state": review["freshness_state"],
                "output": str(args.output.expanduser().absolute()),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
