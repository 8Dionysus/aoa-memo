from __future__ import annotations

from pathlib import Path

from local_memo_port_common import load_json, load_port, resolve_port_path
from reviewed_intake_landing_common import (
    JsonDict,
    LandingError,
    LandingInputs,
    export_ref_path,
    packet_ref_path,
    schema_errors,
)
from validate_local_memo_port import check_refs, validate_candidate_semantics


def validate_inputs(
    *,
    port_path: Path,
    export_path: Path,
    port_payload: JsonDict,
    export_payload: JsonDict,
    candidate_paths: list[Path],
    candidate_payloads: list[JsonDict],
    receipt_paths: list[Path],
    receipt_payloads: list[JsonDict],
) -> None:
    errors: list[str] = []
    errors.extend(schema_errors("local_memo_export.schema.json", export_payload, export_path))
    repo = str(port_payload.get("repo") or "")
    if export_payload.get("repo") != repo:
        errors.append(f"{export_path}: repo must match PORT.yaml repo")
    if export_payload.get("allowed_result") != "reviewed_write":
        errors.append(f"{export_path}: allowed_result must be 'reviewed_write' for corpus landing")
    if not receipt_payloads:
        errors.append(f"{export_path}: reviewed_write landing requires at least one receipt_ref")
    check_refs(errors, port_path, export_path, "source_refs", export_payload.get("source_refs"))
    check_refs(errors, port_path, export_path, "evidence_refs", export_payload.get("evidence_refs"))
    candidate_refs = [
        ref
        for ref in export_payload.get("candidate_refs", [])
        if isinstance(ref, str)
    ]
    candidate_ref_by_path = {
        candidate_path.resolve(): candidate_ref
        for candidate_path, candidate_ref in zip(candidate_paths, candidate_refs, strict=False)
    }
    exported_candidate_paths = set(candidate_ref_by_path)
    successful_receipts_by_candidate: dict[Path, list[Path]] = {}

    for candidate_path, candidate in zip(candidate_paths, candidate_payloads, strict=True):
        errors.extend(schema_errors("local_memo_candidate.schema.json", candidate, candidate_path))
        if candidate.get("repo") != repo:
            errors.append(f"{candidate_path}: repo must match PORT.yaml repo")
        if candidate.get("route") != "reviewed_intake":
            errors.append(f"{candidate_path}: route must be reviewed_intake for corpus landing")
        if candidate.get("review_state") in {"rejected", "superseded", "archived"}:
            errors.append(f"{candidate_path}: review_state blocks corpus landing")
        if candidate.get("source_trust") in {"untrusted", "unknown"}:
            errors.append(f"{candidate_path}: source_trust {candidate.get('source_trust')!r} blocks corpus landing")
        check_refs(errors, port_path, candidate_path, "source_refs", candidate.get("source_refs"))
        check_refs(errors, port_path, candidate_path, "evidence_refs", candidate.get("evidence_refs"))
        validate_candidate_semantics(errors, candidate_path, candidate)

    for receipt_path, receipt in zip(receipt_paths, receipt_payloads, strict=True):
        errors.extend(schema_errors("local_memo_receipt.schema.json", receipt, receipt_path))
        if receipt.get("repo") != repo:
            errors.append(f"{receipt_path}: repo must match PORT.yaml repo")
        if receipt.get("route") != "reviewed_intake":
            errors.append(f"{receipt_path}: route must be reviewed_intake for corpus landing")
        if receipt.get("result") not in {"validated", "forwarded", "landed"}:
            errors.append(f"{receipt_path}: result must be validated, forwarded, or landed before corpus landing")
        if receipt.get("errors"):
            errors.append(f"{receipt_path}: receipt with errors cannot support corpus landing")
        check_refs(errors, port_path, receipt_path, "candidate_ref", [receipt.get("candidate_ref")])
        receipt_candidate_ref = receipt.get("candidate_ref")
        receipt_candidate_path = None
        if isinstance(receipt_candidate_ref, str) and receipt_candidate_ref:
            try:
                receipt_candidate_path = packet_ref_path(port_path, receipt_candidate_ref, "receipt candidate_ref")
            except LandingError:
                receipt_candidate_path = None
        if receipt_candidate_path is None:
            continue
        receipt_candidate_path = receipt_candidate_path.resolve()
        if receipt_candidate_path not in exported_candidate_paths:
            errors.append(f"{receipt_path}: candidate_ref {receipt_candidate_ref} is not listed in export candidate_refs")
            continue
        if (
            receipt.get("repo") == repo
            and receipt.get("route") == "reviewed_intake"
            and receipt.get("result") in {"validated", "forwarded", "landed"}
            and not receipt.get("errors")
        ):
            successful_receipts_by_candidate.setdefault(receipt_candidate_path, []).append(receipt_path)

    for candidate_path in candidate_paths:
        candidate_key = candidate_path.resolve()
        if candidate_key not in successful_receipts_by_candidate:
            candidate_ref = candidate_ref_by_path.get(candidate_key, candidate_path.relative_to(port_path).as_posix())
            errors.append(f"{export_path}: missing successful receipt for candidate_ref {candidate_ref}")

    if errors:
        rendered = "\n".join(f"- {error}" for error in errors)
        raise LandingError(f"reviewed intake landing input validation failed:\n{rendered}")


def load_landing_inputs(port: str | Path, export_ref: str | Path) -> LandingInputs:
    port_path = resolve_port_path(port)
    port_payload = load_port(port_path)
    export_dir = str(port_payload.get("export_dir", "exports"))
    export_path = export_ref_path(port_path, str(export_ref), export_dir)
    export_payload = load_json(export_path)
    if not isinstance(export_payload, dict):
        raise LandingError(f"{export_path}: export packet must be a JSON object")

    candidate_refs = export_payload.get("candidate_refs", [])
    receipt_refs = export_payload.get("receipt_refs", [])
    if not isinstance(candidate_refs, list):
        candidate_refs = []
    if not isinstance(receipt_refs, list):
        receipt_refs = []
    candidate_paths = [
        packet_ref_path(port_path, ref, "candidate_ref")
        for ref in candidate_refs
        if isinstance(ref, str)
    ]
    receipt_paths = [
        packet_ref_path(port_path, ref, "receipt_ref")
        for ref in receipt_refs
        if isinstance(ref, str)
    ]
    candidate_payloads = [load_json(path) for path in candidate_paths]
    receipt_payloads = [load_json(path) for path in receipt_paths]
    if not all(isinstance(payload, dict) for payload in candidate_payloads + receipt_payloads):
        raise LandingError("candidate and receipt packets must be JSON objects")

    validate_inputs(
        port_path=port_path,
        export_path=export_path,
        port_payload=port_payload,
        export_payload=export_payload,
        candidate_paths=candidate_paths,
        candidate_payloads=candidate_payloads,
        receipt_paths=receipt_paths,
        receipt_payloads=receipt_payloads,
    )
    return LandingInputs(
        port_path=port_path,
        export_path=export_path,
        port_payload=port_payload,
        export_payload=export_payload,
        candidate_paths=candidate_paths,
        candidate_payloads=candidate_payloads,
        receipt_paths=receipt_paths,
        receipt_payloads=receipt_payloads,
    )
