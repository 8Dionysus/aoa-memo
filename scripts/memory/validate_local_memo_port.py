#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema", file=sys.stderr)
    raise SystemExit(2) from exc

from local_memo_port_common import (
    INDEX_FILENAME,
    PACKET_DIRS,
    PORT_FILENAME,
    ROOT,
    build_index,
    load_json,
    load_port,
    packet_files,
    render_json,
    repo_root_for_port,
    resolve_port_path,
    vocabulary_terms,
)


SCHEMA_DIR = ROOT / "schemas" / "memory-ports"
FORMAT_CHECKER = FormatChecker()
PACKET_SCHEMAS = {
    "candidates": "local_memo_candidate.schema.json",
    "receipts": "local_memo_receipt.schema.json",
    "exports": "local_memo_export.schema.json",
}
VOCAB_FIELDS = {
    "kind": "kind",
    "family": "family",
    "scope": "scope",
    "route": "route",
    "review_state": "review_state",
    "lifecycle": "lifecycle",
    "source_trust": "source_trust",
}
SYMBOLIC_REF_PREFIXES = (
    "repo:",
    "http://",
    "https://",
    "web:",
    "operator:",
    "state_capsule:",
    "audit_event:",
    "claim:",
    "bridge:",
    "episode:",
    "memory:",
    "candidate:",
    "receipt:",
    "export:",
)


def schema_errors(schema_name: str, payload: Any, path: Path) -> list[str]:
    schema = load_json(SCHEMA_DIR / schema_name)
    validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    return [
        f"{path}:{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(payload), key=lambda err: list(err.absolute_path))
    ]


def resolve_ref(port_path: Path, ref: str) -> Path | None:
    if ref.startswith(SYMBOLIC_REF_PREFIXES):
        return None
    text = ref.split("#", 1)[0]
    if not text:
        return None
    path = Path(text)
    if path.is_absolute():
        return path
    if text.startswith("memo/"):
        return repo_root_for_port(port_path) / text
    candidate = port_path / text
    if candidate.exists():
        return candidate
    return repo_root_for_port(port_path) / text


def check_refs(errors: list[str], port_path: Path, path: Path, label: str, refs: Any) -> None:
    if not isinstance(refs, list):
        errors.append(f"{path}:{label} must be a list")
        return
    for index, ref in enumerate(refs):
        if not isinstance(ref, str) or not ref:
            errors.append(f"{path}:{label}[{index}] must be a non-empty string")
            continue
        target = resolve_ref(port_path, ref)
        if target is not None and not target.exists():
            errors.append(f"{path}:{label}[{index}] points to missing ref {ref}")


def check_vocabulary(errors: list[str], path: Path, payload: dict[str, Any], terms: dict[str, set[str]]) -> None:
    for field, term_group in VOCAB_FIELDS.items():
        value = payload.get(field)
        if isinstance(value, str) and value not in terms.get(term_group, set()):
            errors.append(f"{path}:{field} uses unknown vocabulary term {value!r}")
    risks = payload.get("risk", [])
    if isinstance(risks, list):
        for risk in risks:
            if isinstance(risk, str) and risk not in terms.get("risk", set()):
                errors.append(f"{path}:risk uses unknown vocabulary term {risk!r}")


def validate_candidate_semantics(errors: list[str], path: Path, payload: dict[str, Any]) -> None:
    guardrails = payload.get("guardrails", {})
    if isinstance(guardrails, dict):
        if guardrails.get("direct_durable_write") is not False:
            errors.append(f"{path}:guardrails.direct_durable_write must be false")
        if guardrails.get("instructions_treated_as_data") is not True:
            errors.append(f"{path}:guardrails.instructions_treated_as_data must be true")
    if payload.get("source_trust") in {"untrusted", "unknown", "review_required"}:
        if payload.get("lifecycle") in {"current", "frozen"}:
            errors.append(f"{path}:unreviewed local candidate must not claim lifecycle {payload.get('lifecycle')!r}")
    if payload.get("route") == "reviewed_intake" and guardrails.get("requires_reviewed_intake") is not True:
        errors.append(f"{path}:reviewed_intake candidates must keep requires_reviewed_intake true")


def validate_port(path: str | Path) -> list[str]:
    port_path = resolve_port_path(path)
    errors: list[str] = []
    port_file = port_path / PORT_FILENAME
    if not port_file.exists():
        return [f"{port_file} is missing"]
    try:
        port_payload = load_port(port_path)
    except Exception as exc:
        return [f"{port_file}: {exc}"]

    errors.extend(schema_errors("local_memo_port.schema.json", port_payload, port_file))
    terms = vocabulary_terms(port_payload)

    for directory in PACKET_DIRS:
        expected = port_path / str(port_payload.get(f"{directory[:-1]}_dir", directory))
        if directory == "candidates":
            expected = port_path / str(port_payload.get("candidate_dir", directory))
        elif directory == "receipts":
            expected = port_path / str(port_payload.get("receipt_dir", directory))
        elif directory == "exports":
            expected = port_path / str(port_payload.get("export_dir", directory))
        elif directory == "local":
            expected = port_path / str(port_payload.get("local_dir", directory))
        if not expected.is_dir():
            errors.append(f"{expected} is missing or not a directory")

    for directory, schema_name in PACKET_SCHEMAS.items():
        for packet in packet_files(port_path, directory):
            try:
                payload = load_json(packet)
            except json.JSONDecodeError as exc:
                errors.append(f"{packet}: invalid JSON: {exc}")
                continue
            if not isinstance(payload, dict):
                errors.append(f"{packet}: packet must be a JSON object")
                continue
            errors.extend(schema_errors(schema_name, payload, packet))
            if payload.get("repo") != port_payload.get("repo"):
                errors.append(f"{packet}: repo must match PORT.yaml repo")
            if directory == "candidates":
                check_vocabulary(errors, packet, payload, terms)
                check_refs(errors, port_path, packet, "source_refs", payload.get("source_refs"))
                check_refs(errors, port_path, packet, "evidence_refs", payload.get("evidence_refs"))
                validate_candidate_semantics(errors, packet, payload)
            elif directory == "receipts":
                check_refs(errors, port_path, packet, "candidate_ref", [payload.get("candidate_ref")])
                if payload.get("route") not in terms.get("route", set()):
                    errors.append(f"{packet}:route uses unknown vocabulary term {payload.get('route')!r}")
            elif directory == "exports":
                check_refs(errors, port_path, packet, "candidate_refs", payload.get("candidate_refs"))
                check_refs(errors, port_path, packet, "receipt_refs", payload.get("receipt_refs"))
                check_refs(errors, port_path, packet, "source_refs", payload.get("source_refs"))
                check_refs(errors, port_path, packet, "evidence_refs", payload.get("evidence_refs"))

    index_path = port_path / INDEX_FILENAME
    if index_path.exists():
        try:
            index_payload = load_json(index_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{index_path}: invalid JSON: {exc}")
        else:
            errors.extend(schema_errors("local_memo_port_index.schema.json", index_payload, index_path))
            expected_index = build_index(port_path)
            if render_json(index_payload) != render_json(expected_index):
                errors.append(f"{index_path} is not up to date")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a local memo port.")
    parser.add_argument("--path", required=True, help="Path to a local memo port.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_port(args.path)
    if errors:
        print("Local memo port validation failed.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"[ok] local memo port is valid: {resolve_port_path(args.path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

